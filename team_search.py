from riotwatcher import LolWatcher, ApiError


def team_search(key, team):
    watcher = LolWatcher(key)
    my_region = 'na1'
    latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']
    watcher = LolWatcher(key)
    my_region = 'na1'
    full_team = []
    your_team = []
    latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
    global max_games, total_summoners
    in_game = False
    try:
        # print(team)
        max_games = int(input("How many games do you want to show"))
        assert len(team) > 0
        total_summoners = min(len(team), 5)
        for x in range(0, len(team)):
            full_team.append(watcher.summoner.by_name(my_region, team[x]))
            in_game = True

        if in_game:
            # print(total_summoners)
            player = ["Name", "Rank", "Current LP", "Win Rate", "Total Games", "Match History"]
            player_names = [""]
            your_team.append(player)
            column_ord = []
            column_wid = []
            recent_games_played = 0
            for i in range(0, total_summoners):
                player = []
                temp = 0
                assert total_summoners != 0
                person = full_team[i]

                if len(watcher.league.by_summoner(my_region, person['id'])) == 1:
                    temp = watcher.league.by_summoner(my_region, person['id'])[0]
                else:
                    if watcher.league.by_summoner(my_region, person['id'])[0]['queueType'] == "RANKED_SOLO_5x5":
                        temp = watcher.league.by_summoner(my_region, person['id'])[0]
                    else:
                        temp = watcher.league.by_summoner(my_region, person['id'])[1]

                player_names.append("Summoner " + str(i + 1))  # Summoner number
                player.append(person['name'])  # IGN
                player.append(temp['tier'] + " " + temp['rank'])  # Tier and Division ex; GOLD IV
                player.append(temp['leaguePoints'])  # LP
                player.append(round((temp['wins'] / (temp['losses'] + temp['wins']) * 100), 2))  # Win rate percentage
                player.append((temp['losses'] + temp['wins']))  # Total games
                # Adds last 10 champs played
                # player.append("Recent Match History")
                my_matches = watcher.match.matchlist_by_account(my_region, person['accountId'])
                match_counter = 0

                match_list = my_matches['matches']
                # print(match_list)
                recent_games_played = 0
                while recent_games_played < max_games:
                    if match_counter == 100:
                        break
                    current_match = match_list[match_counter]
                    match_counter += 1
                    info = ""
                    if current_match['queue'] == 420:
                        match_info = watcher.match.by_id(my_region, current_match['gameId'])
                        player_number = -1
                        for x in match_info['participantIdentities']:
                            if x['player']['summonerName'] == person['name']:
                                for a in match_info['participants']:
                                    player_number += 1
                                    if a['participantId'] == x['participantId']:
                                        break
                        # player_number += -2
                        # print(player_number)
                        player_game_info = match_info['participants'][player_number]
                        info += champ_dict[str(player_game_info['championId'])]
                        info += "  " + str(player_game_info['stats']['kills']) + "/" \
                                + str(player_game_info['stats']['deaths']) \
                                + "/" + str(player_game_info['stats']['assists']) + "\n"
                        recent_games_played += 1
                        player.append(info)

                column_wid.append(len(person['name']) * 10)
                column_ord.append(i + 1)
                your_team.append(player)
        return your_team
    except ApiError as err:
        if err.response.status_code == 404:
            in_game = False
            print("Name doesn't exist")
            return your_team
        elif err.response.status_code == 429:
            in_game = False
            print("rate limit exceeded")
            return your_team
        else:
            in_game = False
            return your_team
