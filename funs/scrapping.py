from urllib import request
import bs4 as bs
import ssl
import re
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime     

def get_match_stats(): 

    # connect to the database
    context = ssl._create_unverified_context()
    conn = sqlite3.connect('data/database_matches_all.db')
    
    # define unique index for all matches
    match_id = 0

    # 2010
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2010.html?memo=%7B%22games%22%3A%7B%22faza%22%3A3%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-3')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            print(i)
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]          
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2011
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2011.html?memo=%7B%22games%22%3A%7B%22faza%22%3A3%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-3')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2012
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2012.html?memo=%7B%22games%22%3A%7B%22faza%22%3A3%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-3')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2013
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2013.html?memo=%7B%22games%22%3A%7B%22faza%22%3A3%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-3')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)
                
                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2014
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2014.html?memo=%7B%22games%22%3A%7B%22faza%22%3A2%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-2')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                    1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2015
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2015.html?memo=%7B%22games%22%3A%7B%22faza%22%3A2%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-2')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2016
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2016.html?memo=%7B%22games%22%3A%7B%22faza%22%3A2%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-2')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2017
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2017.html?memo=%7B%22games%22%3A%7B%22faza%22%3A2%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-2')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2018
    urls3 = ['https://www.plusliga.pl/games/tour/2018.html?memo=%7B%22games%22%3A%7B%22faza%22%3A2%7D%7D']
    for link in urls3:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-2')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                try:
                    table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                        0]

                    # create column with final score for home team
                    if float(score_home_team) == 3:
                        table_home['Home_win'] = 1
                    else:
                        table_home['Home_win'] = 0

                    table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                        1]

                    # create column with final score for away team
                    if float(score_away_team) == 3:
                        table_away['Away_win'] = 1
                    else:
                        table_away['Away_win'] = 0

                    # create column with date for both home and away team
                    table_home['Date'] = date
                    table_away['Date'] = date                    
                        
                    # add index for results of both teams
                    table_home['Id'] = match_id
                    table_away['Id'] = match_id

                    # increase counter of match's id
                    match_id = match_id + 1

                    # save tables to sql
                    table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                    table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)
                except:
                    pass

    # 2019
    urls2 = ['https://www.plusliga.pl/games/tour/2019.html?memo=%7B%22games%22%3A%7B%22faza%22%3A1%7D%7D']
    for link in urls2:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-1')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                try:
                    table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                        0]

                    # create column with final score for home team
                    if float(score_home_team) == 3:
                        table_home['Home_win'] = 1
                    else:
                        table_home['Home_win'] = 0

                    table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[
                        1]

                    # create column with final score for away team
                    if float(score_away_team) == 3:
                        table_away['Away_win'] = 1
                    else:
                        table_away['Away_win'] = 0

                    # create column with date for both home and away team
                    table_home['Date'] = date
                    table_away['Date'] = date                    
                        
                    # add index for results of both teams
                    table_home['Id'] = match_id
                    table_away['Id'] = match_id

                    # increase counter of match's id
                    match_id = match_id + 1

                    # save tables to sql
                    table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                    table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)
                except:
                    pass

    # 2020
    # First, we save the list of links for all matches in each season
    urls = ['https://www.plusliga.pl/games/tour/2020.html?memo=%7B%22games%22%3A%7B%22faza%22%3A2%7D%7D']
    # Then, we find the link for results of each match
    for link in urls:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-2')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2021
    urls3 = ['https://www.plusliga.pl/games/tour/2021.html?memo=%7B%22games%22%3A%7B%22faza%22%3A3%7D%7D']
    for link in urls3:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': re.compile('filtr-zawartosc faza faza-3')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})

        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]

        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    # 2022
    urls3 = ['https://www.plusliga.pl/games/tour/2022.html?memo=%7B%22games%22%3A%7B%22faza%22%3A2%7D%7D']
    for link in urls3:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]

        # find each round
        tags = bst.find('div', {'class': ('filtr-zawartosc faza faza-2')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})
        
        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]
        
        # find data for each match
        for key, value in links.items():
            for url in value:
                html4 = request.urlopen(url, context=context)
                bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                # find game's result
                ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                score = ww[-1].text
                score = score.replace('\n', '')
                score_home_team = score.split(':')[0]
                score_away_team = score.split(':')[1]

                # find game's date
                ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                date = ff[-1].text
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace('\r', '')
                date = date.split(',')[0]               
                
                # find tables with results
                table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                        'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[0]
                table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                    'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[1]

                # create column with final score for home team
                if float(score_home_team) == 3:
                    table_home['Home_win'] = 1
                else:
                    table_home['Home_win'] = 0

                # create column with final score for away team
                if float(score_away_team) == 3:
                    table_away['Away_win'] = 1
                else:
                    table_away['Away_win'] = 0

                # find team names
                team_name = bst4.find('h1').text
                team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                print(team_name.split(' vs '))
                home_name = team_name.split(' vs ')[0]
                away_name = team_name.split(' vs ')[1]

                table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                print(table_name_home, table_name_away)

                # create column with date for both home and away team
                table_home['Date'] = date
                table_away['Date'] = date            
                
                # add index for results of both teams
                table_home['Id'] = match_id
                table_away['Id'] = match_id

                # increase counter of match's id
                match_id = match_id + 1

                # save tables to sql database
                table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)
                
                
    # # 2023
    # urls3 = ['https://www.plusliga.pl/games/tour/2023.html?memo=%7B%22games%22%3A%7B%22faza%22%3A1%7D%7D']
    # for link in urls3:
    #     html = request.urlopen(link, context=context)
    #     bst = bs.BeautifulSoup(html.read(), 'html.parser')

    #     # find year
    #     season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
    #     season_nr_short = season_nr.split(' ')[1]
        
    #     # find each round
    #     tags = bst.find('div', {'data-id': ('Point Round')})
    #     tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})
        
    #     links = {}
    #     # find links for each match in each round
    #     for i, tag in enumerate(tags2):
    #         i = i + 1
    #         mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
    #         links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]
        
    #     # find data for each match
    #     for key, value in links.items():
    #         for url in value:
    #             html4 = request.urlopen(url, context=context)
    #             bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

    #             # find game's date
    #             ff = bst4.find_all('div', {'class': re.compile('date khanded')})
    #             date = ff[-1].text
    #             date = date.replace('\n', '')
    #             date = date.replace('\t', '')
    #             date = date.replace('\r', '')
    #             date = date.split(',')[0]       

    #             # check if game was already played
    #             if datetime(int(date.split('.')[2]), int(date.split('.')[1].lstrip("0")), int(date.split('.')[0].lstrip("0"))) <  datetime.now():
    #                 # find game's result
    #                 ww = bst4.find_all('div', {'class': re.compile('gameresult')})
    #                 score = ww[-1].text
    #                 score = score.replace('\n', '')
    #                 score_home_team = score.split(':')[0]
    #                 score_away_team = score.split(':')[1]

    #                 # find tables with results
    #                 table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
    #                         'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[0]
    #                 table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
    #                     'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[1]

    #                 # create column with final score for home team
    #                 if float(score_home_team) == 3:
    #                     table_home['Home_win'] = 1
    #                 else:
    #                     table_home['Home_win'] = 0

    #                 # create column with final score for away team
    #                 if float(score_away_team) == 3:
    #                     table_away['Away_win'] = 1
    #                 else:
    #                     table_away['Away_win'] = 0

    #                 # find team names
    #                 team_name = bst4.find('h1').text
    #                 team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
    #                 print(team_name.split(' vs '))
    #                 home_name = team_name.split(' vs ')[0]
    #                 away_name = team_name.split(' vs ')[1]

    #                 table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
    #                 table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
    #                 print(table_name_home, table_name_away)

    #                 # create column with date for both home and away team
    #                 table_home['Date'] = date
    #                 table_away['Date'] = date            
                    
    #                 # add index for results of both teams
    #                 table_home['Id'] = match_id
    #                 table_away['Id'] = match_id

    #                 # increase counter of match's id
    #                 match_id = match_id + 1

    #                 # save tables to sql database
    #                 table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
    #                 table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)
   
    # close connection
    conn.close()
                




