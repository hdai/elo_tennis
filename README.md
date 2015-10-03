## Historical ATP Ranking using the Elo rating system

After reading *FiveThirtyEight*'s piece about how [Serena Williams stacks up against all-time female greats](http://fivethirtyeight.com/features/serena-williams-and-the-difference-between-all-time-great-and-greatest-of-all-time/#fn-2) using the Elo rating system, I attempted to apply the same rating system to men's tennis.

> The [Elo Rating system](https://en.wikipedia.org/wiki/Elo_rating_system) was developed by Arpad Elo originally to estimate the strength of chess players. Each player's elo rating is based on their prior results. When two chess players enter a match, the system can calculate the expected outcome using each player's rating and then updates each player's rating once the match has concluded. 

#### Mechanics and assumptions
- Match and player data comes from [Jeff Sackmann's ATP Results csv files](https://github.com/JeffSackmann/tennis_atp) 
- Each player starts with an elo rating of 1500
- The paramaeters of the K factor (determines the fluctuation of a player's rankings) comes from the recommendation of [FiveThirtyEight](http://fivethirtyeight.com/features/serena-williams-and-the-difference-between-all-time-great-and-greatest-of-all-time/#fn-2)




