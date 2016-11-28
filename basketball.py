import xmltodict
import requests
from operator import itemgetter


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


def main():

# 	 Win score formula: Win Score Formula=[(Points)+(Rebounds)+(Steals)+(½Assists)+(½Blocked Shots)-(Field Goal Attempts)-(Turnovers)-½(Free Throw Attempts)]/Games
#  You’ll need to apply additional logic to obtain Field Goal Attempts & Free Throw Attempts
#  Field Goal Attempts = (((PTS - 3*THREES)*0.45)/FG
# Free Throw Attempts = (((PTS - 3*THREES)*0.1)/FT
	print('hello world')

	players = {}

	#teams = get_data('https://www.fantasybasketballnerd.com/service/teams')

	stats = get_data('https://www.fantasybasketballnerd.com/service/draft-projections')

	#for key,value in stats['Player'].items():
	#	print(value)

	#print(stats['FantasyBasketballNerd']['Player'])

	for x in stats['FantasyBasketballNerd']['Player']:
		fga = (((float(x['PTS']) - 3*float(x['THREES']))*0.45)/float(x['FG']))
		fta = (((float(x['PTS'])- 3*float(x['THREES']))*0.1)/float(x['FT']))
		win_score = (float(x['PTS'])+float(x['REB'])+float(x['STL'])+(0.5*float(x['AST']))+(0.5*float(x['BLK']))-fga-float(x['TO'])-(0.5*fta)/float(x['Games']))

		player = (x['name'],x['team'],win_score)
		if x['position'] in players:
			players[x['position']].append(player)
		else:
			players[x['position']] = [player]

	print(sorted(players['SF'], key=itemgetter(2), reverse=True))







if __name__ == '__main__':
	main()