def get_table_positions(year: list):
    
    for year_ in year:
        year_ = int(year_)
        
        if year_ == 2010:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)

            # table after each round
            for i in range(18):
                counter = 18
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()

        if year_ == 2011:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)

            # table after each round
            for i in range(18):
                counter = 18
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()
            
        if year_ == 2012:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)

            # table after each round
            for i in range(18):
                counter = 18
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()    

        if year_ == 2013:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(22):
                counter = 22
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()
                
        if year_ == 2014:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(26):
                counter = 26
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()
                
        if year_ == 2015:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(26):
                counter = 26
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()
                
        if year_ == 2016:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(30):
                counter = 30
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()
                
        if year_ == 2017:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(30):
                counter = 30
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()

                
        if year_ == 2018:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)

            # table after each round
            for i in range(26):
                counter = 26
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()
                
        if year_ == 2019:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(26):
                counter = 26
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()
                
        if year_ == 2020:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(26):
                counter = 26
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()

        if year_ == 2021:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(26):
                counter = 26
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()

        if year_ == 2022:
            
            # Database in which scraped data is stored
            conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

            # Links for individual teams and seasons
            url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

            context = ssl._create_unverified_context()

            html4 = request.urlopen(url, context=context)
            bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

            table_ = pd.read_html(str(bst4.find_all('table')))[0]
            print(table_)
            
            # table after each round
            for i in range(30):
                counter = 30
                table_round = table_.iloc[i::counter, :]

                # save table name
                table_name = 'Round_' + str(i + 1)

                # save tables to sql
                table_round.to_sql(table_name, conn, if_exists='replace', index=False)
                
            # close connection
            conn.close()
            




