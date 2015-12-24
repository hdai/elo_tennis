import csv
import math
import pickle
import pandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from pandas import DataFrame
from pandas import Series


#define k factor assumptions
def k_factor(matches_played):
	K = 250
	offset = 5
	shape = 0.4
	return K/(matches_played + offset)**shape

#winning a match regardless the number of sets played = 1
score = 1

#define a function for calculating the expected score of player_A
#expected score of player_B = 1 - expected score of player
def calc_exp_score(playerA_rating, playerB_rating):
	exp_score = 1/(1+(10**((playerB_rating - playerA_rating)/400)))
	return exp_score
	
#define a function for calculating new elo
def update_elo(old_elo, k, actual_score, expected_score):
	new_elo = old_elo + k *(actual_score - expected_score)	return new_elo

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

#Column headers for player dataframe
player_col_header = ['player_id', 'last_name', 'first_name', 'country']

#Create a dataframe for keeping track of player info
#every player starts with an elo rating of 1500
players = DataFrame(all_players, columns = player_col_header)
players['current_elo'] = Series(1500, index=players.index)
players['last_tourney_date'] = Series('N/A', index=players.index)
players['matches_played'] = Series(0, index=players.index)
players['peak_elo'] = Series(1500, index=players.index)
players['peak_elo_date'] = Series('N/A', index=players.index)

#Convert objects within dataframe to numeric
players = players.convert_objects(convert_numeric=True)

#Create an empty dataframe to store time series elo for top 10 players based on peak elo rating
#Use player_id as the column header of the dataframe
#Top ten players consist of: Djokovic, Federer, McEnroe, Nadal, Borg, Lendl, Becker, Murray, Sampras, Connors 
elo_timeseries_col_header = [104925, 103819, 100581, 104745, 100437, 100656, 101414, 104918, 101948, 100284]
elo_timeseries = DataFrame(columns=elo_timeseries_col_header)

#read through matches file for each year to update players data frame
#starting from current_year
current_year = 1968

for i in range((2015-1968)+1):
	current_year_file_name = 'atp_matches_'+ str(current_year) + '.csv'

	#read match CSV file and store important columns into lists
	with open(current_year_file_name) as csvfile:
		readCSV = csv.reader(csvfile, delimiter= ',')
		col_index = [0,5,7,17,27,28,29]
		all_matches = []
		for row in readCSV:
			match_info = []
			for i in col_index:
				match_info.append(row[i])
			all_matches.append(match_info)
		
	#separate column names and match info
	header_info = all_matches[0]
	all_matches = all_matches[1:]

	#Create a dataframe to store match info
	matches = DataFrame(all_matches, columns=header_info)

	#Convert objects within matches dataframe to numeric
	matches = matches.convert_objects(convert_numeric=True)
	
	#Sort matches dataframe by tourney_date and then by round
	sorter = ['RR', 'R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F']
	matches.round = matches.round.astype('category')
	matches.round.cat.set_categories(sorter, inplace=True)
	matches = matches.sort(['tourney_date', 'round'], ascending = [1, sorter])

	for index, row in matches.iterrows():
		winner_id = row['winner_id']
		loser_id = row['loser_id']
		tourney_date = row['tourney_date']
		index_winner = players[players['player_id'] == winner_id].index.tolist()
		index_loser = players[players['player_id'] == loser_id].index.tolist()
		old_elo_winner = players.loc[index_winner[0], 'current_elo'] 
		old_elo_loser = players.loc[index_loser[0], 'current_elo']
		exp_score_winner = calc_exp_score(old_elo_winner, old_elo_loser)
		exp_score_loser = 1 - exp_score_winner 
		matches_played_winner = players.loc[index_winner[0], 'matches_played']
		matches_played_loser = players.loc[index_loser[0], 'matches_played']
		new_elo_winner = update_elo(old_elo_winner, k_factor(matches_played_winner), score, exp_score_winner)
		new_elo_loser = update_elo(old_elo_loser, k_factor(matches_played_loser), score-1, exp_score_loser)
		players.loc[index_winner[0], 'current_elo'] = new_elo_winner
		players.loc[index_winner[0], 'last_tourney_date'] = tourney_date
		players.loc[index_winner[0], 'matches_played'] = players.loc[index_winner[0], 'matches_played'] + 1
		players.loc[index_loser[0], 'current_elo'] = new_elo_loser
		players.loc[index_loser[0], 'last_tourney_date'] = tourney_date
		players.loc[index_loser[0], 'matches_played'] = players.loc[index_loser[0], 'matches_played'] + 1
		if new_elo_winner > players.loc[index_winner[0], 'peak_elo']:
			players.loc[index_winner[0], 'peak_elo'] = new_elo_winner
			players.loc[index_winner[0], 'peak_elo_date'] = row['tourney_date']
		
		#Convert tourney_date to a time stamp, then update elo_timeseries data frame
		tourney_date_timestamp = pandas.to_datetime(tourney_date, format='%Y%m%d')
		if tourney_date_timestamp not in elo_timeseries.index:
			elo_timeseries.loc[tourney_date_timestamp, elo_timeseries_col_header] = np.nan
		
		if (winner_id in elo_timeseries_col_header) and (loser_id in elo_timeseries_col_header):
			elo_timeseries.ix[tourney_date_timestamp, winner_id]= new_elo_winner
			elo_timeseries.ix[tourney_date_timestamp, loser_id]= new_elo_loser
		elif winner_id in elo_timeseries_col_header:
			elo_timeseries.ix[tourney_date_timestamp, winner_id]= new_elo_winner
		elif loser_id in elo_timeseries_col_header:
			elo_timeseries.ix[tourney_date_timestamp, loser_id]= new_elo_loser
			
	##Uncomment to output year end elo_rankings for every year between 1968 and 2015
	#output_file_name = str(current_year) + '_yr_end_elo_ranking.csv'
	#players.to_csv(output_file_name)

	current_year = current_year + 1


