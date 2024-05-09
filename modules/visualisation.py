import pandas as pd
import matplotlib.pyplot as plt

def analyze_matches(df, start_date, end_date, championship_id):
    # Filter by date and championship
    mask = (df['date'] >= start_date) & (df['date'] <= end_date) & (df['championship'] == championship_id)
    filtered_df = df[mask]

    # Analyze results
    results = {}
    for i, match in filtered_df.iterrows():
        home_team, away_team = match['home_team'], match['away_team']
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

# Apply the function for Serie A 2019-2020
serie_a_results = analyze_matches(matches_df, '2019-08-24', '2020-08-02', 5)

# Plotting
serie_a_results.sort_values('matches', ascending=False).plot(kind='bar', figsize=(14, 7))
plt.title('Match Outcomes by Club for Serie A 2019-2020')
plt.xlabel('Club')
plt.ylabel('Number of Matches')
plt.show()