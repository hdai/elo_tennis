## Historical ATP Ranking using the Elo rating system

After reading *FiveThirtyEight*'s piece about how [Serena Williams stacks up against all-time female greats](http://fivethirtyeight.com/features/serena-williams-and-the-difference-between-all-time-great-and-greatest-of-all-time/#fn-2) using the Elo rating system, I attempted to apply the same rating system to men's tennis with Python. *FiveThirtyEight* applied [the elo rating system to men's tennis](http://fivethirtyeight.com/features/djokovic-and-federer-are-vying-to-be-the-greatest-of-all-time/) as well. 

> The [Elo Rating system](https://en.wikipedia.org/wiki/Elo_rating_system) was developed by Arpad Elo originally to estimate the strength of chess players. Each player's elo rating is based on their prior results. When two chess players enter a match, the system can calculate the expected outcome using each player's rating and then updates each player's rating once the match has concluded. 

#### Mechanics and assumptions
- Match and player data comes from [Jeff Sackmann's ATP Results csv files](https://github.com/JeffSackmann/tennis_atp) 
- Each player starts with an elo rating of 1500
- The paramaeters of the K factor (determines the fluctuation of a player's rankings) comes from the recommendation of [FiveThirtyEight](http://fivethirtyeight.com/features/serena-williams-and-the-difference-between-all-time-great-and-greatest-of-all-time/#fn-2)

#### Top Ten Elo Ratings (as of September 2015)

| Rank | Player Name    | Peak Elo | Peak Elo Date |
| :--: | -------------  |:--------:| ------------- |
| 1    | Novak Djokovic | 2538     | 2015-05-24    |
| 2    | Roger Federer  | 2536     | 2007-02-26    |
| 3    | John McEnroe   | 2501     | 1985-04-01    |
| 4    | Rafael Nadal   | 2495     | 2013-09-30    |
| 5    | Bjorn Borg     | 2483     | 1980-08-11    |
| 6    | Ivan Lendl     | 2467     | 1986-03-24    |
| 7    | Boris Becker   | 2390     | 1990-03-05    |
| 8    | Andy Murray    | 2382     | 2009-04-12    |
| 9    | Pete Sampras   | 2381     | 1994-05-09    |
| 10   | Jimmy Connors  | 2372     | 1978-10-31    |

Taking these top ten players, we will then look at their respective elo ratings throughout their careers.

![alt tag](https://raw.githubusercontent.com/hdai/elo_tennis/master/historical_elo_rating.png)


