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

# 	 Win score formula: Win Score Formula=[(Points)+(Rebounds)+(Steals)+(½Assists)+(½Blocked Shots)-
#  (Field Goal Attempts)-(Turnovers)-½(Free Throw Attempts)]/Games
#  You’ll need to apply additional logic to obtain Field Goal Attempts & Free Throw Attempts
#  Field Goal Attempts = (((PTS - 3*THREES)*0.45)/FG
# Free Throw Attempts = (((PTS - 3*THREES)*0.1)/FT

	players = {}

	#teams = get_data('https://www.fantasybasketballnerd.com/service/teams')

#Make the initial HTTP request to get the xml data
	stats = get_data('https://www.fantasybasketballnerd.com/service/draft-projections')


#iterate through the players to add the FGA and FTA to calculate Win Score
	for x in stats['FantasyBasketballNerd']['Player']:
		fga = (((float(x['PTS']) - 3*float(x['THREES']))*0.45)/float(x['FG']))
		fta = (((float(x['PTS'])- 3*float(x['THREES']))*0.1)/float(x['FT']))
		win_score = (float(x['PTS'])+float(x['REB'])+float(x['STL'])+(0.5*float(x['AST']))+(0.5*float(x['BLK']))-fga-float(x['TO'])-(0.5*fta))/float(x['Games'])

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
			tableBuilder += '<td class="tg-yw4l">'+str(format(dataOut[key]["win_score"],'.2f'))+'</td>'
			tableBuilder += '<td class="tg-yw4l">'+str(format(dataOut[key]["avg"],'.2f'))+'</td>'
			tableBuilder += '<td class="tg-yw41"><font color="green">+'+str(format(dataOut[key]["win_score"] - dataOut[key]["avg"],'.2f'))+'</font></td>'
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
			.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:bold;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
			.tg .tg-yw4l{vertical-align:top}
			</style>""" + tableBuilder +"""</body></html>""")
 
@application.route('/graph')
def graph():
 # 	 Win score formula: Win Score Formula=[(Points)+(Rebounds)+(Steals)+(½Assists)+(½Blocked Shots)-
#  (Field Goal Attempts)-(Turnovers)-½(Free Throw Attempts)]/Games
#  You’ll need to apply additional logic to obtain Field Goal Attempts & Free Throw Attempts
#  Field Goal Attempts = (((PTS - 3*THREES)*0.45)/FG
# Free Throw Attempts = (((PTS - 3*THREES)*0.1)/FT

	players = {}

	#teams = get_data('https://www.fantasybasketballnerd.com/service/teams')

#Make the initial HTTP request to get the xml data
	stats = get_data('https://www.fantasybasketballnerd.com/service/draft-projections')


#iterate through the players to add the FGA and FTA to calculate Win Score
	for x in stats['FantasyBasketballNerd']['Player']:
		fga = (((float(x['PTS']) - 3*float(x['THREES']))*0.45)/float(x['FG']))
		fta = (((float(x['PTS'])- 3*float(x['THREES']))*0.1)/float(x['FT']))
		win_score = (float(x['PTS'])+float(x['REB'])+float(x['STL'])+(0.5*float(x['AST']))+(0.5*float(x['BLK']))-fga-float(x['TO'])-(0.5*fta))/float(x['Games'])

#Create a player record with the win score
		player = (x['name'],x['team'],win_score)

#build  dictionary to group the players by Position		
		if x['position'] in players:
			players[x['position']].append(player)
		else:
			players[x['position']] = [player]

	dataOut = '['

	for key in players.keys():
		count = 0
		total = 0
		for x in players[key]:
			count += 1
			total += x[2]

		#this will sort the list of players by win score for each position (key), we take item 0 to get the first in the list
		top = (sorted(players[key], key=itemgetter(2), reverse=True)[0])

		avg = total / count

		if key == 'PF':
			x,y = 245,565
		elif key == 'C':
			x,y = 540,510
		elif key == 'PG':
			x,y = 400,250
		elif key == 'SF':
			x,y = 620,610
		elif key == 'SG':
			x,y = 120,320
		else:
			print('error parsing position')

		dataOut += '{"x":'+str(x)+',"y":'+str(y)+',"r":'+str(format(top[2],'.2f'))+',"name":"'+str(top[0])+'","pos":"'+key+'","team": "'+top[1]+'"},'

	dataOut = dataOut[:-1]
	dataOut += ']'

	print (dataOut)
	

#	var data = [{x: 245, y: 565, r:20, name:"Kevin Love", pos:"PF", team:"DAL"},
#						{x: 540, y: 510, r:20, name:"DeAndre Jordan", pos:"C", team:"DAL"},
#           {x: 400, y: 250 , r:20, name:"Kevin Rose",pos:"PG", team:"DAL"},
#						{x: 620, y: 610, r:20, name:"Kevin Durant", pos:"SF", team:"DAL"},
#						{x: 120, y: 320, r:20, name:"Kevin Hardaway", pos:"SG", team:"DAL"}];


	return("""<html>
			<head>
			<title> Top NBA Players by Win Score by Position </title>
			</head>
			<body>
			<style type="text/css">
			svg{
  			 background-image: url("/static/court3.jpg");
			   }

			circle{
			  fill: orange;
			}

			text{;
			  font-size: 20px;
			}
			</style></body>

<script src="//d3js.org/d3.v3.min.js"></script>
<script>var svg = d3.select("body").append("svg")
    .attr("width", '800px')
    .attr("height", '720px')
    .attr("stroke",'black');
  
var data = """+dataOut+""";

var circles = svg.selectAll("circle")
                          .data(data)
                          .enter()
                          .append("circle");

var circleAttributes = circles
                       .attr("cx", function (d) { return d.x; })
                       .attr("cy", function (d) { return d.y; })
                       .attr("r", function (d) { return d.r*1.75; });

//Add the SVG Text Element to the svgContainer
var text = svg.selectAll("text")
                        .data(data)
                        .enter();

//Add SVG Text Element Attributes
text.append("text")
                .attr("x", function(d) { return d.x + 30; })
                .attr("y", function(d) { return d.y - 20; })
                .text(function(d) { return d.name});
                
text.append("text")
                .attr("x", function(d) { return d.x + 30; })
                .attr("y", function(d) { return d.y; })
                .text(function(d) { return d.team});
                
text.append("text")
                .attr("x", function(d) { return d.x + 30; })
                .attr("y", function(d) { return d.y+20; })
                .text(function(d) { return 'win score: '+d.r});

text.append("text")
                .attr("x", function(d) { return d.x-15; })
                .attr("y", function(d) { return d.y+2; })
                .text(function(d) { return '('+d.pos+')'});


                    </script></html>""")


if __name__ == '__main__':
	#main()
	application.run()
