''' Following functions are used for generating predictions for curent season '''

import pandas as pd
import sqlite3
import os 
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# change directory 
os.chdir(r'C:\Users\Rodzinka\Desktop\siatka_23')


def generate_predictions():
    '''
    Generate predictions for the currently played season, based on the last round - reference round number, that is the last round that will have predictions generated for, is stored in the csv file 
    
    Parameters
    ----------
    
    Examples
    --------
    >>> generate_predictions() generates predictions for currently played season and saves them to csv file 
    
    '''

    # read database, change path and database name if needed
    conn = sqlite3.connect('data/final_database.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # find table names - match data
    table_names = sorted(list(zip(*result))[0])

    # create first table
    data = pd.read_sql("SELECT * FROM '{}'".format(table_names[0]), conn)

    # append all match stats to one table
    for name in table_names[1:]:
        data_i = pd.read_sql("SELECT * FROM '{}'".format(name), conn)
        data = pd.concat([data, data_i])

    # copy data for model performance assessment purposes
    data_copy = data.copy()

    data_to_export = data[['Team_name_home', 'Round_home', 'Team_name_away', 'Year_away']]

    data = data.drop(columns = ['Team_name_home', 'Round_home', 'Team_name_away', 'Year_away', 'Round_away', 
                                'Results_away', 'Round_diff', 'Year_diff', 'Team_name_diff' ]) 

    # drop NAs
    data = data.dropna()

    # import predefined column names
    column_names= pd.read_csv('data/column_names.txt', delimiter=',', header=None)
    column_names= [x for x in column_names.iloc[:, 0]]
    column_names = [e[2:-1] for e in column_names]

    # create one new column 
    data['%_points_poss_diff'] = data['%_points_poss_home'] - data['%_points_poss_away']

    # change column names
    data.columns = column_names

    # define column with the result
    df1 = data.pop('Results_home') 
    data['Result']=df1 

    # define in_sample data
    in_sample = data[data['Year_home'].isin(['2022/2023', '2021/2022','2020/2021', '2019/2020', '2018/2019', '2017/2018', '2016/2017', '2015/2016', '2014/2015', '2013/2014', 
            '2012/2013', '2011/2012', '2010/2011'])]

    # define games' results
    labels = in_sample.pop('Result')

    # drop columns not used for modeling
    in_sample = in_sample.drop(columns=['ID', 'Year_home'])

    # split in-sample data into train and validation 
    X_train, X_test, y_train, y_test = train_test_split(in_sample, labels, test_size = 0.3, random_state = 30)

    # define out-of-sample data
    out_of_time = data[data['Year_home'] == ('2023/2024')]
    y_oot = out_of_time['Result']
    X_oot = out_of_time.drop(columns=['ID', 'Result', 'Year_home'])

    # prepare data for performance testing
    # import column names
    column_names_with_round = pd.read_csv('data/column_names_with_round.txt', delimiter=',', header=None)
    column_names_with_round = [x for x in column_names_with_round.iloc[:, 0]]
    column_names_with_round = [e[2:-1] for e in column_names_with_round]

    # prepare data for performance assessment
    data_copy = data_copy.drop(columns = ['Team_name_home', 'Team_name_away', 'Year_away', 'Round_away', 
                                'Results_away', 'Round_diff', 'Year_diff', 'Team_name_diff' ]) 

    # remove NAs
    data_copy = data_copy.dropna()

    # out of sample data only
    data_temp = data_copy[data_copy['Year_home'] == ('2023/2024')].copy()
    data_temp['%_points_poss_diff'] = data_temp['%_points_poss_home'] - data_temp['%_points_poss_away']
    data_temp.columns = column_names_with_round

    # define column with the result
    data_temp.rename(columns={'Results_home': 'Result'}, inplace=True)


    # import round number
    reference = pd.read_csv(r"C:\Users\Rodzinka\Desktop\siatka_23\data\reference.csv")
    last_round = int(reference.iloc[2,0]) - 1
                

    current_round = data_temp[data_temp['Round']==last_round].copy()
    current_round.drop(columns=['Result', 'ID', 'Year_home', 'Round'], inplace=True)

    # generate predictions

    xgb_model = XGBClassifier(colsample_bytree=0.5, learning_rate=0.01, max_depth=3, min_child_weight=5, n_estimators=500, objective='binary:logistic', subsample=0.1)

    # fit the final model
    xgb_model.fit(in_sample, labels)

    # generate predictions for one current round

    predictions_oot = xgb_model.predict(current_round)

    probability_oot = xgb_model.predict_proba(current_round)


    data_to_export = data_to_export.iloc[current_round.index]
    data_to_export['Predicted_probability_home'] = probability_oot[:,1]
    data_to_export['Predicted_probability_away'] = probability_oot[:,0]
    data_to_export['Result_(home_team)'] = predictions_oot

    data_to_export.to_csv('data/predictions_round_{0}.txt'.format(last_round))
