import os

# change directory 
os.chdir(r'C:\Users\Rodzinka\Desktop\siatka_23')

# import scrapping functions
from funs.scrapping import *

# import data preprocessing functions 
from funs.data_prep import *

# import function used for generating predictions 
from funs.predictions_warm_start import *

''' If you want to build the database from scratch, execute the whole code.'''

# this is to build a whole base database after whole season 
# get 'core' data from web
get_match_stats()

get_table_positions([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])

get_player_data()

get_additional_player_data() 

''' If you just want to refresh the database with latest results and calculate predictions, skip the lines above and execute lines below '''

# refresh data after each round
refresh_table_positions()

refresh_match_stats() 


# calculate statistics

calc_teams_place()

calc_players_averages() 

calc_table_stats_averages()  
 
calc_match_stats_averages()

create_final_database()


# generate results
generate_predictions()
