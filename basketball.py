import xmltodict
import requests
from operator import itemgetter
from flask import Flask	

application = Flask(__name__)


#try to make an http request for XML data, if succesful parse to dictionary and return new datastructure
def get_data(url):
	try:
		tempData = requests.get(url).text
	except:
		print('error retrieving data from url')
		return 0

	#print(teams_xml)

	try:
		tempData = xmltodict.parse(tempData)
	except:
		print ('error parsing data to xml')
		return 0

	return tempData

@application.route('/')
def main():

# 	 Win score formula: Win Score Formula=[(Points)+(Rebounds)+(Steals)+(½Assists)+(½Blocked Shots)-(Field Goal Attempts)-(Turnovers)-½(Free Throw Attempts)]/Games
#  You’ll need to apply additional logic to obtain Field Goal Attempts & Free Throw Attempts
#  Field Goal Attempts = (((PTS - 3*THREES)*0.45)/FG
# Free Throw Attempts = (((PTS - 3*THREES)*0.1)/FT
	print('hello world')

	players = {}

	#teams = get_data('https://www.fantasybasketballnerd.com/service/teams')

#Make the initial HTTP request to get the xml data
	stats = get_data('https://www.fantasybasketballnerd.com/service/draft-projections')


#iterate through the players to add the FGA and FTA to calculate Win Score
	for x in stats['FantasyBasketballNerd']['Player']:
		fga = (((float(x['PTS']) - 3*float(x['THREES']))*0.45)/float(x['FG']))
		fta = (((float(x['PTS'])- 3*float(x['THREES']))*0.1)/float(x['FT']))
		win_score = (float(x['PTS'])+float(x['REB'])+float(x['STL'])+(0.5*float(x['AST']))+(0.5*float(x['BLK']))-fga-float(x['TO'])-(0.5*fta)/float(x['Games']))

#Create a player record with the win score
		player = (x['name'],x['team'],win_score)

#build  dictionary to group the players by Position		
		if x['position'] in players:
			players[x['position']].append(player)
		else:
			players[x['position']] = [player]

	dataOut = {}

	for key in players.keys():
		count = 0
		total = 0
		for x in players[key]:
			count += 1
			total += x[2]

		#this will sort the list of players by win score for each position (key), we take item 0 to get the first in the list
		top = (sorted(players[key], key=itemgetter(2), reverse=True)[0])

		avg = total / count

		dataOut[key] = {"name":top[0],"team":top[1],"win_score":top[2],"avg":avg}



		#initialize the table and build the header row
		tableBuilder = """<table class="tg">
						<tr>
							<th class="tg-yw4l">Position</th>
							<th class="tg-yw4l">Top Player by Win Score</th>
							<th class"tg-yw41">Top Player's Team</th>
							<th class="tg-yw4l">Win Score</th>
						    <th class="tg-yw4l">Average Win Score for Position</th>
						    <th class="tg-yw4l">Differential</th>
					 	</tr>"""

		for key in dataOut.keys():
			tableBuilder += '<tr><td class="tg-yw4l">'+key+'</td>'
			tableBuilder += '<td class="tg-yw4l">'+dataOut[key]["name"]+'</td>'
			tableBuilder += '<td class="tg-yw4l">'+dataOut[key]["team"]+'</td>'
			tableBuilder += '<td class="tg-yw4l">'+str(dataOut[key]["win_score"])+'</td>'
			tableBuilder += '<td class="tg-yw4l">'+str(dataOut[key]["avg"])+'</td>'
			tableBuilder += '<td class="tg-yw4l">'+str(dataOut[key]["win_score"] - dataOut[key]["avg"])+'</td>'
			tableBuilder += '</tr>'

		tableBuilder +='</table>'


		#print('{"Position": "'+key+'", "'+str(top[0]) +' - '+ str(top[1])+'" : "'+str(top[2])+'" ,"Average": "'+str(avg) +'"}')

	# for key, value in players.items():
	# 	print(key)
	# 	print(value)
		#for postition in values:
			#print(sorted(players['SF'], key=itemgetter(2), reverse=True))

	return("""<html>
			<head>
			<title> Top NBA Players by Win Score by Position </title>
			</head>
			<body>
			<style type="text/css">
			.tg  {border-collapse:collapse;border-spacing:0;}
			.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
			.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
			.tg .tg-yw4l{vertical-align:top}
			</style>""" + tableBuilder +"""</body></html>""")
 


if __name__ == '__main__':
	#main()
	application.run()