players.to_csv('2015_yr_end_elo_ranking.csv')
players = pandas.read_csv('2015_yr_end_elo_ranking.csv')
#Print all-time top 10 peak_elo
print players.sort(columns= 'peak_elo', ascending=False)[:10]

#Save elo_timeseries dataframe for plotting purposes
elo_timeseries.to_pickle('elo_timeseries.pkl')

#Open saved pickle file and save into a dataframe
elo_timeseries = pandas.read_pickle('elo_timeseries.pkl')

#Convert objects within elo_timeseries dataframe to numeric
elo_timeseries = elo_timeseries.convert_objects(convert_numeric=True)

#Use linear interpolation for elo_ratings
elo_timeseries = elo_timeseries.interpolate(method='linear')

#Store the indices in the elo_timeseries in a list
index_timestamp = list(elo_timeseries.index.values)

#Get rid of elo ratings since known last_tourney_date
for player in elo_timeseries_col_header:
	player_index = players[players['player_id'] == player].index.tolist()
	player_last_played = players.loc[player_index[0], 'last_tourney_date']
	player_last_played_timestamp = np.datetime64(pandas.to_datetime(player_last_played, format='%Y%m%d'))

	elo_ratings_remove = index_timestamp[index_timestamp.index(player_last_played_timestamp)+1:]

	for i in elo_ratings_remove:
		elo_timeseries.loc[i, player] = np.nan

style.use('stylesheet.mplstyle')
plt.plot(elo_timeseries.index, elo_timeseries[104925]) #Djokovic
plt.plot(elo_timeseries.index, elo_timeseries[103819]) #Federer
plt.plot(elo_timeseries.index, elo_timeseries[100581]) #McEnroe
plt.plot(elo_timeseries.index, elo_timeseries[104745]) #Nadal
plt.plot(elo_timeseries.index, elo_timeseries[100437]) #Borg
plt.plot(elo_timeseries.index, elo_timeseries[100656]) #Lendl
plt.plot(elo_timeseries.index, elo_timeseries[101414]) #Becker
plt.plot(elo_timeseries.index, elo_timeseries[104918]) #Murray
plt.plot(elo_timeseries.index, elo_timeseries[101948]) #Sampras
plt.plot(elo_timeseries.index, elo_timeseries[100284]) #Connors

plt.title("Historical elo ratings for top 10 ATP players", fontsize=25, y=1.1, weight = 'bold')   
plt.xlabel("Years starting in the Open-Era", labelpad= 25)
plt.ylabel("Elo rating", labelpad= 32)
plt.axhline(1200, color='grey', linewidth=5)

plt.show()