def refresh_match_stats():

    # import reference index and date
    reference = pd.read_csv(r"C:\Users\Rodzinka\Desktop\siatka_23\reference.csv")
    date_ = reference.iloc[0,0]
    match_id = int(reference.iloc[1,0])
    last_round = int(reference.iloc[2,0])
            
    context = ssl._create_unverified_context()
    conn = sqlite3.connect('data/database_matches_all.db')

    # frequent updates to the db
    # 2023
    urls3 = ['https://www.plusliga.pl/games/tour/2023.html?memo=%7B%22games%22%3A%7B%22faza%22%3A1%7D%7D']
    for link in urls3:
        html = request.urlopen(link, context=context)
        bst = bs.BeautifulSoup(html.read(), 'html.parser')

        # find year
        season_nr = bst.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
        season_nr_short = season_nr.split(' ')[1]
        
        # find each round
        tags = bst.find('div', {'data-id': ('Point Round')})
        tags2 = tags.find_all('div', {'data-type': re.compile('k_f')})
        
        links = {}
        # find links for each match in each round
        for i, tag in enumerate(tags2):
            i = i + 1
            mm = tag.find_all('a', {'class': re.compile('btn btn-default btm-margins')})
            links[i] = ['https://www.plusliga.pl' + m['href'] for m in mm]
        
        # find data for each match
        for key, value in links.items():
            if key <= last_round:
                for url in value:
                    html4 = request.urlopen(url, context=context)
                    bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

                    # find game's date
                    ff = bst4.find_all('div', {'class': re.compile('date khanded')})
                    date = ff[-1].text
                    date = date.replace('\n', '')
                    date = date.replace('\t', '')
                    date = date.replace('\r', '')
                    date = date.split(',')[0]      
                    
                    # find game's result
                    ww = bst4.find_all('div', {'class': re.compile('gameresult')})
                    score = ww[-1].text
                    score = score.replace('\n', '')
                    score_home_team = score.split(':')[0]
                    score_away_team = score.split(':')[1]

                    # check if table exists - if not create table filled with 0's
                    if not score == '0:0':
                        # find tables with results
                        table_home = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                                'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[0]
                        table_away = pd.read_html(str(bst4.find_all('table', {'class': re.compile(
                            'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive')})))[1]

                        # create column with final score for home team
                        if float(score_home_team) == 3:
                            table_home['Home_win'] = 1
                        else:
                            table_home['Home_win'] = 0

                        # create column with final score for away team
                        if float(score_away_team) == 3:
                            table_away['Away_win'] = 1
                        else:
                            table_away['Away_win'] = 0

                    else:
                        # create table filled with 0's of the same shape as the orginal tables
                        table_home = pd.DataFrame({('Unnamed: 0_level_0', 'Unnamed: 0_level_1'): {0: '1 Zouheir El Graoui', 1: '2 Maciej Muzaj (L)', 2: '6 Konrad Jankowski', 3: '8 Dominik Kramczyński', 4: '9 Michał Gierżot', 5: '10 Remigiusz Kapica', 6: '11 Tsimafei Zhukouski', 7: '12 Nicolas Zerba', 8: '14 Jakub Abramowicz', 9: '16 Kamil Dembiec', 10: '20 Kamil Szymura (L)', 11: '66 Kamil Kosiba', 12: '90 Wojciech Włodarczyk', 13: '91 Patryk Szczurek', 14: 'Łącznie'}, 
                                    ('Set', 'I'): {0: '4', 1: 0, 2: 0, 3: 0, 4: '1', 5: '6', 6: '3', 7: '5', 8: '2', 9: 0, 10: '*', 11: 0, 12: 0, 13: 0, 14: 0}, 
                                    ('Set', 'II'): {0: '3', 1: 0, 2: 0, 3: 0, 4: '6', 5: '5', 6: '2', 7: '4', 8: '1', 9: 0, 10: '*', 11: '*', 12: 0, 13: '*', 14: 0}, 
                                    ('Set', 'III'): {0: '4', 1: 0, 2: 0, 3: 0, 4: '1', 5: '6', 6: '3', 7: '5', 8: '2', 9: 0, 10: '*', 11: 0, 12: '*', 13: 0, 14: 0}, 
                                    ('Set', 'IV'): {0: '4', 1: 0, 2: 0, 3: 0, 4: '*', 5: '6', 6: '3', 7: '5', 8: '2', 9: 0, 10: '*', 11: '*', 12: '1', 13: '*', 14: 0}, 
                                    ('Set', 'V'): {0: '6', 1: 0, 2: 0, 3: 0, 4: '3', 5: '2', 6: '5', 7: '1', 8: '4', 9: 0, 10: '*', 11: 0, 12: 0, 13: '*', 14: 0}, 
                                    ('Punkty', 'suma'): {0: 19, 1: 0, 2: 0, 3: 0, 4: 8, 5: 27, 6: 3, 7: 7, 8: 7, 9: 0, 10: 0, 11: 0, 12: 2, 13: 0, 14: 73}, 
                                    ('Punkty', 'BP'): {0: 11, 1: 0, 2: 0, 3: 0, 4: 2, 5: 11, 6: 2, 7: 2, 8: 3, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 31}, 
                                    ('Punkty', 'z-s'): {0: 9, 1: 0, 2: 0, 3: 0, 4: 4, 5: 22, 6: -1, 7: 7, 8: 3, 9: 0, 10: -4, 11: -1, 12: 0, 13: 0, 14: 39}, 
                                    ('Zagrywka', 'Liczba'): {0: 14, 1: 0, 2: 0, 3: 0, 4: 12, 5: 17, 6: 21, 7: 9, 8: 20, 9: 0, 10: 0, 11: 2, 12: 6, 13: 4, 14: 105}, 
                                    ('Zagrywka', 'bł'): {0: 4, 1: 0, 2: 0, 3: 0, 4: 1, 5: 4, 6: 4, 7: 0, 8: 3, 9: 0, 10: 0, 11: 1, 12: 2, 13: 0, 14: 19}, 
                                    ('Zagrywka', 'as'): {0: 1, 1: 0, 2: 0, 3: 0, 4: 1, 5: 5, 6: 1, 7: 0, 8: 2, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 10}, 
                                    ('Zagrywka', 'eff%'): {0: '-21%', 1: '-', 2: '-', 3: '-', 4: '8%', 5: '6%', 6: '-10%', 7: '0%', 8: '-5%', 9: '-', 10: '-', 11: '-50%', 12: '-33%', 13: '25%', 14: '-5%'}, 
                                    ('Przyjecie zagrywki', 'liczba'): {0: 24, 1: 0, 2: 0, 3: 0, 4: 24, 5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 19, 11: 0, 12: 7, 13: 0, 14: 76}, 
                                    ('Przyjecie zagrywki', 'bł'): {0: 4, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 4, 11: 0, 12: 0, 13: 0, 14: 11}, 
                                    ('Przyjecie zagrywki', 'poz%'): {0: '38%', 1: '-', 2: '-', 3: '-', 4: '42%', 5: '0%', 6: '-', 7: '-', 8: '0%', 9: '-', 10: '11%', 11: '-', 12: '29%', 13: '-', 14: '30%'}, 
                                    ('Przyjecie zagrywki', 'perf%'): {0: '33%', 1: '-', 2: '-', 3: '-', 4: '17%', 5: '0%', 6: '-', 7: '-', 8: '0%', 9: '-', 10: '11%', 11: '-', 12: '0%', 13: '-', 14: '18%'}, 
                                    ('Atak', 'liczba'): {0: 27, 1: 0, 2: 0, 3: 0, 4: 17, 5: 33, 6: 4, 7: 7, 8: 7, 9: 0, 10: 0, 11: 0, 12: 5, 13: 0, 14: 100}, 
                                    ('Atak', 'bł'): {0: 2, 1: 0, 2: 0, 3: 0, 4: 2, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 4}, 
                                    ('Atak', 'blok'): {0: 2, 1: 0, 2: 0, 3: 0, 4: 3, 5: 4, 6: 1, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 2, 13: 0, 14: 12}, 
                                    ('Atak', 'Pkt'): {0: 15, 1: 0, 2: 0, 3: 0, 4: 5, 5: 20, 6: 1, 7: 5, 8: 4, 9: 0, 10: 0, 11: 0, 12: 1, 13: 0, 14: 51}, 
                                    ('Atak', 'skut%'): {0: '56%', 1: '-', 2: '-', 3: '-', 4: '29%', 5: '61%', 6: '25%', 7: '71%', 8: '57%', 9: '-', 10: '-', 11: '-', 12: '20%', 13: '-', 14: '51%'}, 
                                    ('Atak', 'eff%'): {0: '41%', 1: '-', 2: '-', 3: '-', 4: '0%', 5: '48%', 6: '0%', 7: '71%', 8: '56%', 9: '-', 10: '-', 11: '-', 12: '-20%', 13: '-', 14: '35%'}, 
                                    ('Blok', 'pkt'): {0: 3, 1: 0, 2: 0, 3: 0, 4: 2, 5: 2, 6: 1, 7: 2, 8: 1, 9: 0, 10: 0, 11: 0, 12: 1, 13: 0, 14: 12}, 
                                    ('Blok', 'wyblok'): {0: 6, 1: 0, 2: 0, 3: 0, 4: 3, 5: 2, 6: 1, 7: 3, 8: 2, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 17}, 
                                    ('Home_win', ''): {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}, 
                                    ('Date', ''): {0: '04.11.2023', 1: '04.11.2023', 2: '04.11.2023', 3: '04.11.2023', 4: '04.11.2023', 5: '04.11.2023', 6: '04.11.2023', 7: '04.11.2023', 8: '04.11.2023', 9: '04.11.2023', 10: '04.11.2023', 11: '04.11.2023', 12: '04.11.2023', 13: '04.11.2023', 14: '04.11.2023'}, 
                                    ('Id', ''): {0: 2268, 1: 2268, 2: 2268, 3: 2268, 4: 2268, 5: 2268, 6: 2268, 7: 2268, 8: 2268, 9: 2268, 10: 2268, 11: 2268, 12: 2268, 13: 2268, 14: 2268}})

                        table_away = pd.DataFrame({('Unnamed: 0_level_0', 'Unnamed: 0_level_1'): {0: '1 Zouheir El Graoui', 1: '2 Maciej Muzaj (L)', 2: '6 Konrad Jankowski', 3: '8 Dominik Kramczyński', 4: '9 Michał Gierżot', 5: '10 Remigiusz Kapica', 6: '11 Tsimafei Zhukouski', 7: '12 Nicolas Zerba', 8: '14 Jakub Abramowicz', 9: '16 Kamil Dembiec', 10: '20 Kamil Szymura (L)', 11: '66 Kamil Kosiba', 12: '90 Wojciech Włodarczyk', 13: '91 Patryk Szczurek', 14: 'Łącznie'}, 
                                    ('Set', 'I'): {0: '4', 1: 0, 2: 0, 3: 0, 4: '1', 5: '6', 6: '3', 7: '5', 8: '2', 9: 0, 10: '*', 11: 0, 12: 0, 13: 0, 14: 0}, 
                                    ('Set', 'II'): {0: '3', 1: 0, 2: 0, 3: 0, 4: '6', 5: '5', 6: '2', 7: '4', 8: '1', 9: 0, 10: '*', 11: '*', 12: 0, 13: '*', 14: 0}, 
                                    ('Set', 'III'): {0: '4', 1: 0, 2: 0, 3: 0, 4: '1', 5: '6', 6: '3', 7: '5', 8: '2', 9: 0, 10: '*', 11: 0, 12: '*', 13: 0, 14: 0}, 
                                    ('Set', 'IV'): {0: '4', 1: 0, 2: 0, 3: 0, 4: '*', 5: '6', 6: '3', 7: '5', 8: '2', 9: 0, 10: '*', 11: '*', 12: '1', 13: '*', 14: 0}, 
                                    ('Set', 'V'): {0: '6', 1: 0, 2: 0, 3: 0, 4: '3', 5: '2', 6: '5', 7: '1', 8: '4', 9: 0, 10: '*', 11: 0, 12: 0, 13: '*', 14: 0}, 
                                    ('Punkty', 'suma'): {0: 19, 1: 0, 2: 0, 3: 0, 4: 8, 5: 27, 6: 3, 7: 7, 8: 7, 9: 0, 10: 0, 11: 0, 12: 2, 13: 0, 14: 73}, 
                                    ('Punkty', 'BP'): {0: 11, 1: 0, 2: 0, 3: 0, 4: 2, 5: 11, 6: 2, 7: 2, 8: 3, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 31}, 
                                    ('Punkty', 'z-s'): {0: 9, 1: 0, 2: 0, 3: 0, 4: 4, 5: 22, 6: -1, 7: 7, 8: 3, 9: 0, 10: -4, 11: -1, 12: 0, 13: 0, 14: 39}, 
                                    ('Zagrywka', 'Liczba'): {0: 14, 1: 0, 2: 0, 3: 0, 4: 12, 5: 17, 6: 21, 7: 9, 8: 20, 9: 0, 10: 0, 11: 2, 12: 6, 13: 4, 14: 105}, 
                                    ('Zagrywka', 'bł'): {0: 4, 1: 0, 2: 0, 3: 0, 4: 1, 5: 4, 6: 4, 7: 0, 8: 3, 9: 0, 10: 0, 11: 1, 12: 2, 13: 0, 14: 19}, 
                                    ('Zagrywka', 'as'): {0: 1, 1: 0, 2: 0, 3: 0, 4: 1, 5: 5, 6: 1, 7: 0, 8: 2, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 10}, 
                                    ('Zagrywka', 'eff%'): {0: '-21%', 1: '-', 2: '-', 3: '-', 4: '8%', 5: '6%', 6: '-10%', 7: '0%', 8: '-5%', 9: '-', 10: '-', 11: '-50%', 12: '-33%', 13: '25%', 14: '-5%'}, 
                                    ('Przyjecie zagrywki', 'liczba'): {0: 24, 1: 0, 2: 0, 3: 0, 4: 24, 5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 19, 11: 0, 12: 7, 13: 0, 14: 76}, 
                                    ('Przyjecie zagrywki', 'bł'): {0: 4, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 4, 11: 0, 12: 0, 13: 0, 14: 11}, 
                                    ('Przyjecie zagrywki', 'poz%'): {0: '38%', 1: '-', 2: '-', 3: '-', 4: '42%', 5: '0%', 6: '-', 7: '-', 8: '0%', 9: '-', 10: '11%', 11: '-', 12: '29%', 13: '-', 14: '30%'}, 
                                    ('Przyjecie zagrywki', 'perf%'): {0: '33%', 1: '-', 2: '-', 3: '-', 4: '17%', 5: '0%', 6: '-', 7: '-', 8: '0%', 9: '-', 10: '11%', 11: '-', 12: '0%', 13: '-', 14: '18%'}, 
                                    ('Atak', 'liczba'): {0: 27, 1: 0, 2: 0, 3: 0, 4: 17, 5: 33, 6: 4, 7: 7, 8: 7, 9: 0, 10: 0, 11: 0, 12: 5, 13: 0, 14: 100}, 
                                    ('Atak', 'bł'): {0: 2, 1: 0, 2: 0, 3: 0, 4: 2, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 4}, 
                                    ('Atak', 'blok'): {0: 2, 1: 0, 2: 0, 3: 0, 4: 3, 5: 4, 6: 1, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 2, 13: 0, 14: 12}, 
                                    ('Atak', 'Pkt'): {0: 15, 1: 0, 2: 0, 3: 0, 4: 5, 5: 20, 6: 1, 7: 5, 8: 4, 9: 0, 10: 0, 11: 0, 12: 1, 13: 0, 14: 51}, 
                                    ('Atak', 'skut%'): {0: '56%', 1: '-', 2: '-', 3: '-', 4: '29%', 5: '61%', 6: '25%', 7: '71%', 8: '57%', 9: '-', 10: '-', 11: '-', 12: '20%', 13: '-', 14: '51%'}, 
                                    ('Atak', 'eff%'): {0: '41%', 1: '-', 2: '-', 3: '-', 4: '0%', 5: '48%', 6: '0%', 7: '71%', 8: '56%', 9: '-', 10: '-', 11: '-', 12: '-20%', 13: '-', 14: '35%'}, 
                                    ('Blok', 'pkt'): {0: 3, 1: 0, 2: 0, 3: 0, 4: 2, 5: 2, 6: 1, 7: 2, 8: 1, 9: 0, 10: 0, 11: 0, 12: 1, 13: 0, 14: 12}, 
                                    ('Blok', 'wyblok'): {0: 6, 1: 0, 2: 0, 3: 0, 4: 3, 5: 2, 6: 1, 7: 3, 8: 2, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 17}, 
                                    ('Away_win', ''): {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}, 
                                    ('Date', ''): {0: '04.11.2023', 1: '04.11.2023', 2: '04.11.2023', 3: '04.11.2023', 4: '04.11.2023', 5: '04.11.2023', 6: '04.11.2023', 7: '04.11.2023', 8: '04.11.2023', 9: '04.11.2023', 10: '04.11.2023', 11: '04.11.2023', 12: '04.11.2023', 13: '04.11.2023', 14: '04.11.2023'}, 
                                    ('Id', ''): {0: 2268, 1: 2268, 2: 2268, 3: 2268, 4: 2268, 5: 2268, 6: 2268, 7: 2268, 8: 2268, 9: 2268, 10: 2268, 11: 2268, 12: 2268, 13: 2268, 14: 2268}})

                        table_away.iloc[:,1:] = 0
                        table_home.iloc[:,1:] = 0

                        # create columns with final score for home team - artificial 0 - match has not been played yet
                        table_home['Home_win'] = 0
                        table_away['Away_win'] = 0                    
                    
                    # find team names
                    team_name = bst4.find('h1').text
                    team_name = team_name.replace('\n', '').replace('\t', '').replace('\r', '')
                    print(team_name.split(' vs '))
                    home_name = team_name.split(' vs ')[0]
                    away_name = team_name.split(' vs ')[1]

                    table_name_home = season_nr_short + ' ' + home_name + ' ' + str(key)
                    table_name_away = season_nr_short + ' ' + away_name + ' ' + str(key)
                    print(table_name_home, table_name_away)

                    # create column with date for both home and away team
                    table_home['Date'] = date
                    table_away['Date'] = date            
                    
                    # add index for results of both teams
                    table_home['Id'] = match_id
                    table_away['Id'] = match_id

                    # increase counter of match's id
                    match_id = match_id + 1

                    print(match_id)
                    
                    # save tables to sql database
                    table_home.to_sql(table_name_home, conn, if_exists='replace', index=False)
                    table_away.to_sql(table_name_away, conn, if_exists='replace', index=False)

    last_round = last_round + 1
    # save for reference during the next run

    temp_ = pd.DataFrame([date_, match_id, last_round])
    temp_.to_csv("reference.csv", sep=',',index=False)
    
    # close connection
    conn.close()



