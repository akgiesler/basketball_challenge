I’d like you to write a script to determine the player with the best Win Score per game by position (see formula below). I need you to use Python and/or R as the scripting language (Javascript is acceptable. Please, automatically pull in the data via an http request from the following source
https://www.fantasybasketballnerd.com/fantasy-basketball-api#teams
 Apply the following formula to obtain win score:
 Win score formula: Win Score Formula=[(Points)+(Rebounds)+(Steals)+(½Assists)+(½Blocked Shots)-(Field Goal Attempts)-(Turnovers)-½(Free Throw Attempts)]/Games
 You’ll need to apply additional logic to obtain Field Goal Attempts & Free Throw Attempts
 Field Goal Attempts = (((PTS - 3*THREES)*0.45)/FG
Free Throw Attempts = (((PTS - 3*THREES)*0.1)/FT