from riotwatcher import LolWatcher, ApiError
from . import constants

# app = Flask(__name__)
api_key = constants.API_KEY
watcher = LolWatcher(api_key)
my_region = 'na1'
full_team = []
your_team = []
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

def duo_checker(account1, account2, game_list):
    try:
        left_bar = [""]
        stats = []
        ranked_solo_case = False
        ranked_flex_case = False
        norms_case = False
        aram_case = False
        aram_wins = 0
        aram_losses = 0
        norms_wins = 0
        norms_losses = 0
        ranked_solo_wins = 0
        ranked_solo_losses = 0
        ranked_flex_wins = 0
        ranked_flex_losses = 0
        total_wins = 0
        total_losses = 0
        contains_duo = False
        if '1' in game_list:
            left_bar.append("Ranked Solo: Win Rate")
            left_bar.append("Ranked Solo: Total Games")
            ranked_solo_case = True
        if '2' in game_list:
            left_bar.append("Ranked Flex: Win Rate")
            left_bar.append("Ranked Flex: Total Games")
            ranked_flex_case = True
        if '3' in game_list:
            left_bar.append("Norms: Win Rate")
            left_bar.append("Norms: Total Games")
            norms_case = True
        if '4' in game_list:
            left_bar.append("Aram: Win Rate")
            left_bar.append("Aram: Total Games")
            aram_case = True
        left_bar.append("Total Win Rate")
        left_bar.append("Total Games")
        player = watcher.summoner.by_name(my_region, account1)
        my_matches = watcher.match.matchlist_by_account(my_region, player['accountId'])
        match_list = my_matches['matches']
        for match_counter in range(0, 100):
            current_match = match_list[match_counter]
            contains_duo = False
            if ranked_solo_case:
                if current_match['queue'] == 420:
                    match_info = watcher.match.by_id(my_region, current_match['gameId'])
                    player_number = -1
                    for x in match_info['participantIdentities']:
                        for y in match_info['participantIdentities']:
                            if y['player']['summonerName'] == account2:
                                contains_duo = True
                                break
                        if x['player']['summonerName'] == player['name']:
                            for a in match_info['participants']:
                                player_number += 1
                                if a['participantId'] == x['participantId']:
                                    break
                    player_game_info = match_info['participants'][player_number]
                    if player_game_info['stats']['win'] and contains_duo:
                        ranked_solo_wins += 1
                        total_wins += 1
                    elif contains_duo:
                        ranked_solo_losses += 1
                        total_losses += 1
            if ranked_flex_case:
                if current_match['queue'] not in [410, 420, 450] and not current_match['queue'] < 410:
                    match_info = watcher.match.by_id(my_region, current_match['gameId'])
                    player_number = -1
                    for x in match_info['participantIdentities']:
                        for y in match_info['participantIdentities']:
                            if y['player']['summonerName'] == account2:
                                contains_duo = True
                                break
                        if x['player']['summonerName'] == player['name']:
                            for a in match_info['participants']:
                                player_number += 1
                                if a['participantId'] == x['participantId']:
                                    break
                    player_game_info = match_info['participants'][player_number]
                    if player_game_info['stats']['win'] and contains_duo:
                        ranked_flex_wins += 1
                        total_wins += 1
                    elif contains_duo:
                        ranked_flex_losses += 1
                        total_losses += 1
            if aram_case:
                if current_match['queue'] == 450:
                    match_info = watcher.match.by_id(my_region, current_match['gameId'])
                    player_number = -1
                    for x in match_info['participantIdentities']:
                        for y in match_info['participantIdentities']:
                            if y['player']['summonerName'] == account2:
                                contains_duo = True
                                break
                        if x['player']['summonerName'] == player['name']:
                            for a in match_info['participants']:
                                player_number += 1
                                if a['participantId'] == x['participantId']:
                                    break
                    player_game_info = match_info['participants'][player_number]
                    if player_game_info['stats']['win'] and contains_duo:
                        aram_wins += 1
                        total_wins += 1
                    elif contains_duo:
                        aram_losses += 1
                        total_losses += 1
            if norms_case:
                if current_match['queue'] <= 410:
                    match_info = watcher.match.by_id(my_region, current_match['gameId'])
                    player_number = -1
                    for x in match_info['participantIdentities']:
                        for y in match_info['participantIdentities']:
                            if y['player']['summonerName'] == account2:
                                contains_duo = True
                                break
                        if x['player']['summonerName'] == player['name']:
                            for a in match_info['participants']:
                                player_number += 1
                                if a['participantId'] == x['participantId']:
                                    break
                    player_game_info = match_info['participants'][player_number]
                    if player_game_info['stats']['win'] and contains_duo:
                        norms_wins += 1
                        total_wins += 1
                    elif contains_duo:
                        norms_losses += 1
                        total_losses += 1
        info = ["Duo winrate: "+account1+" and "+account2]

        try:
            if ranked_solo_case:
                info.append(str(round((ranked_solo_wins / (ranked_solo_wins + ranked_solo_losses) * 100), 2))+"%")
                info.append(ranked_solo_wins + ranked_solo_losses)
        except ZeroDivisionError as err:
            info.append("N/A")
            info.append("N/A")
        try:
            if ranked_flex_case:
                info.append(str(round((ranked_flex_wins / (ranked_flex_wins + ranked_flex_losses) * 100), 2))+"%")
                info.append(ranked_flex_wins + ranked_flex_losses)
        except ZeroDivisionError as err:
            info.append("N/A")
            info.append("N/A")
        try:
            if norms_case:
                info.append(str(round((norms_wins / (norms_wins + norms_losses) * 100), 2))+"%")
                info.append(norms_wins + norms_losses)
        except ZeroDivisionError as err:
            info.append("N/A")
            info.append("N/A")
        try:
            if aram_case:
                info.append(str(round((aram_wins / (aram_wins + aram_losses) * 100), 2))+"%")
                info.append(aram_wins + aram_losses)
        except ZeroDivisionError as err:
            info.append("N/A")
            info.append("N/A")
        try:
            info.append(str(round((total_wins / (total_wins + total_losses) * 100), 2))+"%")
            info.append(total_wins + total_losses)
        except ZeroDivisionError as err:
            info.append("N/A")
            info.append("N/A")
        stats = [left_bar, info]
        return stats
    except ApiError as err:
        if err.response.status_code == 404:
            stats = [-1]
            print("Name doesn't exists")
        elif err.response.status_code == 429:
            stats = [-1]
            print("Rate limit exceeded")
        else:
            stats = [-1]
            print(err.response.status_code)
            print("Other error")
        return stats

