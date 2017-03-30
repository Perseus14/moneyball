import net_util
import json
import csv
from unidecode import unidecode
import os


def getTeams(dump):
    script_dir = os.path.dirname(__file__)
    team_dict = {}
    rel_path = "Data/teams.csv"
    abs_file_path = os.path.join(script_dir, rel_path)     
    f = csv.writer(open(abs_file_path, "wb+"))
    f.writerow(["id", "code", "name", "strength", "strength_overall_home", 
        "strength_overall_away", "strength_attack_home", "strength_attack_away",
        "strength_defence_home", "strength_defence_away"])    
    for team in dump["teams"]:
        #create code to id dictionary for team identification
        team_dict[team["code"]] = team["id"] - 1
        f.writerow([team["id"], team["code"], team["name"], team["strength"], 
            team["strength_overall_home"], team["strength_overall_away"], 
            team["strength_attack_home"], team["strength_attack_away"],
            team["strength_defence_home"], team["strength_defence_away"]]) 
    return team_dict
            

def getPlayers(dump, team_dict):
    script_dir = os.path.dirname(__file__)
    base_url = 'https://fantasy.premierleague.com/drf/element-summary/'
    #there are 616 players in the league
    for i in range(1, 617):               
        resource = '{0}'.format(i)
        response = net_util.call_api(resource, None, base_url)
        player = json.loads(response)    
        rel_path = "Data/Players/player_{0}.csv".format(i)
        abs_file_path = os.path.join(script_dir, rel_path)                
        f = csv.writer(open(abs_file_path, "wb+"))
        f.writerow(["id", "first_name", "second_name", "team_code", "team_name", "type",
            "cost", "status", "total_points",
            "round", "kickoff_time", "opp_team_id", "opp_team_name", "was_home", "team_h_score", "team_a_score", "strength_overall_home",
            "strength_overall_away", "strength_attack_home", "strength_attack_away",
            "strength_defence_home", "strength_defence_away", "opp_strength_overall_home",
            "opp_strength_overall_away", "opp_strength_attack_home", "opp_strength_attack_away",
            "opp_strength_defence_home", "opp_strength_defence_away",
            "minutes", "yellow_cards", "red_cards", "goals_scored",
            "own_goals", "fouls", "dribbles",
            "saves", "clean_sheets", "goals_conceded", "penalties_saved",
            "errors_leading_to_goal", "errors_leading_to_goal_attempt",
            "clearances_blocks_interceptions", "penalties_conceded", "tackles",
            "recoveries",
            "big_chances_missed", "offside", "open_play_crosses", "big_chances_created",
            "key_passes", "attempted_passes", "completed_passes", "assists", "penalties_missed",
            "tackled", "target_missed", "points"])
        ply = dump["elements"][i-1]
        for fixture in player["history"]:   
            #home code
            home = dump["teams"][team_dict[ply["team_code"]]]
            #opponent code
            opp = dump["teams"][fixture["opponent_team"] - 1]
            f.writerow([ply["id"], unidecode(ply["first_name"]), unidecode(ply["second_name"]), ply["team_code"], home["name"], ply["element_type"],
                ply["now_cost"], ply["status"], ply["total_points"],
                fixture["round"], fixture["kickoff_time_formatted"], fixture["opponent_team"], opp["name"], fixture["was_home"], fixture["team_h_score"], fixture["team_a_score"], home["strength_overall_home"],
                home["strength_overall_away"], home["strength_attack_home"], home["strength_attack_away"],
                home["strength_defence_home"], home["strength_defence_away"], opp["strength_overall_home"],
                opp["strength_overall_away"], opp["strength_attack_home"], opp["strength_attack_away"],
                opp["strength_defence_home"], opp["strength_defence_away"],
                fixture["minutes"], fixture["yellow_cards"], fixture["red_cards"], fixture["goals_scored"],
                fixture["own_goals"], fixture["fouls"], fixture["dribbles"],
                fixture["saves"], fixture["clean_sheets"], fixture["goals_conceded"], fixture["penalties_saved"],
                fixture["errors_leading_to_goal"], fixture["errors_leading_to_goal_attempt"],
                fixture["clearances_blocks_interceptions"], fixture["penalties_conceded"], fixture["tackles"],
                fixture["recoveries"],
                fixture["big_chances_missed"], fixture["offside"], fixture["open_play_crosses"], fixture["big_chances_created"],
                fixture["key_passes"], fixture["attempted_passes"], fixture["completed_passes"], fixture["assists"], fixture["penalties_missed"],
                fixture["tackled"], fixture["target_missed"], fixture["total_points"]])   
        next_fixture = player["fixtures_summary"][0]
        home = dump["teams"][team_dict[ply["team_code"]]]
        opp = dump["teams"][next_fixture["team_a"] - 1]        
        f.writerow([ply["id"], unidecode(ply["first_name"]), unidecode(ply["second_name"]), ply["team_code"], 
                home["name"], ply["element_type"], ply["now_cost"], ply["status"], ply["total_points"], next_fixture["event"], 
                next_fixture["kickoff_time_formatted"], next_fixture["team_a"], 
                next_fixture["opponent_name"], next_fixture["is_home"], "", "", home["strength_overall_home"],
                home["strength_overall_away"], home["strength_attack_home"], home["strength_attack_away"],
                home["strength_defence_home"], home["strength_defence_away"], opp["strength_overall_home"],
                opp["strength_overall_away"], opp["strength_attack_home"], opp["strength_attack_away"],
                opp["strength_defence_home"], opp["strength_defence_away"]])
        print "Got player {0}".format(i)
    return None

    
def getGameweeks(dump):
    script_dir = os.path.dirname(__file__)
    rel_path = "Data/gameweeks.csv"
    abs_file_path = os.path.join(script_dir, rel_path)     
    f = csv.writer(open(abs_file_path, "wb+"))
    f.writerow(["id", "average_points", "highest_points"])    
    for gameweek in dump["events"]:
        f.writerow([gameweek["id"], gameweek["average_entry_score"], gameweek["highest_score"]])
    return None         

if __name__ == '__main__':
    #get the entire data dump of teams, players and fixtures
    base_url = 'https://fantasy.premierleague.com/drf/bootstrap-static'   
    resource = ''
    response = net_util.call_api(resource, None, base_url)
    dump = json.loads(response)                
    #get team data
    team_dict = getTeams(dump)
    #get player data
    getPlayers(dump, team_dict)
    #get gameweek data of fantasy team performance
    getGameweeks(dump)
