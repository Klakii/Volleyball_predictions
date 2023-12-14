import re
import pandas as pd
import numpy as np
import sqlite3
import os

# change directory 
os.chdir(r'C:\Users\Rodzinka\Desktop\siatka_23')


def calc_teams_place():
    
    print(".......Calculating team place after each season........")
    
    # define function for rolling mean calculation
    def rolling_diff(df, list_of_n):
        temp_df = pd.DataFrame()
        counter = 0
        for n in list_of_n:
            for column in df.columns[:7]:
                new_name = 'Last_' + str(n) + '_' + column
                temp_df[new_name] = df[column].rolling(window=n+1).apply(lambda x: x.iloc[-1] - x.iloc[0])
            for j in range(1, n):
                temp_df.iloc[j,counter:counter+7] = df.iloc[j,:7]
            counter = counter + 7
        temp_df["Round"] = df["Round"]
        temp_df['Year'] = df['Year']
        temp_df['Team_name'] = df['Team_name']
        return temp_df


    # import data from db 
    # define years 
    years = ['2010/2011','2011/2012','2012/2013','2013/2014','2014/2015','2015/2016','2016/2017','2017/2018',
            '2018/2019','2019/2020','2020/2021','2021/2022', '2022/2023', '2023/2024']

    # change team names to ones used in other notebooks 
    names = ['Aluron', 'AZS Częstochowa', 'Asseco', 'BBTS', 'Bydgoszcz', 'Kielce', 'Szczecin', 'Czarni', 'Lubin', 
            'Indykpol', 'GKS', 'Węgiel', 'Będzin', 'Wieluń',
            'Lublin', 'Skra', 'Warsza', 'Nysa', 'Suwałki', 'ZAKSA', 'Gdańsk', 'Hemarpol',
            'www']

    # create empty table for storing results
    tab = pd.DataFrame()

    # loop over all seasons
    for year in years:
        # read database, change path and database name if needed
        year_ = year.split('/')[0]  
        conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))
        cursor = conn.cursor()
        result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

        # find table names - match data
        table_names = sorted(list(zip(*result))[0])

        # create first table
        test_name = table_names[0]
        data = pd.read_sql("SELECT * FROM '{}'".format(test_name), conn)
        data['Round'] = test_name.split('_')[1]
        
        # append all match stats to one table
        for name in table_names[1:]:
            data_i = pd.read_sql("SELECT * FROM '{}'".format(name), conn)
            data_i['Round']= name.split('_')[1]
            # concatenate created table with whole data
            data = pd.concat([data, data_i])
        
        # change team name
        for name in names:
            data.iloc[:,1] = data.iloc[:,1].apply(lambda x: name if not pd.isnull(x) and name.lower() in x.lower() else x)

        # add year
        data['Year'] = year
        
        # concatenate results from each year
        tab = pd.concat([tab, data])
        


    # change data type in order to perform calculations
    tab['Round'] = pd.to_numeric(tab['Round'])

    # choose columns and change their names
    tab = tab.iloc[:, [2, 4, 5, 6, 7, 8, 9, 18, 19, 1]]
    tab.columns = ['Points', 'Matches_won', 'Matches_lost', 'Sets_won', 'Sets_lost', 'Points_won', 'Points_lost',
                    'Round','Year', 'Team_name']

    # round data
    tab = tab.round(2)


    tab['Round'] = tab['Round'] + 1

    # save results to db
    conn21 = sqlite3.connect('data/database_rounds_prepared.db')
    tab.to_sql("Rounds_prep", conn21, if_exists='replace', index=False)   

    tab['Round'] = tab['Round'] - 1

    # create empty table for storing the results
    final = pd.DataFrame()

    # define years 
    years = ['2010/2011','2011/2012','2012/2013','2013/2014','2014/2015','2015/2016','2016/2017','2017/2018',
            '2018/2019','2019/2020','2020/2021','2021/2022', '2022/2023', '2023/2024']

    # define team names
    names = ['Aluron', 'AZS Częstochowa', 'Asseco', 'BBTS', 'Bydgoszcz', 'Kielce', 'Szczecin', 'Czarni', 'Lubin', 
            'Indykpol', 'GKS', 'Węgiel', 'Będzin', 'Wieluń',
            'Lublin', 'Skra', 'Warsza', 'Nysa', 'Suwałki', 'ZAKSA', 'Gdańsk', 'Hemarpol',
            'www']

    for year in years:
        for name in names:

            temp_ = tab[tab['Team_name']==name]
            temp_ = temp_[temp_['Year']==year]
            temp_ = temp_.sort_values(by=['Round']).reset_index(drop=True)
            
            if temp_.empty:
                print(year, name, 'Could not retrieve data for rounds - {0} was not playing in Plusliga in {1} season'.format(name, year))

                
            else:
                temp_.iloc[-1] = temp_.iloc[0]  # adding a row - there is no reliable data for macthes played during the first round of the season 
                temp_.iloc[-1, 7] = 0
                temp_ = temp_.sort_values(by=['Round'])
                temp_.iloc[0, :7] = 0
                temp_ = temp_.reset_index(drop=True) 
                
                # calculate rolling differences
                temp_ = rolling_diff(temp_, [1, 3, 5])
                
                # increase round number in order to prevent data leakage
                temp_['Round'] += 1

                final = pd.concat([final, temp_])
                print(year, name)

    # save created data as sql
    conn3 = sqlite3.connect('data/database_rounds_averages_all_teams.db')
    final.to_sql("Rounds", conn3, if_exists='replace', index=False)   

    # close connection
    cursor.close() 
    conn.close()
    conn3.close()
    



