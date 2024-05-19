import pandas as pd
import matplotlib.pyplot as plt

def calculate_gains(row):
    default_loss = -1

    if pd.notna(row['quotation_home']) and pd.notna(row['quotation_away']) and pd.notna(row['quotation_draw']):
        if row['home_score'] > row['away_score']:
            return (1 * row['quotation_home']) - 1
        elif row['home_score'] < row['away_score']:
            return (1 * row['quotation_away']) - 1
        else:
            return (1 * row['quotation_draw']) - 1
    else:
        return default_loss