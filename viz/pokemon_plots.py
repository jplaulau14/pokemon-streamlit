import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_attack_defense_scatter(df):
    # Create scatter plot
    fig = px.scatter(
        df, 
        x="attack", 
        y="defense", 
        color="type1", 
        size='hp', 
        hover_data=['name'], 
        title='Attack vs Defense Colored by Type 1 and Sized by HP',
        labels={
            'attack': 'Attack Score',
            'defense': 'Defense Score',
            'type1': 'Primary Type',
            'hp': 'Health Points'
        },
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=600,
        width=800
    )

    return fig

def create_top10_pokemon_plot(df, type1=None, generation=None, legendary=None, stat='total'):
    # Apply filters
    if type1:
        df = df[df['type1'] == type1]
    if generation:
        df = df[df['generation'] == generation]
    if legendary is not None:
        df = df[df['is_legendary'] == legendary]

    # Sort by selected stat and take top 10
    top10_df = df.sort_values(by=stat, ascending=False).head(10)

    # Create bar plot
    fig = px.bar(
        top10_df, 
        x='name', 
        y=stat, 
        color=stat, 
        title=f'Top 10 Pokémon by {stat}', 
        labels={'name': 'Pokémon', stat: stat},
        color_continuous_scale='Bluered_r'
    )

    return fig

def create_pokemon_comparison_plot(df, pokemon1, pokemon2):
    # Get the stats for the selected Pokémon
    pokemon1_stats = df[df['name'] == pokemon1][['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].iloc[0]
    pokemon2_stats = df[df['name'] == pokemon2][['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].iloc[0]

    # Create DataFrame for the plot
    comparison_df = pd.DataFrame({'Stat': pokemon1_stats.index, 'Pokemon 1': pokemon1_stats.values, 'Pokemon 2': pokemon2_stats.values})

    # Create bar plot
    fig = go.Figure(data=[
        go.Bar(name=pokemon1, x=comparison_df['Stat'], y=comparison_df['Pokemon 1'], marker_color='green'),
        go.Bar(name=pokemon2, x=comparison_df['Stat'], y=comparison_df['Pokemon 2'], marker_color='red')
    ])

    # Change the bar mode
    fig.update_layout(barmode='group', title_text='Comparison of Pokémon Stats')

    return fig

def create_type_heatmap(df):
    # Create a pivot table for the number of Pokémon for each combination of Type 1 and Type 2
    type_pivot = df.pivot_table(index='type1', columns='type2', aggfunc='size')

    # Create heatmap
    fig = px.imshow(
        type_pivot, 
        labels=dict(x="Type 2", y="Type 1", color="Number of Pokémon"), 
        title="Heatmap of Pokémon Types",
        height=800,  # Increase the height
        width=1000   # Increase the width
    )

    return fig