def calc_players_averages():
    
    print('.......Calculating players averages for each season..........')
    
    # read database, change path and database name if needed
    conn = sqlite3.connect('data/database_players_allteams.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names
    table_names = sorted(list(zip(*result))[0])

    # define teams' names
    names = ['Aluron', 'AZS Częstochowa', 'Asseco', 'BBTS', 'Bydgoszcz', 'Kielce', 'Szczecin', 'Czarni', 'Lubin', 
            'Indykpol', 'GKS', 'Węgiel', 'Będzin', 'Wieluń',
            'Lublin', 'Skra', 'Warsza', 'Nysa', 'Suwałki', 'ZAKSA', 'Gdańsk', 'Hermapol',
            'test']

    # define years
    years = ['2023/2024', '2022/2023', '2021/2022', '2020/2021', '2019/2020', '2018/2019', '2017/2018', '2016/2017', '2015/2016', '2014/2015', '2013/2014', 
            '2012/2013', '2011/2012', '2010/2011']

    # create final table
    tab = pd.DataFrame(columns=['Height_avg', 'Weight_avg', 'Range_avg', 'Atakujący_Height',
                    'Libero_Height', 'Przyjmujący_Height', 'Rozgrywający_Height',
                    'Środkowy_Height', 'Atakujący_Weight', 'Libero_Weight',
                    'Przyjmujący_Weight', 'Rozgrywający_Weight', 'Środkowy_Weight',
                    'Atakujący_Range', 'Libero_Range', 'Przyjmujący_Range',
                    'Rozgrywający_Range', 'Środkowy_Range', 'Team_name', 'Year'])

    for year in  years:
        for name in names: 
            
            # list for storing table names
            names_players = []
            for table_name in table_names:
                
                if table_name.find(year) != -1:
                    if table_name.lower().find(name.lower())!= -1:
                        names_players.append(table_name)

            if not names_players:
                continue           
            else:
                #print(names_players)

                # get results for each round
                for name_tab in names_players:
                    # read table
                    data = pd.read_sql("SELECT * FROM '{}'".format(name_tab), conn)
                    
                    # average for all players
                    data = data.apply(pd.to_numeric, errors='ignore')
                    data_temp = data[['Height', 'Weight', 'Range']].mean(axis=0)
                    temp = [round(w, 2) for w in data_temp]
                    average = pd.DataFrame(columns = ['Height_avg', 'Weight_avg', 'Range_avg'])
                    
                    average = pd.concat([average, pd.DataFrame([temp], columns=['Height_avg', 'Weight_avg', 'Range_avg'])], ignore_index=False)
                    average = average.reset_index(drop=True)
                    
                    # average for each position
                    try:
                        by_position = data.groupby("Position").mean().round(2)
                        by_position=by_position.reset_index()

                        # change data format to wide
                        df_long = pd.melt(by_position, id_vars=['Position'])

                        # transpose data
                        transpose = df_long.T

                        # create unique column names
                        transpose.loc['name'] = transpose.loc['Position'] + '_' + transpose.loc['variable']
                        transpose.drop('Position', inplace=True)
                        transpose.drop('variable', inplace=True)
                        transpose.columns = transpose.iloc[1]
                        transpose.drop('name', inplace=True)
                        transpose = transpose.reset_index(drop=True)
                        
                        # merge created tables
                        data_f = pd.concat([average, transpose], axis=1)
                        data_f['Team_name'] = name
                        data_f['Year'] = year
                        
                        # append results to final table
                        tab = pd.concat([tab, data_f], ignore_index=True)
                        
                    except:
                        print(name_tab, 'Could not retrieve data for players')
                        pass
            

    # remove unnecessary columns 
    tab_final = tab.iloc[:,:-3]

    # create database for new data
    conn3 = sqlite3.connect('data/database_players_averages_all_teams.db')
    tab_final.to_sql("Players_prepared", conn3, if_exists='replace', index=False)   

    # close connection
    cursor.close() 
    conn.close()
    conn3.close()
    


def calc_match_stats_averages():
    
    print('........Calculating match statistics for each team in every season..........')

    # create function for calculating rolling averages
    def rolling_mean(df, list_of_n):
        df2 = pd.DataFrame()
        for n in list_of_n:
            for column in df.columns[:15]:
                new_name = 'AVG_' + str(n) + '_' + column
                df2[new_name] = df[column].rolling(n, min_periods = 1, closed='left').mean().round(2)
        df2["ID"] = df["ID"]
        df2['Team_name'] = df['Team_name']
        df2['Year'] = df['Year']
        df2['Round'] = df['Round']
        df2['Results'] = df['Result']
        df2['Date'] = df['Date']
        return df2


    # read database, change path and database name if needed
    conn = sqlite3.connect('data/database_matches_all.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names
    table_names = sorted(list(zip(*result))[0])

    # define teams' names
    names = ['Aluron', 'Częstochowa', 'Asseco', 'BBTS', 'Bydgoszcz', 'Kielce', 'Szczecin', 'Czarni', 'Lubin', 
            'Indykpol', 'GKS', 'Węgiel', 'Będzin', 'Wieluń',
            'Lublin', 'Skra', 'Warsza', 'Nysa', 'Suwałki', 'ZAKSA', 'Gdańsk', 
            'www']


    # import net differences in points
    conn99 = sqlite3.connect('data/database_matches_net_difference_small_points.db')
    cursor99 = conn99.cursor()
    result99 = cursor99.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names - match data
    table_names_hh = sorted(list(zip(*result99))[0])

    # save data to one table
    test_name_hh = table_names_hh[0]
    data_points = pd.read_sql("SELECT * FROM '{}'".format(test_name_hh), conn99)
    data_points

    # create database for new data
    conn2 = sqlite3.connect('data/database_matches_averages.db')

    # data from seasons 2021/2022 and 2020/2021 looks a little bit different than from all other seasons, 
    # thus two version of the code are needed

    # define years
    years = ['2023/2024','2022/2023','2021/2022', '2020/2021']

    for year in years:
        for name in names: 
            
            # list for storing table names
            names_2021 = []
            
            for table_name in table_names:
                if table_name.find(year) != -1:
                    if table_name.lower().find(name.lower())!= -1:
                        names_2021.append(table_name)
                        
            if not names_2021:
                continue 
                
            else:
                # sort table names
                names_2021.sort(key = lambda x: int(x.split(' ')[-1]))

                # create final table
                tab = pd.DataFrame(columns=["Points", "Serve_number", "Serve_errors", "Serve_aces", 
                                "Serve_%_effic", "Rec_number", "Rec_errors", "Rec_%_pos",
                                "Rec_%_perf", "Atack_number", "Atack_error", "Atack_blocked",
                                "Atack_%_eff", "Block_points", "ID", "Team_name", "Round", "Year", "Result", "Date"])

                # get results for each round
                for name_tab in names_2021:
                    data = pd.read_sql("SELECT * FROM '{}'".format(name_tab), conn)
                    data2 = data.iloc[-1:]
                    data_f = pd.concat([data2.iloc[:,6], data2.iloc[:, 9:21], data2.iloc[:, 23], data2.iloc[:, -1:]], axis = 1)
                    data_f.columns = ["Points", "Serve_number", "Serve_errors", "Serve_aces", 
                                        "Serve_%_effic", "Rec_number", "Rec_errors", "Rec_%_pos",
                                        "Rec_%_perf", "Atack_number", "Atack_error", "Atack_blocked",
                                        "Atack_%_eff", "Block_points", "ID"]
                    data_f['Team_name'] = name
                    data_f['Round'] = name_tab.split(' ')[-1]
                    data_f['Year'] = year
                    data_f['Date'] = data2.iloc[:,-2]
                    
                    # away win = 4, away loose = 5, home win = 1, home loose = 0
                    if data2.columns[-3].find('Home')!=-1:
                        data_f['Result'] = data2.iloc[:, -3]
                    else:
                        if data2.iloc[:, -3].any()==1:
                            data_f['Result'] = 4
                        else:
                            data_f['Result'] = 5
                    
                    # append results to final table
                    tab = pd.concat([tab, data_f])

                # remove % signs
                tab['Serve_%_effic'] = tab['Serve_%_effic'].str.replace('%','')
                tab['Rec_%_pos'] = tab['Rec_%_pos'].str.replace('%','')
                tab['Rec_%_perf'] = tab['Rec_%_perf'].str.replace('%','')
                try:
                    tab['Atack_%_eff'] = tab['Atack_%_eff'].str.replace('%','')
                except:
                    pass
            
                # convert all values to numeric
                tab = tab.apply(pd.to_numeric, errors='ignore')
                
                # merge net_points with tab table
                tab = pd.merge(tab, data_points, on=["Year", "ID", "Round", "Team_name"])
                
                # change columns order
                cols = tab.columns.tolist()
                cols = cols[:-7] + cols[-1:] + cols[-7:-1]
                tab = tab[cols]
                
                # sort tables by date in order to calculate rolling means
                tab['Date'] = pd.to_datetime(tab['Date'], format="%d.%m.%Y")
                tab = tab.sort_values(by='Date')   

                # calculate rolling means
                mean_stats = rolling_mean(tab, [1,3,5])
                
                # define key - table name
                key = year + ' ' + name 
                print(key)
                
                # Save created data to sql database
                mean_stats.to_sql(key, conn2, if_exists='replace', index=False)     
                
    # define years
    years = ['2019/2020', '2018/2019', '2017/2018', '2016/2017', '2015/2016', '2014/2015', '2013/2014', 
            '2012/2013', '2011/2012', '2010/2011']

    for year in years:
        for name in names: 
            
            # list for storing table names
            names_2021 = []
            
            for table_name in table_names:
                if table_name.find(year) != -1:
                    if table_name.lower().find(name.lower())!= -1:
                        names_2021.append(table_name)
                        
            if not names_2021:
                continue 
                
            else:

                # sort table names
                names_2021.sort(key = lambda x: int(x.split(' ')[-1]))
                
                # create final table
                tab = pd.DataFrame(columns=["Points", "Serve_number", "Serve_errors", "Serve_aces", 
                                "Serve_%_effic", "Rec_number", "Rec_errors", "Rec_%_pos",
                                "Rec_%_perf", "Atack_number", "Atack_error", "Atack_blocked",
                                "Atack_%_eff", "Block_points", "ID", "Team_name", "Year", "Round", "Date"])

                # get results for each round
                for name_tab in names_2021:
                    data = pd.read_sql("SELECT * FROM '{}'".format(name_tab), conn)
                    
                    data2 = data.iloc[-1:]            
                    data_f = pd.concat([data2.iloc[:, 6], data2.iloc[:, 7], data2.iloc[:, 9], data2.iloc[:, 8], 
                                        data2.iloc[:, 10], data2.iloc[:, 11], data2.iloc[:, 12], data2.iloc[:, 15],
                                        data2.iloc[:, 17], data2.iloc[:, 18], data2.iloc[:, 19], data2.iloc[:, 20], 
                                        data2.iloc[:, 22], data2.iloc[:, 23], data2.iloc[:, -1:]], axis = 1)

                    data_f.columns = ["Points", "Serve_number", "Serve_errors", "Serve_aces", 
                                    "Serve_%_effic", "Rec_number", "Rec_errors", "Rec_%_pos",
                                    "Rec_%_perf", "Atack_number", "Atack_error", "Atack_blocked",
                                    "Atack_%_eff", "Block_points", "ID"]

                    data_f['Team_name'] = name
                    data_f['Year'] = year
                    data_f['Round'] = name_tab.split(' ')[-1]
                    data_f["Serve_%_effic"] = (data_f["Serve_aces"] - data_f["Serve_errors"])/data_f["Serve_number"]
                    data_f['Date'] = data2.iloc[:,-2]
                    
                    # away win = 4, away loose = 5, home win = 1, home loose = 0
                    if data2.columns[-3].find('Home')!=-1:
                        data_f['Result'] = data2.iloc[:, -3]
                    else:
                        if data2.iloc[:, -3].any()==1:
                            data_f['Result'] = 4
                        else:
                            data_f['Result'] = 5            
                    
                    # append results to final table
                    tab = pd.concat([tab, data_f])
                                
                # remove % signs
                try:
                    tab['Serve_%_effic'] = tab['Serve_%_effic'].str.replace('%','')
                except:
                    pass
                
                try:
                    tab['Rec_%_pos'] = tab['Rec_%_pos'].str.replace('%','')
                except:
                    pass
                
                try:
                    tab['Rec_%_perf'] = tab['Rec_%_perf'].str.replace('%','')
                except:
                    pass
                
                try:
                    tab['Atack_%_eff'] = tab['Atack_%_eff'].str.replace('%','')
                except:
                    pass            

                # convert all values to numeric
                tab = tab.apply(pd.to_numeric, errors='ignore')
                
                # merge net_points with tab table
                tab = pd.merge(tab, data_points, on=["Year", "ID", "Round", "Team_name"])
                
                # change columns order
                cols = tab.columns.tolist()
                cols = cols[:-7] + cols[-1:] + cols[-7:-1]
                tab = tab[cols]

                # sort tables by date in order to calculate rolling means
                tab['Date'] = pd.to_datetime(tab['Date'], format="%d.%m.%Y")
                tab = tab.sort_values(by='Date')   
                
                # calculate rolling means
                mean_stats = rolling_mean(tab, [1,3,5])

                # define key - table name
                key = year + ' ' + name 
                print(key)
                
                # Save created data to sql database
                mean_stats.to_sql(key, conn2, if_exists='replace', index=False)        
                
    # close connection
    cursor.close()
    cursor99.close()
    conn.close()
    conn99.close()
    


def calc_table_stats_averages():
    print('......Calculating averaged table stastistics.......')


    # read database, change path and database name if needed
    conn = sqlite3.connect('data/database_matches_all.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names
    table_names = sorted(list(zip(*result))[0])

    # define teams' names
    names = ['Aluron', 'AZS Częstochowa', 'Asseco', 'BBTS', 'Bydgoszcz', 'Kielce', 'Szczecin', 'Czarni', 'Lubin', 
            'Indykpol', 'GKS', 'Węgiel', 'Będzin', 'Wieluń',
            'Lublin', 'Skra', 'Warsza', 'Nysa', 'Suwałki', 'ZAKSA', 'Gdańsk', 'Hermapol',
            'www']

    # create database for new data
    conn45 = sqlite3.connect('data/database_matches_stats_aggregated.db')

    # due to differences in scrapped data for newer and older seasons, there are seperate code chunks for both 

    # define years
    years = ['2023/2024', '2022/2023', '2021/2022', '2020/2021']

    for year in years:
        for name in names: 
            
            # list for storing table names
            names_2021 = []
            
            for table_name in table_names:
                if table_name.find(year) != -1:
                    if table_name.lower().find(name.lower())!= -1:
                        names_2021.append(table_name)
                        
            if not names_2021:
                continue 
                
            else:
                # sort table names
                names_2021.sort(key = lambda x: int(x.split(' ')[-1]))

                # create final table
                tab = pd.DataFrame(columns=["Points", "Serve_number", "Serve_errors", "Serve_aces", 
                                "Serve_%_effic", "Rec_number", "Rec_errors", "Rec_%_pos",
                                "Rec_%_perf", "Atack_number", "Atack_error", "Atack_blocked",
                                "Atack_%_eff", "Block_points", "ID", "Team_name", "Round", "Year", "Result"])

                # get results for each round
                for name_tab in names_2021:
                    data = pd.read_sql("SELECT * FROM '{}'".format(name_tab), conn)
                    data2 = data.iloc[-1:]
                    data_f = pd.concat([data2.iloc[:,6], data2.iloc[:, 9:21], data2.iloc[:, 23], data2.iloc[:, -1:]], axis = 1)
                    data_f.columns = ["Points", "Serve_number", "Serve_errors", "Serve_aces", 
                                        "Serve_%_effic", "Rec_number", "Rec_errors", "Rec_%_pos",
                                        "Rec_%_perf", "Atack_number", "Atack_error", "Atack_blocked",
                                        "Atack_%_eff", "Block_points", "ID"]
                    data_f['Team_name'] = name
                    data_f['Round'] = name_tab.split(' ')[-1]
                    data_f['Year'] = year
                    
                    # away win = 4, away loose = 5, home win = 1, home loose = 0
                    if data2.columns[-3].find('Home')!=-1:
                        data_f['Result'] = data2.iloc[:, -3]
                    else:
                        if data2.iloc[:, -3].any()==1:
                            data_f['Result'] = 4
                        else:
                            data_f['Result'] = 5
                    
                    # append results to final table
                    tab = pd.concat([tab, data_f], ignore_index=True)

                
                # remove % signs
                try:
                    tab['Serve_%_effic'] = tab['Serve_%_effic'].str.replace('%','')
                    tab['Rec_%_pos'] = tab['Rec_%_pos'].str.replace('%','')
                    tab['Rec_%_perf'] = tab['Rec_%_perf'].str.replace('%','')   
                    tab['Atack_%_eff'] = tab['Atack_%_eff'].str.replace('%','')
                except:
                    pass
                
                # for matches that have not been played yet, fill null values with 0's    
                tab.fillna(0, inplace=True)
                
                # convert all values to numeric
                tab = tab.apply(pd.to_numeric, errors='ignore')
                
                # define key - table name
                key = year + ' ' + name 
                print(key)
                
                # Save created data to sql database
                tab.to_sql(key, conn45, if_exists='replace', index=False)      
                
    # define years
    years = ['2019/2020', '2018/2019', '2017/2018', '2016/2017', '2015/2016', '2014/2015', '2013/2014', 
            '2012/2013', '2011/2012', '2010/2011']

    for year in years:
        for name in names: 
            
            # list for storing table names
            names_2021 = []
            
            for table_name in table_names:
                if table_name.find(year) != -1:
                    if table_name.lower().find(name.lower())!= -1:
                        names_2021.append(table_name)
                        
            if not names_2021:
                continue 
                
            else:

                # sort table names
                names_2021.sort(key = lambda x: int(x.split(' ')[-1]))
                
                # create final table
                tab = pd.DataFrame(columns=["Points", "Serve_number", "Serve_errors", "Serve_aces", 
                                "Serve_%_effic", "Rec_number", "Rec_errors", "Rec_%_pos",
                                "Rec_%_perf", "Atack_number", "Atack_error", "Atack_blocked",
                                "Atack_%_eff", "Block_points", "ID", "Team_name", "Year", "Round"])

                # get results for each round
                for name_tab in names_2021:
                    data = pd.read_sql("SELECT * FROM '{}'".format(name_tab), conn)
                    
                    data2 = data.iloc[-1:]            
                    data_f = pd.concat([data2.iloc[:, 6], data2.iloc[:, 7], data2.iloc[:, 9], data2.iloc[:, 8], 
                                        data2.iloc[:, 10], data2.iloc[:, 11], data2.iloc[:, 12], data2.iloc[:, 15],
                                        data2.iloc[:, 17], data2.iloc[:, 18], data2.iloc[:, 19], data2.iloc[:, 20], 
                                        data2.iloc[:, 22], data2.iloc[:, 23], data2.iloc[:, -1:]], axis = 1)

                    data_f.columns = ["Points", "Serve_number", "Serve_errors", "Serve_aces", 
                                    "Serve_%_effic", "Rec_number", "Rec_errors", "Rec_%_pos",
                                    "Rec_%_perf", "Atack_number", "Atack_error", "Atack_blocked",
                                    "Atack_%_eff", "Block_points", "ID"]

                    data_f['Team_name'] = name
                    data_f['Year'] = year
                    data_f['Round'] = name_tab.split(' ')[-1]
                    data_f["Serve_%_effic"] = (data_f["Serve_aces"] - data_f["Serve_errors"])/data_f["Serve_number"]
                    
                    # away win = 4, away loose = 5, home win = 1, home loose = 0
                    if data2.columns[-3].find('Home')!=-1:
                        data_f['Result'] = data2.iloc[:, -3]
                    else:
                        if data2.iloc[:, -3].any()==1:
                            data_f['Result'] = 4
                        else:
                            data_f['Result'] = 5       
                                    
                    # append results to final table
                    tab = pd.concat([tab, data_f], ignore_index=True)
                                
                # remove % signs
                try:
                    tab['Serve_%_effic'] = tab['Serve_%_effic'].str.replace('%','')
                except:
                    pass
                
                try:
                    tab['Rec_%_pos'] = tab['Rec_%_pos'].str.replace('%','')
                except:
                    pass
                
                try:
                    tab['Rec_%_perf'] = tab['Rec_%_perf'].str.replace('%','')
                except:
                    pass
                
                try:
                    tab['Atack_%_eff'] = tab['Atack_%_eff'].str.replace('%','')
                except:
                    pass    
                
                # for matches that have not been played yet, fill null values with 0's    
                tab.fillna(0, inplace=True)        

                # convert all values to numeric
                tab = tab.apply(pd.to_numeric, errors='ignore')

                # define key - table name
                key = year + ' ' + name 
                print(key)
                
                # Save created data to sql database
                tab.to_sql(key, conn45, if_exists='replace', index=False)     

    # close connection
    cursor.close() 
    conn.close()
    conn45.close()

    # matches data
    conn3 = sqlite3.connect('data/database_matches_stats_aggregated.db')
    cursor = conn3.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names - match data
    table_names = sorted(list(zip(*result))[0])

    # create first table
    test_name = table_names[0]
    data = pd.read_sql("SELECT * FROM '{}'".format(test_name), conn3)

    # append all match stats to one table
    for name in table_names[1:]:
        data_i = pd.read_sql("SELECT * FROM '{}'".format(name), conn3)
        data = pd.concat([data, data_i])

    # create first table
    temp = data[data['ID']==0]

    print('......Calculating difference in table points for each match......')
    
    # home
    home = temp.loc[temp['Result'].isin([0, 1])]
    home = home.reset_index(drop=True)
    # away
    away = temp.loc[temp['Result'].isin([4, 5])]
    away = away.reset_index(drop=True)

    # points scored by both teams and difference between them 
    home = pd.concat([home.iloc[:, 0], home.iloc[:, -5:]], axis = 1)

    away = pd.concat([away.iloc[:, 0], away.iloc[:, -5:]], axis = 1)

    away = pd.concat([away.iloc[:, 0], away.iloc[:, -5:]], axis = 1)
    together = pd.merge(home, away, on=["Year", "ID", "Round"], suffixes=('_home', '_away'))
    together['difference_home'] = together['Points_home'] - together['Points_away']
    together['difference_away'] = together['Points_away'] - together['Points_home']

    # define new table 
    rrr = pd.DataFrame(columns=["Points_net", "ID", "Team_name", "Year", "Round"])

    # results for home team
    data_h = pd.concat([together.iloc[:, -2], together.iloc[:,1:5]], axis = 1)
    data_h.columns = ["Points_net", "ID", "Team_name", "Year", "Round"]

    # results for away team
    data_a = pd.concat([together.iloc[:, -1], together.iloc[:,1], together.iloc[:,7], together.iloc[:, 3:5]], axis = 1)
    data_a.columns = ["Points_net", "ID", "Team_name", "Year", "Round"]

    # append results
    rrr = pd.concat([rrr, data_h], axis = 0)
    rrr = pd.concat([rrr, data_a], ignore_index=True)

    # append all results
    for i in range(1, len(data)): # 4458    
        # find results for both teams competing
        temp = data[data['ID']==i]

        # home
        home = temp.loc[temp['Result'].isin([0, 1])]
        home = home.reset_index(drop=True)

        # away
        away = temp.loc[temp['Result'].isin([4, 5])]
        away = away.reset_index(drop=True)

        # points scored by both teams and difference between them 
        home = pd.concat([home.iloc[:, 0], home.iloc[:, -5:]], axis = 1)

        away = pd.concat([away.iloc[:, 0], away.iloc[:, -5:]], axis = 1)

        away = pd.concat([away.iloc[:, 0], away.iloc[:, -5:]], axis = 1)

        together = pd.merge(home, away, on=["Year", "ID", "Round"], suffixes=('_home', '_away'))
        together['difference_home'] = together['Points_home'] - together['Points_away']
        together['difference_away'] = together['Points_away'] - together['Points_home']

        # results for home team
        data_h = pd.concat([together.iloc[:, -2], together.iloc[:,1:5]], axis = 1)
        data_h.columns = ["Points_net", "ID", "Team_name", "Year", "Round"]

        # results for away team
        data_a = pd.concat([together.iloc[:, -1], together.iloc[:,1], together.iloc[:,7], together.iloc[:, 3:5]], axis = 1)
        data_a.columns = ["Points_net", "ID", "Team_name", "Year", "Round"]

        # append results
        rrr = pd.concat([rrr, data_h], axis = 0)
        rrr = pd.concat([rrr, data_a], ignore_index=True)
        

    # create database for new data
    conn3 = sqlite3.connect('data/database_matches_net_difference_small_points.db')
    rrr.to_sql("M", conn3, if_exists='replace', index=False)   

    # close connection
    cursor.close() 
    conn.close()
    conn3.close()






def create_final_database():
    print('......Creating final database......')

    # matches data
    conn = sqlite3.connect('data/database_matches_averages.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names - match data
    table_names = sorted(list(zip(*result))[0])

    # create first table
    test_name = table_names[0]
    data = pd.read_sql("SELECT * FROM '{}'".format(test_name), conn)

    # append all match stats to one table
    for name in table_names[1:]:
        data_i = pd.read_sql("SELECT * FROM '{}'".format(name), conn)
        data = pd.concat([data, data_i])

    # remove column with date
    data.pop("Date")


    # player data
    # read database
    conn6 = sqlite3.connect('data/database_players_averages_all_teams.db')
    cursor2 = conn6.cursor()
    result2 = cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names
    table_names_p = sorted(list(zip(*result2))[0])

    # create first table
    test_name_p = table_names_p[0]
    data_p = pd.read_sql("SELECT * FROM '{}'".format(test_name_p), conn6)

    # append all stats to one table
    for name in table_names_p[1:]:
        data_l = pd.read_sql("SELECT * FROM '{}'".format(name), conn6)
        data_p = pd.concat([data_p, data_l])


    # rounds data
    # read database
    conn8 = sqlite3.connect('data/database_rounds_prepared.db')
    cursor8 = conn8.cursor()
    result3 = cursor8.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names
    table_names_r = sorted(list(zip(*result3))[0])

    # create first table
    test_name_r = table_names_r[0]
    data_r = pd.read_sql("SELECT * FROM '{}'".format(test_name_r), conn8)

    # append all stats to one table
    for name in table_names_r[1:]:
        data_h = pd.read_sql("SELECT * FROM '{}'".format(name), conn8)
        data_r = pd.concat([data_r, data_h])


    # rounds averages data
    # read database
    conn10 = sqlite3.connect('data/database_rounds_averages_all_teams.db')
    cursor10 = conn10.cursor()
    result10 = cursor10.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names
    table_names_a = sorted(list(zip(*result10))[0])

    # create first table
    test_name_a = table_names_a[0]
    data_a = pd.read_sql("SELECT * FROM '{}'".format(test_name_a), conn10)

    # append all stats to one table
    for name in table_names_a[1:]:
        data_n = pd.read_sql("SELECT * FROM '{}'".format(name), conn10)
        data_a = pd.concat([data_a, data_n])


    # create first table
    temp = data[data['ID']==0]

    # convert data to numeric
    temp = temp.apply(pd.to_numeric, errors='ignore')
    data_p = data_p.apply(pd.to_numeric, errors='ignore')
    data_r = data_r.apply(pd.to_numeric, errors='ignore')

    # prepare match and players data
    temp_p = pd.merge(temp, data_p, on=["Year", "Team_name"])
    cols = temp_p.columns.tolist()
    cols = cols[:45] + cols[50:] + cols[45:50]
    temp_p = temp_p[cols]

    # home
    home = temp_p.loc[temp_p['Results'].isin([0, 1])]
    home = home.reset_index(drop=True)

    # away
    away = temp_p.loc[temp_p['Results'].isin([4, 5])]
    away = away.reset_index(drop=True)

    # difference between home and away team
    difff = home.iloc[:, :-5] - away.iloc[:, :-5]
    difff.columns = difff.columns + '_diff'
    difff['ID'] = temp.iloc[0, -5]

    # merge stats for both teams and differences together
    result2 = pd.merge(home, away, on="ID", suffixes=('_home', '_away'))
    data_merged = pd.merge(result2, difff, on="ID", suffixes=('_eee', '_diff'))

    # append all results
    for i in range(len(data)): # len(data)
    
        # find results for both teams competing
        temp = data[data['ID']==i]

        # change columns only if data frame is not empty
        if not temp.empty:
            # convert data to numeric
            temp = temp.apply(pd.to_numeric, errors='ignore')
            data_p = data_p.apply(pd.to_numeric, errors='ignore')
            data_r = data_r.apply(pd.to_numeric, errors='ignore')

            # prepare match and players data
            temp_p = pd.merge(temp, data_p, on=["Year", "Team_name"])
            cols = temp_p.columns.tolist()
            cols = cols[:45] + cols[50:] + cols[45:50]
            temp_p = temp_p[cols]

            # home
            home = temp_p.loc[temp_p['Results'].isin([0, 1])]
            home = home.reset_index(drop=True)

            # away
            away = temp_p.loc[temp_p['Results'].isin([4, 5])]
            away = away.reset_index(drop=True)

            # difference between home and away team
            difff = home.iloc[:, :-5] - away.iloc[:, :-5]
            difff.columns = difff.columns + '_diff'
            difff['ID'] = temp.iloc[0, -5]

            # merge stats for both teams and differences together
            result2 = pd.merge(home, away, on="ID", suffixes=('_home', '_away'))
            result3 = pd.merge(result2, difff, on="ID", suffixes=('_eee', '_diff'))


            data_merged = pd.concat([data_merged, result3], ignore_index=True)


    # create first table
    temp = data[data['ID']==10]

    # convert data to numeric
    temp = temp.apply(pd.to_numeric, errors='ignore')
    data_p = data_p.apply(pd.to_numeric, errors='ignore')

    # prepare players data
    temp_p = pd.merge(temp, data_p, on=["Year", "Team_name"])
    cols = temp_p.columns.tolist()
    cols = cols[:45] + cols[50:] + cols[45:50]
    temp_p = temp_p[cols]

    # prepare match, players and rounds data
    temp_r = pd.merge(temp_p, data_r, on=["Year", "Team_name", "Round"])
    cols2 = temp_r.columns.tolist()
    cols2 = cols2[:63] + cols2[68:] + cols2[63:68]
    temp_r = temp_r[cols2]

    # prepare match, players, rounds and rounds averages data
    temp_a = pd.merge(temp_r, data_a, on=["Year", "Team_name", "Round"])
    cols3 = temp_a.columns.tolist()
    cols3 = cols3[:70] + cols3[75:] + cols3[70:75]
    temp_a = temp_a[cols3]

    # home
    home = temp_a.loc[temp_a['Results'].isin([0, 1])]
    home = home.reset_index(drop=True)

    # away
    away = temp_a.loc[temp_a['Results'].isin([4, 5])]
    away = away.reset_index(drop=True)

    # difference between home and away team
    difff = home.iloc[:, :-5] - away.iloc[:, :-5]
    difff.columns = difff.columns + '_diff'
    difff['ID'] = temp.iloc[0, -5]

    # merge stats for both teams and differences together
    result2 = pd.merge(home, away, on="ID", suffixes=('_home', '_away'))
    data_merged = pd.merge(result2, difff, on="ID", suffixes=('_eee', '_diff'))
    data_merged.columns.to_list()



    # create first table
    temp = data[data['ID']==10]

    # convert data to numeric
    temp = temp.apply(pd.to_numeric, errors='ignore')
    data_p = data_p.apply(pd.to_numeric, errors='ignore')

    # prepare players data
    temp_p = pd.merge(temp, data_p, on=["Year", "Team_name"])
    cols = temp_p.columns.tolist()
    cols = cols[:45] + cols[50:] + cols[45:50]
    temp_p = temp_p[cols]

    # prepare match, players and rounds data
    temp_r = pd.merge(temp_p, data_r, on=["Year", "Team_name", "Round"])
    cols2 = temp_r.columns.tolist()
    cols2 = cols2[:63] + cols2[68:] + cols2[63:68]
    temp_r = temp_r[cols2]

    # prepare match, players, rounds and rounds averages data
    temp_a = pd.merge(temp_r, data_a, on=["Year", "Team_name", "Round"])
    cols3 = temp_a.columns.tolist()
    cols3 = cols3[:70] + cols3[75:] + cols3[70:75]
    temp_a = temp_a[cols3]

    # home
    home = temp_a.loc[temp_a['Results'].isin([0, 1])]
    home = home.reset_index(drop=True)

    # away
    away = temp_a.loc[temp_a['Results'].isin([4, 5])]
    away = away.reset_index(drop=True)

    # difference between home and away team
    difff = home.iloc[:, :-5] - away.iloc[:, :-5]
    difff.columns = difff.columns + '_diff'
    difff['ID'] = temp.iloc[0, -5]

    # merge stats for both teams and differences together
    result2 = pd.merge(home, away, on="ID", suffixes=('_home', '_away'))
    data_merged = pd.merge(result2, difff, on="ID", suffixes=('_eee', '_diff'))
    data_merged.columns.tolist()

    # append all results
    for i in range(len(data)): # len(data)
    
        # find results for both teams competing
        temp = data[data['ID']==i]

        if not temp.empty:
            # convert data to numeric
            temp = temp.apply(pd.to_numeric, errors='ignore')
            data_p = data_p.apply(pd.to_numeric, errors='ignore')

            # prepare players data
            temp_p = pd.merge(temp, data_p, on=["Year", "Team_name"])
            cols = temp_p.columns.tolist()
            cols = cols[:45] + cols[50:] + cols[45:50]
            temp_p = temp_p[cols]

            # prepare match, players and rounds data
            temp_r = pd.merge(temp_p, data_r, on=["Year", "Team_name", "Round"])
            cols2 = temp_r.columns.tolist()
            cols2 = cols2[:63] + cols2[68:] + cols2[63:68]
            temp_r = temp_r[cols2]

            # prepare match, players, rounds and rounds averages data
            temp_a = pd.merge(temp_r, data_a, on=["Year", "Team_name", "Round"])
            cols3 = temp_a.columns.tolist()
            cols3 = cols3[:70] + cols3[75:] + cols3[70:75]
            temp_a = temp_a[cols3]

            # home
            home = temp_a.loc[temp_a['Results'].isin([0, 1])]
            home = home.reset_index(drop=True)

            # away
            away = temp_a.loc[temp_a['Results'].isin([4, 5])]
            away = away.reset_index(drop=True)

            # difference between home and away team
            difff = home.iloc[:, :-5] - away.iloc[:, :-5]
            difff.columns = difff.columns + '_diff'
            difff['ID'] = temp.iloc[0, -5]

            # merge stats for both teams and difference together
            result2 = pd.merge(home, away, on="ID", suffixes=('_home', '_away'))
            result3 = pd.merge(result2, difff, on="ID", suffixes=('_eee', '_diff'))

            data_merged = pd.concat([data_merged, result3])
        
    data_merged['%_points_poss_home'] = data_merged['Points_home'] / (3*data_merged['Round_home'])

    data_merged['%_points_poss_away'] = data_merged['Points_away'] / (3*data_merged['Round_away'])

    data_merged[['Points_home', 'Round_home', '%_points_poss_home', 'Points_away', 'Round_away', '%_points_poss_away']]

    data_merged = data_merged.round(2)

    # create database for new data
    conn3 = sqlite3.connect('data/final_database.db')
    data_merged.to_sql("Merged_m_p", conn3, if_exists='replace', index=False)   

    # close connection
    cursor.close() 
    conn.close()
    conn3.close()