def refresh_table_positions():
    # import reference index and date
    reference = pd.read_csv(r"C:\Users\Rodzinka\Desktop\siatka_23\reference.csv")
    last_round = int(reference.iloc[2,0])

    year_ = 2023

    # Database in which scraped data is stored
    conn = sqlite3.connect('data/database_rounds_{}.db'.format(year_))

    # Links for individual teams and seasons
    url = 'https://www.plusliga.pl/table/tour/' + str(year_) + '.html'

    context = ssl._create_unverified_context()

    html4 = request.urlopen(url, context=context)
    bst4 = bs.BeautifulSoup(html4.read(), 'html.parser')

    table_ = pd.read_html(str(bst4.find_all('table')))[0]
    print(table_)

    # table after each round, but only for rounds that have already been played
    for i in range(last_round):
        counter = 30
        table_round = table_.iloc[i::counter, :]

        # save table name
        table_name = 'Round_' + str(i + 1)

        # save tables to sql
        table_round.to_sql(table_name, conn, if_exists='replace', index=False)
        
    # close connection 
    conn.close()
    
    
def refresh_player_data():
    # Database in which scraped data is stored
    conn = sqlite3.connect('data/database_players_allteams.db')

    # Links for individual teams and seasons
    links_teams_seasons = ['https://www.plusliga.pl/teams/tour/2017/id/1413.html', 'https://www.plusliga.pl/teams/tour/2016/id/1413.html', 'https://www.plusliga.pl/teams/tour/2015/id/1413.html',
                        'https://www.plusliga.pl/teams/tour/2014/id/1413.html', 'https://www.plusliga.pl/teams/tour/2013/id/1413.html', 'https://www.plusliga.pl/teams/tour/2012/id/1413.html',
                        'https://www.plusliga.pl/teams/tour/2011/id/1413.html', 'https://www.plusliga.pl/teams/tour/2010/id/1413.html',
                        'https://www.plusliga.pl/teams/tour/2017/id/1402.html', 'https://www.plusliga.pl/teams/tour/2018/id/1402.html', 'https://www.plusliga.pl/teams/tour/2019/id/1402.html',
                        'https://www.plusliga.pl/teams/tour/2016/id/1402.html', 'https://www.plusliga.pl/teams/tour/2015/id/1402.html', 'https://www.plusliga.pl/teams/tour/2014/id/1402.html',
                        'https://www.plusliga.pl/teams/tour/2013/id/1402.html', 'https://www.plusliga.pl/teams/tour/2012/id/1402.html', 'https://www.plusliga.pl/teams/tour/2011/id/1402.html',
                        'https://www.plusliga.pl/teams/tour/2010/id/1402.html',
                        'https://www.plusliga.pl/teams/tour/2017/id/26783.html', "https://www.plusliga.pl/teams/tour/2018/id/26783.html", 'https://www.plusliga.pl/teams/tour/2019/id/26783.html',
                        'https://www.plusliga.pl/teams/tour/2020/id/26783.html', 'https://www.plusliga.pl/teams/tour/2016/id/26783.html', 'https://www.plusliga.pl/teams/tour/2015/id/26783.html',
                        'https://www.plusliga.pl/teams/tour/2014/id/26783.html',
                        'https://www.plusliga.pl/teams/tour/2016/id/29788.html', 'https://www.plusliga.pl/teams/tour/2017/id/29788.html', 'https://www.plusliga.pl/teams/tour/2018/id/29788.html',
                        'https://www.plusliga.pl/teams/tour/2016/id/1409.html', "https://www.plusliga.pl/teams/tour/2015/id/1409.html", 'https://www.plusliga.pl/teams/tour/2014/id/1409.html',
                        'https://www.plusliga.pl/teams/tour/2013/id/1409.html', 'https://www.plusliga.pl/teams/tour/2012/id/1409.html', 'https://www.plusliga.pl/teams/tour/2011/id/1409.html',
                        'https://www.plusliga.pl/teams/tour/2010/id/1409.html',
                        'https://www.plusliga.pl/teams/tour/2010/id/1412.html',
                        'https://www.plusliga.pl/teams/tour/2023/id/2100012.html',
                        'https://www.plusliga.pl/teams/tour/2023/id/26787.html', 'https://www.plusliga.pl/teams/tour/2022/id/26787.html', 'https://www.plusliga.pl/teams/tour/2021/id/26787.html',
                        'https://www.plusliga.pl/teams/tour/2020/id/26787.html', 'https://www.plusliga.pl/teams/tour/2019/id/26787.html', 'https://www.plusliga.pl/teams/tour/2018/id/26787.html',
                        'https://www.plusliga.pl/teams/tour/2017/id/26787.html', 'https://www.plusliga.pl/teams/tour/2016/id/26787.html', 'https://www.plusliga.pl/teams/tour/2015/id/26787.html',
                        'https://www.plusliga.pl/teams/tour/2014/id/26787.html']


    context = ssl._create_unverified_context()

    dicti = {}
    # Then, we extract link for player data out of each team link
    for link in links_teams_seasons:
        html3 = request.urlopen(link, context=context)
        bst3 = bs.BeautifulSoup(html3.read(), 'html.parser')
        tags = bst3.find_all('div', {'class': re.compile('player-item to-filter cut-paste')})

        links_players = []
        links_players = ['https://www.plusliga.pl' + tag.find('a')['href'] for tag in tags]

        team_name = bst3.find('h1').text
        
        # for new teams in plusliga, the code needs to be slightly modified 
        if team_name == 'Exact Systems Hemarpol Częstochowa':
            team_name_nr = 'Exact Systems Hemarpol Częstochowa' + ' ' + '2023/2024'
        
        else: 
            season_nr = bst3.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
            season_nr_short = season_nr.split(' ')[1]

            team_name_nr = team_name + ' ' + season_nr_short

        dicti[team_name_nr] = links_players


    # Finally, we extract height, weight and range for each player
    for key, value in dicti.items():
        tab = pd.DataFrame(columns=["Height", "Weight", "Range", "Position"])
        tab2 = pd.DataFrame(columns=["Age"])
        print(key, value)
        for url_player in value:
            html_player = request.urlopen(url_player, context=context)
            bst_player = bs.BeautifulSoup(html_player.read(), 'html.parser')

            # find position
            tags_pos = bst_player.find_all('div', {'class': re.compile("datainfo small")})
            uu = tags_pos[1].text
            uu = uu.split(' ')[1]

            # find height, weight and range
            tags_p = bst_player.find_all('div', {'class': re.compile("datainfo text-center")})
            tt = [re.sub('[^0-9\.]','', tag.text) for tag in tags_p]

            # create df with all 4 features
            tt.append(str(uu))
            tab = pd.concat([tab, pd.DataFrame([tt], columns=["Height", "Weight", "Range", "Position"])], ignore_index=True)

            # find age - not used for now in final modelling
            tags_p2 = bst_player.find_all('div', {'class': re.compile("datainfo small")})
            tt2 = [re.sub('[^0-9\.]', '', tag.text) for tag in tags_p2]
            tab2 = pd.concat([tab2, pd.DataFrame([tt2[0][-4:]], columns=["Age"])], ignore_index=True)

            tab3 = pd.concat([tab, tab2], axis=1)

        print(tab3)

        # Save data to sql database
        tab.to_sql(key, conn, if_exists='replace', index=False)

    # close connection
    conn.close()
    



