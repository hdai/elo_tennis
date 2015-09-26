import csv
from pandas import DataFrame

#read CSV file and store important columns into lists
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
df = DataFrame(all_matches, columns=header_info)

#Convert objects within dataframe to int64
df = df.convert_objects(convert_numeric=True)




			


			
