from riotwatcher import LolWatcher, ApiError

# app = Flask(__name__)


def champion_search(key, account, champ, game_list, match_history_list):
    watcher = LolWatcher(key)
    my_region = 'na1'
    full_team = []
    your_team = []
    latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']
    stats = []
    ranked_solo = []
    ranked_flex = []
    aram = []
    norms = []
    champion_stats = []
    ranked_solo_case = False
    ranked_flex_case = False
    norms_case = False
    aram_case = False
    match_history = False
    champs = champ.lower().split(",")
    try:
        print(game_list)
        left_bar = ["Champion"]
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

        left_bar.append("Total: Win Rate")
        left_bar.append("Total: Total Games")
        if 1 in match_history_list:
            match_history = True
        print(ranked_flex_case)
        print(ranked_solo_case)
        print(norms_case)
        print(aram_case)
        stats.append(left_bar)
        player = watcher.summoner.by_name(my_region, account)
        ranked_list = watcher.league.by_summoner(my_region, player['id'])
        my_matches = watcher.match.matchlist_by_account(my_region, player['accountId'])
        match_list = my_matches['matches']
        match_counter = 0
        print(match_list)
        aram_wins = [0] * len(champs)
        aram_losses = [0] * len(champs)
        norms_wins = [0] * len(champs)
        norms_losses = [0] * len(champs)
        ranked_solo_wins = [0] * len(champs)
        ranked_solo_losses = [0] * len(champs)
        ranked_flex_wins = [0] * len(champs)
        ranked_flex_losses = [0] * len(champs)
        champion_stats = []
        for match_counter in range(0, 100):
            current_match = match_list[match_counter]
            info = ""
            if aram_case:
                if current_match['queue'] == 450:
                    match_info = watcher.match.by_id(my_region, current_match['gameId'])
                    player_number = -1
                    for x in match_info['participantIdentities']:
                        if x['player']['summonerName'] == player['name']:
                            for a in match_info['participants']:
                                player_number += 1
                                if a['participantId'] == x['participantId']:
                                    break
                    player_game_info = match_info['participants'][player_number]
                    if player_game_info['stats']['win'] and champ_dict[
                        str(player_game_info['championId'])].lower() in champs:
                        aram_wins[champs.index(champ_dict[str(player_game_info['championId'])].lower())] += 1
                    elif champ_dict[str(player_game_info['championId'])].lower() in champs:
                        aram_losses[champs.index(champ_dict[str(player_game_info['championId'])].lower())] += 1
            if norms_case:
                if current_match['queue'] <= 410:
                    match_info = watcher.match.by_id(my_region, current_match['gameId'])
                    player_number = -1
                    for x in match_info['participantIdentities']:
                        if x['player']['summonerName'] == player['name']:
                            for a in match_info['participants']:
                                player_number += 1
                                if a['participantId'] == x['participantId']:
                                    break
                    player_game_info = match_info['participants'][player_number]
                    print(champ_dict[str(player_game_info['championId'])])
                    if player_game_info['stats']['win'] and champ_dict[
                        str(player_game_info['championId'])].lower() in champs:
                        norms_wins[champs.index(champ_dict[str(player_game_info['championId'])].lower())] += 1
                    elif champ_dict[str(player_game_info['championId'])].lower() in champs:
                        norms_losses[champs.index(champ_dict[str(player_game_info['championId'])].lower())] += 1
            if ranked_solo_case:
                if current_match['queue'] == 420:
                    match_info = watcher.match.by_id(my_region, current_match['gameId'])
                    player_number = -1
                    for x in match_info['participantIdentities']:
                        if x['player']['summonerName'] == player['name']:
                            for a in match_info['participants']:
                                player_number += 1
                                if a['participantId'] == x['participantId']:
                                    break
                    player_game_info = match_info['participants'][player_number]
                    if player_game_info['stats']['win'] and champ_dict[
                        str(player_game_info['championId'])].lower() in champs:
                        ranked_solo_wins[champs.index(champ_dict[str(player_game_info['championId'])].lower())] += 1
                    elif champ_dict[str(player_game_info['championId'])].lower() in champs:
                        ranked_solo_losses[champs.index(champ_dict[str(player_game_info['championId'])].lower())] += 1
            if ranked_flex_case:
                if current_match['queue'] not in [410, 420, 450] and not current_match['queue'] < 410:
                    match_info = watcher.match.by_id(my_region, current_match['gameId'])
                    player_number = -1
                    for x in match_info['participantIdentities']:
                        if x['player']['summonerName'] == player['name']:
                            for a in match_info['participants']:
                                player_number += 1
                                if a['participantId'] == x['participantId']:
                                    break
                    player_game_info = match_info['participants'][player_number]
                    if player_game_info['stats']['win'] and champ_dict[
                        str(player_game_info['championId'])].lower() in champs:
                        ranked_flex_wins[champs.index(champ_dict[str(player_game_info['championId'])].lower())] += 1
                    elif champ_dict[str(player_game_info['championId'])].lower() in champs:
                        ranked_flex_losses[champs.index(champ_dict[str(player_game_info['championId'])].lower())] += 1

        print(ranked_solo_wins, norms_wins)
        for champion in champs:
            champion_stats = [champion]
            try:
                if ranked_solo_case:
                    champion_stats.append(str(round((ranked_solo_wins[champs.index(champion)] / (
                            ranked_solo_wins[champs.index(champion)] + ranked_solo_losses[
                        champs.index(champion)]) * 100), 2)) + "%")
                    champion_stats.append(
                        ranked_solo_wins[champs.index(champion)] + ranked_solo_losses[champs.index(champion)])
            except ZeroDivisionError as err:
                champion_stats.append("N/A")
                champion_stats.append("N/A")

            try:
                if ranked_flex_case:
                    champion_stats.append(str(round((ranked_flex_wins[champs.index(champion)] / (
                            ranked_flex_wins[champs.index(champion)] + ranked_flex_losses[
                        champs.index(champion)]) * 100), 2)) + "%")
                    champion_stats.append(
                        ranked_flex_wins[champs.index(champion)] + ranked_flex_losses[champs.index(champion)])
            except ZeroDivisionError as err:
                champion_stats.append("N/A")
                champion_stats.append("N/A")

            try:
                if norms_case:
                    champion_stats.append(str(round((norms_wins[champs.index(champion)] / (
                            norms_wins[champs.index(champion)] + norms_losses[champs.index(champion)]) * 100), 2)) + "%")
                    champion_stats.append(norms_wins[champs.index(champion)] + norms_losses[champs.index(champion)])
            except ZeroDivisionError as err:
                champion_stats.append("N/A")
                champion_stats.append("N/A")

            try:
                if aram_case:
                    champion_stats.append(str(round((aram_wins[champs.index(champion)] / (
                            aram_wins[champs.index(champion)] + aram_losses[champs.index(champion)]) * 100), 2)) + "%")
                    champion_stats.append(aram_wins[champs.index(champion)] + aram_losses[champs.index(champion)])
            except ZeroDivisionError as err:
                champion_stats.append("N/A")
                champion_stats.append("N/A")

            try:
                champion_stats.append(str(round(((ranked_solo_wins[champs.index(champion)] +
                                              ranked_flex_wins[champs.index(champion)] +
                                              aram_wins[champs.index(champion)] +
                                              norms_wins[champs.index(champion)]) /

                                             (ranked_solo_wins[champs.index(champion)] +
                                              ranked_flex_wins[champs.index(champion)] +
                                              aram_wins[champs.index(champion)] +
                                              norms_wins[champs.index(champion)] +
                                              ranked_solo_losses[champs.index(champion)] +
                                              ranked_flex_losses[champs.index(champion)] +
                                              aram_losses[champs.index(champion)] +
                                              norms_losses[champs.index(champion)])) * 100, 2))+"%")

                champion_stats.append(ranked_solo_wins[champs.index(champion)] +
                                      ranked_flex_wins[champs.index(champion)] +
                                      aram_wins[champs.index(champion)] +
                                      norms_wins[champs.index(champion)] +
                                      ranked_solo_losses[champs.index(champion)] +
                                      ranked_flex_losses[champs.index(champion)] +
                                      aram_losses[champs.index(champion)] +
                                      norms_losses[champs.index(champion)])
            except ZeroDivisionError as err:
                champion_stats.append("N/A")
                champion_stats.append("N/A")
            stats.append(champion_stats)
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
