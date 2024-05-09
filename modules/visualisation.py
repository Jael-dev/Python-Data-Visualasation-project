import pandas as pd
import matplotlib.pyplot as plt

def analyze_matches(df, start_date, end_date, championship_id):
    # Filter by date and championship
    mask = (df['date'] >= start_date) & (df['date'] <= end_date) & (df['chamionship'] == championship_id)
    filtered_df = df[mask]

    # Analyze results
    results = {}
    for i, match in filtered_df.iterrows():
        home_team, away_team = match['hometeam'], match['awayteam']
        home_score, away_score = match['home_score'], match['away_score']
        
        # Initialize teams in the dictionary if not already
        if home_team not in results:
            results[home_team] = {'wins': 0, 'losses': 0, 'draws': 0, 'matches': 0}
        if away_team not in results:
            results[away_team] = {'wins': 0, 'losses': 0, 'draws': 0, 'matches': 0}
        
        # Increment matches
        results[home_team]['matches'] += 1
        results[away_team]['matches'] += 1
        
        # Determine outcome
        if home_score > away_score:
            results[home_team]['wins'] += 1
            results[away_team]['losses'] += 1
        elif home_score < away_score:
            results[home_team]['losses'] += 1
            results[away_team]['wins'] += 1
        else:
            results[home_team]['draws'] += 1
            results[away_team]['draws'] += 1

    # Convert to DataFrame for easier manipulation and visualization
    results_df = pd.DataFrame.from_dict(results, orient='index')
    return results_df

