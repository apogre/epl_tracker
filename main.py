import requests
import json
import ConfigParser
import traceback
import sys


config = ConfigParser.ConfigParser()
config.read('config.ini')
api_key = config.get('API', 'key')


headers = {'X-Auth-Token': api_key}

club_id = {'liv': 64,
           'mc': 65
           }
# r = requests.get('http://api.football-data.org/v2/competitions/2021/standings', headers=headers)
#
# print r.status_code
#
# print r.text


def get_match_data(team_id='64', params={}):
    try:
        r = requests.get(
                url='http://api.football-data.org/v2/teams/'+team_id+'/matches',
                headers=headers,
                params=params
            )
        logging.info('URL: {}, headers: {}'.format(r.url, r.headers))
        logging.info('Status Code: {}'.format(r.status_code))
        if r.status_code == 200:
            return json.loads(r.text)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        raise


def get_points_tally(team_code, league_id):
    points_list = []
    total = 0
    team_data = read_json(team_code)
    matches = team_data.get('matches', {})
    if matches:
        for match in matches:
            competition_id = match.get('competition', {}).get('id', '')
            game_status = match.get('status')
            if competition_id == league_id and game_status == 'FINISHED':
                winner = match.get('score', {}).get('winner', '')
                away_team_id = match.get('awayTeam', {}).get('id', '')
                home_team_id = match.get('homeTeam', {}).get('id', '')
                utc_date = match.get('utcDate', '')
                if points_list:
                    total = points_list[-1][0]
                if 'AWAY' in winner:
                    if away_team_id == club_id.get(team_code):
                        points_list.append([total+3, 'AWAY', utc_date])
                    else:
                        points_list.append([total, 'HOME', utc_date])
                elif 'HOME' in winner:
                    if home_team_id == club_id.get(team_code):
                        points_list.append([total+3, 'HOME', utc_date])
                    else:
                        points_list.append([total, 'AWAY', utc_date])
                elif 'DRAW' in winner:
                    if home_team_id == club_id.get(team_code):
                        points_list.append([total+1, 'HOME', utc_date])
                    else:
                        points_list.append([total+1, 'AWAY', utc_date])
                else:
                    print match
        return points_list
    else:
        return []


def read_json(file_name):
    with open('data/match_data_'+file_name+'.json') as f:
        data = json.load(f)
        return data


def write_json(output, file_name):
    with open(file_name, 'w') as f:
        json.dump(output, f, indent=4)


if __name__ == '__main__':
    import logging;
    logging.basicConfig(level=logging.DEBUG)
    # match_data = get_match_data()
    # write_json(match_data, 'data/match_data_liv.json')
    # match_data = get_match_data(team_id='65')
    # write_json(match_data, 'data/match_data_mc.json')
    liv_points_list = get_points_tally('liv', 2021)
    mc_points_list = get_points_tally('mc', 2021)
    print liv_points_list
    print mc_points_list
