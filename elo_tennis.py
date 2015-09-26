import csv
from pandas import DataFrame
from pandas import Series

#define assumptions
k_factor = 20
score = 1

#define a function for calculating the expected score of player_A
def calc_exp_score(playerA_rating, playerB_rating):
	exp_score = 1/(1+10^((playerB_rating - playerA_rating)/400))
	return exp_score
	
#define a function for calculating new elo
def update_elo(old_elo, k_factor, actual_score, expected_score):
	new_elo = old_elo + k * (actual_score - expected_score)
	return new_elo

#read player CSV file and store important columns into lists
with open('atp_players.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter= ',')
	col_index = [0,1,2,5]
	all_players = []
	for row in readCSV:
		player_info = []
		for i in col_index:
			player_info.append(row[i])
		all_players.append(player_info)

player_col_header = ['player_id', 'last_name', 'first_name', 'country']
players = DataFrame(all_players, columns = player_col_header)

#Create a dataframe for keeping track of player elo rating
#every player starts with an elo rating of 1500
elo_rating = players
elo_rating['elo'] = Series(1500, index=elo_rating.index)
elo_rating['last_tourney_date'] = Series('N/A', index=elo_rating.index)

#read match CSV file and store important columns into lists
with open('atp_matches_1969.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter= ',')
	col_index = [0,5,7,17,27,28]
	all_matches = []
	for row in readCSV:
		match_info = []
		for i in col_index:
			match_info.append(row[i])
		all_matches.append(match_info)
		
#separate match_info
header_info = all_matches[0]
all_matches = all_matches[1:]

#create a dataframe
matches = DataFrame(all_matches, columns=header_info)

#Convert objects within dataframe to int64
players = players.convert_objects(convert_numeric=True)

#find index of a player in players data frame by player_id
ind = players[players['player_id']==100001].index.tolist()

players.loc[ind[0],'elo'] = players.loc[ind[0], 'elo'] + 0
players.loc[ind[0],'last_tourney_date'] = '1993-03-22'


winner_id = matches.loc[0, 'winner_id']
loser_id = matches.loc[0, 'loser_id']
tourney_date = matches.loc[0, 'tourney_date']











			


			