def get_player_data():
    # Database in which scraped data is stored
    conn = sqlite3.connect('data/database_players_allteams.db')

    # First, we save the link for each team
    url = 'https://www.plusliga.pl/statsTeams/tournament_1/all.html'
    context = ssl._create_unverified_context()
    html = request.urlopen(url, context=context)
    bst = bs.BeautifulSoup(html.read(), 'html.parser')
    tags = bst.find_all('div', {'class': re.compile('thumbnail player team-logo')})
    links_teams = []
    links_teams = ['https://www.plusliga.pl' + tag.find('a')['href'][16:] for tag in tags]

    # remove teams that have different web layout - I will access them separately 
    indexes = [2, 9, 16, 19, 20, 26]
    for index in sorted(indexes, reverse=True):
        del links_teams[index]

    # Then, for each team we find the link to results after each season
    links_teams_seasons = {}
    for i, link_ in enumerate(links_teams):
        html2 = request.urlopen(link_, context=context)
        bst2 = bs.BeautifulSoup(html2.read(), 'html.parser')
        tags2 = bst2.find_all('a', {'href': re.compile('/teams/tour.*')})
        links_teams_seasons[i] = ['https://www.plusliga.pl' + tag['href'] for tag in tags2]

    dicti = {}
    # Then, we extract link for player data out of each team link
    for i, links in links_teams_seasons.items():
        for j, link in enumerate(links):
            html3 = request.urlopen(link, context=context)
            bst3 = bs.BeautifulSoup(html3.read(), 'html.parser')
            tags = bst3.find_all('div', {'class': re.compile('player-item to-filter cut-paste')})

            links_players = []
            links_players = ['https://www.plusliga.pl' + tag.find('a')['href'] for tag in tags]

            team_name = bst3.find('h1').text

            season_nr = bst3.find('button', {'class': re.compile("btn btn-default dropdown-toggle form-control")}).text
            season_nr_short = season_nr.split(' ')[1]

            team_name_nr = team_name + ' ' + season_nr_short

            dicti[team_name_nr] = links_players


    # Finally, we extract height, weight and range for each player
    for key, value in dicti.items():
        tab = pd.DataFrame(columns=["Height", "Weight", "Range", "Position"])
        tab2 = pd.DataFrame(columns=["Age"])
        print(key, value)
        for url_player in value:
            html_player = request.urlopen(url_player, context=context)
            bst_player = bs.BeautifulSoup(html_player.read(), 'html.parser')

            # find position
            tags_pos = bst_player.find_all('div', {'class': re.compile("datainfo small")})
            uu = tags_pos[1].text
            uu = uu.split(' ')[1]

            # find height, weight and range
            tags_p = bst_player.find_all('div', {'class': re.compile("datainfo text-center")})
            tt = [re.sub('[^0-9\.]','', tag.text) for tag in tags_p]

            # create df with all 4 features
            tt.append(str(uu))
            tab = pd.concat([tab, pd.DataFrame([tt], columns=["Height", "Weight", "Range", "Position"])], ignore_index=True)

            # find age - not used for now in final modelling
            tags_p2 = bst_player.find_all('div', {'class': re.compile("datainfo small")})
            tt2 = [re.sub('[^0-9\.]', '', tag.text) for tag in tags_p2]
            tab2 = pd.concat([tab2, pd.DataFrame([tt2[0][-4:]], columns=["Age"])], ignore_index=True)

            tab3 = pd.concat([tab, tab2], axis=1)

        print(tab3)

        # Save data to sql database
        tab.to_sql(key, conn, if_exists='replace', index=False)

    # close connection
    conn.close()




