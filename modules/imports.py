import pandas as pd
import json
import os

json_files=os.listdir("data")

def open_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_teams_df():
    teams_data=[]
    for file in json_files:
        data=open_json_file('data/'+file)
        for side in ['Home', 'Away']:
            team_id = data[side]['id']
            team_name = data[side]['club']
            teams_data.append({'idteam': team_id, 'name': team_name})
    return pd.DataFrame(teams_data).drop_duplicates()

def create_players_df():
    players_data=[]
    for file in json_files:
        data=open_json_file('data/'+file)
        for side in ['Home', 'Away']:
            players=data[side]['players']
            for p_id, p_info in players.items():
                player_id = p_id
                lastname = p_info['info']['lastname']
                players_data.append({'idplayer': player_id, 'lastname': lastname})
    return pd.DataFrame(players_data).drop_duplicates()

def create_formations_types_df(side,data):
    formations_data = []
    players=data[side]['players']
    for p_id, p_info in players.items():
        formation = p_info['info']['formation_used']
        if formation not in formations_data:  
            formations_data.append(formation)
           
    return (formations_data)

def create_matches_df():
    matches_data=[]
    for file in json_files:
        data=open_json_file('data/'+file)
        home_team = data['Home']
        away_team = data['Away']
        matchid = data['id']
        date = data['dateMatch']
        duration = data['matchTime']
        period = data['period']
        championship = data.get('championship', None)
        quotation_pre_game = data.get('quotationPreGame', {})
        quotation_away = quotation_pre_game.get('Away', None)
        quotation_home = quotation_pre_game.get('Home', None)
        quotation_draw = quotation_pre_game.get('Draw', None)
        home_formation = create_formations_types_df('Home', data)
        away_formation = create_formations_types_df('Away', data)
        home_score =  len(data.get('matchData', {}).get('home', {}).get('goals', []))
        away_score =  len(data.get('matchData', {}).get('away', {}).get('goals', []))
        matches_data.append({
            'matchid': matchid, 'hometeam': home_team['club'], 'awayteam': away_team['club']
            , 'date':date, 'duration':duration,
            'period':period, 'chamionship': championship,
            'quotation_away': quotation_away,
            'quotation_home': quotation_home, 
            'quotation_draw': quotation_draw,
            'home_formation': home_formation,
            'away_formation': away_formation
            ,'home_score': home_score, 'away_score': away_score})
    return pd.DataFrame(matches_data)


def create_highlight_df():
    highlight_data = []
    for file in json_files:
        data=open_json_file('data/'+file)
        matchid = data['id']
        for matchdata in data['matchData']:
            time = matchdata['timeline']['time'],  
            playerid = matchdata['timeline']['playerId'],
            thetype = matchdata['timeline']['type']
            highlight_data.append({'matchid': matchid, 'time': time, 'playerid': playerid, 'type': thetype})
    return pd.DataFrame(highlight_data).drop_duplicates()


def create_substitutions_df():
    substitution_data = []
    for file in json_files:
        data=open_json_file('data/'+file)
        matchid = data['id']
        for side in ['Home', 'Away']:
            for substitution in data[side]['substitutions']:
                time = substitution['time']
                player_in = substitution['subOn']
                player_out = substitution['subOff']
                reason = substitution['reason']
                substitution_data.append({'matchid': matchid, 'time': time, 'on_playerid': player_in, 'off_playerid': player_out, 'reason': reason})
    return pd.DataFrame(substitution_data).drop_duplicates()

def get_player_quotation(quotation_players, player_id):
    player_key = f"player_{player_id}"
    return quotation_players.get(player_key)

def create_match_players_df():
    match_players_data = []
    for file in json_files:
        data = open_json_file('data/'+file)
        matchid = data['id']
        
        for side in ['Home', 'Away']:
            team_id = data[side]['id']
            for player_id, player_info in data[side]['players'].items():
                player_id = player_id,
                team_id = player_info['info']['idteam']
                position = player_info['info']['position']
                formation_place = player_info['info']['formation_place']
                quotation_player = get_player_quotation(data['quotationPlayers'], player_id)
                final_mark_2015 = player_info['info']['note_final_2015']


#play_duration,  player_stats (une colonne 
#par champ: penalty_conceaded, red_card, …). 