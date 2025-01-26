import requests



# Raise an exception if the status code is not 200 (OK)

# Parse the JSON response body


def get_astros_scores():
    response = requests.get('http://localhost:3000/api/astros-playing')

    data = response.json()
    if data["playing"] == False:
        return None
    
    teams = data["game"]["teams"]
    
    # Determine which team is the Astros
    if teams["away"]["team"]["name"] == "Houston Astros":
        astros = teams["away"]
        other_team = teams["home"]
    else:
        astros = teams["home"]
        other_team = teams["away"]
    
    astros_score = f'{astros["score"]} - {astros["team"]["name"]}'
    other_team_score = f'{other_team["score"]} - {other_team["team"]["name"]}'
    
    return astros_score, other_team_score

print(get_astros_scores())