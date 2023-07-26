import pandas as pd

def calculate_composite_score(pokemon, enemy_types, df, weights=None):
    """
    Calculate a composite score for a given Pokémon against a list of enemy types.
    The composite score is a combination of type effectiveness and stat power.
    """
    if weights is None:
        weights = {
            'hp': 1,
            'attack': 1,
            'defense': 1,
            'sp_attack': 1,
            'sp_defense': 1,
            'speed': 1
        }

    pokemon_row = df[df['name'] == pokemon].iloc[0]
    
    type_score = 0
    for enemy_type in enemy_types:
        type_score += pokemon_row[f'against_{enemy_type}']

    stat_power_score = sum(pokemon_row[stat] * weight for stat, weight in weights.items())
    
    composite_score = 0.7 * type_score + 0.3 * stat_power_score

    return composite_score

def recommend_pokemon_with_scores(enemy_team, df, N=1, filters=None):
    enemy_types = list(df[df['name'].isin(enemy_team)]['type1'].values) + list(df[df['name'].isin(enemy_team)]['type2'].dropna().values)

    scores = df['name'].apply(lambda x: calculate_composite_score(x, enemy_types, df))
    
    if filters:
        for key, value in filters.items():
            df = df[df[key] == value]

    df['score'] = scores
    recommended_pokemon = df.nlargest(N, 'score')['name'].values
    recommended_scores = df.nlargest(N, 'score')['score'].values

    return recommended_pokemon, recommended_scores
