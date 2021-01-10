from riotwatcher import LolWatcher, ApiError

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


def your_search(account, game_list):
    stats = []
    ranked_solo_case = False
    ranked_flex_case = False
    norms_case = False
    aram_case = False
    try:
        aram = []
        norms = []
        ranked_solo = []
        ranked_flex = []
        print(game_list)
        if '1' in game_list:
            ranked_solo_case = True
        if '2' in game_list:
            ranked_flex_case = True
        if '3' in game_list:
            norms_case = True
        if '4' in game_list:
            aram_case = True
        print(ranked_solo_case)
        print(ranked_flex_case)
        print(norms_case)
        print(aram_case)

        player = watcher.summoner.by_name(my_region, account)
        ranked_list = watcher.league.by_summoner(my_region, player['id'])
        my_matches = watcher.match.matchlist_by_account(my_region, player['accountId'])
        match_list = my_matches['matches']
        match_counter = 0
        aram_wins = 0
        aram_losses = 0
        norms_wins = 0
        norms_losses = 0
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
                    if player_game_info['stats']['win']:
                        aram_wins += 1
                    else:
                        aram_losses += 1
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
                    if player_game_info['stats']['win']:
                        norms_wins += 1
                    else:
                        norms_losses += 1

        if not watcher.league.by_summoner(my_region, player['id']):
            ranked_solo = ["Ranked Solo/Duo", "N/A", "N/A", "N/A", "N/A"]
            ranked_flex = ["Ranked Flex", "N/A", "N/A", "N/A", "N/A"]
            print(watcher.league.by_summoner(my_region, player['id'])[1]['queueType'])
        elif watcher.league.by_summoner(my_region, player['id'])[0][
            'queueType'] == "RANKED_SOLO_5x5" and ranked_solo_case:
            ranked_solo = ["Ranked Solo/Duo"]
            print("poop")
            solo_info = watcher.league.by_summoner(my_region, player['id'])[0]
            ranked_solo.append(solo_info['tier'] + " " + solo_info['rank'])  # Tier and Division ex; GOLD IV
            ranked_solo.append(solo_info['leaguePoints'])  # LP
            ranked_solo.append(round((solo_info['wins'] / (solo_info['losses'] + solo_info['wins']) * 100), 2))
            ranked_solo.append((solo_info['losses'] + solo_info['wins']))  # Total games
            ranked_flex = ["N/A", "N/A", "N/A", "N/A"]
            if len(watcher.league.by_summoner(my_region, player['id'])) > 1 and ranked_flex_case:
                flex_info = watcher.league.by_summoner(my_region, player['id'])[1]
                ranked_flex = ["Ranked Flex", flex_info['tier'] + " " + flex_info['rank'], flex_info['leaguePoints'],
                               round((flex_info['wins'] / (flex_info['losses'] + flex_info['wins']) * 100), 2),
                               (flex_info['losses'] + flex_info['wins'])]
        elif len(watcher.league.by_summoner(my_region, player['id'])) > 1 and ranked_flex_case:
            flex_info = watcher.league.by_summoner(my_region, player['id'])[1]
            ranked_flex = ["Ranked Flex", flex_info['tier'] + " " + flex_info['rank'], flex_info['leaguePoints'],
                           round((flex_info['wins'] / (flex_info['losses'] + flex_info['wins']) * 100), 2),
                           (flex_info['losses'] + flex_info['wins'])]
        elif ranked_flex_case:
            ranked_flex = ["Ranked Flex"]
            flex_info = watcher.league.by_summoner(my_region, player['id'])[0]
            ranked_flex.append(flex_info['tier'] + " " + flex_info['rank'])  # Tier and Division ex; GOLD IV
            ranked_flex.append(flex_info['leaguePoints'])  # LP
            ranked_flex.append(round((flex_info['wins'] / (flex_info['losses'] + flex_info['wins']) * 100), 2))
            ranked_flex.append((flex_info['losses'] + flex_info['wins']))  # Total games
            ranked_solo = ["N/A", "N/A", "N/A", "N/A"]
            if len(watcher.league.by_summoner(my_region, player['id'])) > 1 and ranked_solo_case:
                solo_info = watcher.league.by_summoner(my_region, player['id'])[1]
                ranked_solo = ["Ranked Solo/Duo", solo_info['tier'] + " " + solo_info['rank'],
                               solo_info['leaguePoints'],
                               round((solo_info['wins'] / (solo_info['losses'] + solo_info['wins']) * 100), 2),
                               (solo_info['losses'] + solo_info['wins'])]
        elif len(watcher.league.by_summoner(my_region, player['id'])) > 1 and ranked_solo_case:
            solo_info = watcher.league.by_summoner(my_region, player['id'])[1]
            ranked_solo = ["Ranked Solo/Duo", solo_info['tier'] + " " + solo_info['rank'], solo_info['leaguePoints'],
                           round((solo_info['wins'] / (solo_info['losses'] + solo_info['wins']) * 100), 2),
                           (solo_info['losses'] + solo_info['wins'])]

        norms = ["Norms", "N/A", "N/A"]
        try:
            norms.append(round((norms_wins / (norms_wins + norms_losses) * 100), 2))
            norms.append(norms_wins + norms_losses)
        except ZeroDivisionError as err:
            norms.append("N/A")
            norms.append("N/A")

        aram = ["Aram", "N/A", "N/A"]
        try:
            aram.append(round((aram_wins / (aram_wins + aram_losses) * 100), 2))
            aram.append(aram_wins + aram_losses)
        except ZeroDivisionError as err:
            aram.append("N/A")
            aram.append("N/A")

        header = [account, "Ranked Solo/Duo", "Ranked Flex", "Norms", "ARAM"]

        left_bar = ["", "Rank", "LP", "Win Rate", "Total Games"]

        stats.append(left_bar)
        if ranked_solo_case:
            stats.append(ranked_solo)
        if ranked_flex_case:
            stats.append(ranked_flex)
        if norms_case:
            stats.append(norms)
        if aram_case:
            stats.append(aram)

        # fig = go.Figure(data=[go.Table(
        #     header=dict(values=header,
        #                 line_color='darkslategray',
        #                 fill_color='lightgray',
        #                 align='left',
        #                 font=dict(color='white', size=12),
        #                 height=40),
        #     cells=dict(
        #         values=stats, line_color='darkslategray', fill_color='white', align='left',
        #         font_size=12,
        #         height=30))
        # ])
        #
        # fig.update_layout(width=800, height=1000)
        # fig.show()
        return stats
    except ApiError as err:
        if err.response.status_code == 404:
            stats = [-2]
            print("Name doesn't exists")
        elif err.response.status_code == 429:
            stats = [-1]
            print("Rate limit exceeded")
        else:
            stats = [-1]
            print(err.response.status_code)
            print("Other error")
        return stats
