import requests
import json
import ConfigParser
import traceback
import sys
from invoke import task, Collection
import csv
import logging
import time


config = ConfigParser.ConfigParser()
config.read('config.ini')

club_id = {'liv': 64,
           'mc': 65,
           'tot': 73,
           'che': 61,
           'ars': 57,
           'mu': 66,
           'hud': 394,
           'ful':63,
            'car': 715,
           'bur': 328,
           'so': 340,
           'bri': 397
           }

logging.basicConfig(level=logging.INFO)


def get_match_data(team_id='64', params={}):
    api_key = config.get('API', 'key')

    headers = {'X-Auth-Token': api_key}

    try:
        r = requests.get(
                url='http://api.football-data.org/v2/teams/'+team_id+'/matches',
                headers=headers,
                params=params
            )
        logging.info('URL: {}, headers: {}'.format(r.url, r.headers))
        logging.info('Status Code: {}'.format(r.status_code))
        time.sleep(30)
        if r.status_code == 200:
            return json.loads(r.text)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        raise


@task(name='team_points')
def get_points_tally(ctx, team_codes='liv,mc,tot,che,ars,mu,hud,ful,car,bur,so,bri', league_id=2021, pull=0):
    results = []
    for team_code in team_codes.split(','):
        team_results = []
        total = 0
        if pull:
            logging.info("Pulling new data for {}".format(team_code))
            team_data = get_match_data(team_id=str(club_id.get(team_code)))
            write_json(team_data, 'data/match_data_'+team_code+'.json')
        else:
            team_data = read_json(team_code)
        if team_data:
            for match in team_data.get("matches", {}):
                # import pdb; pdb.set_trace()
                competition_id = match.get('competition', {}).get('id', '')
                game_status = match.get('status')
                utc_date = match.get('utcDate', '')
                match_id = match.get('matchday', 0)
                if team_results:
                    total = team_results[-1].get('total', 0)
                if competition_id == league_id and game_status == 'FINISHED':
                    winner = match.get('score', {}).get('winner', '')
                    away_team_id = match.get('awayTeam', {}).get('id', '')
                    home_team_id = match.get('homeTeam', {}).get('id', '')
                    if 'AWAY' in winner:
                        if away_team_id == club_id.get(team_code):
                            team_results.append({'match_id': match_id, 'team': team_code, 'total': total+3,
                                                'game': 'AWAY', 'date': utc_date})
                        else:
                            team_results.append({'match_id': match_id, 'team': team_code, 'total': total,
                                                'game': 'HOME', 'date': utc_date})
                    elif 'HOME' in winner:
                        if home_team_id == club_id.get(team_code):
                            team_results.append({'match_id': match_id, 'team': team_code, 'total': total+3,
                                                'game': 'HOME', 'date': utc_date})
                        else:
                            team_results.append({'match_id': match_id, 'team': team_code, 'total': total,
                                                'game': 'AWAY', 'date': utc_date})
                    elif 'DRAW' in winner:
                        if home_team_id == club_id.get(team_code):
                            team_results.append({'match_id': match_id, 'team': team_code, 'total': total+1,
                                                'game': 'HOME', 'date': utc_date})
                        else:
                            team_results.append({'match_id': match_id, 'team': team_code, 'total': total+1,
                                                'game': 'AWAY', 'date': utc_date})
                    else:
                        print match
                elif competition_id == league_id and game_status == 'SCHEDULED':
                    if away_team_id == club_id.get(team_code):
                        team_results.append({'match_id': match_id, 'team': team_code, 'total': total+3,
                                             'game': 'AWAY', 'date': utc_date})
                    else:
                        team_results.append({'match_id': match_id, 'team': team_code, 'total': total+3,
                                            'game': 'HOME', 'date': utc_date})
                else:
                    pass
        results.extend(team_results)
    write_csv(results, 'team_results_full')


def read_json(file_name):
    with open('data/match_data_'+file_name+'.json') as f:
        data = json.load(f)
        return data


def write_json(output, file_name):
    with open(file_name, 'w') as f:
        json.dump(output, f, indent=4)


def write_csv(output, file_name):
    with open('data/'+file_name+'.csv', 'wb') as f:
        field_names = output[0].keys()
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(output)


ns = Collection(
    get_points_tally
)



