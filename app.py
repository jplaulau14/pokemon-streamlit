import streamlit as st
import pandas as pd
from viz.pokemon_plots import (create_attack_defense_scatter, create_top10_pokemon_plot, 
                               create_pokemon_comparison_plot, create_type_heatmap)
from recommender.recommender import recommend_pokemon_with_scores

# Load the dataset
pokemon_df = pd.read_csv('data/pokemon 2.csv')

# Main app
def main():
    st.title("Pokémon Data Exploration App")
    st.sidebar.title("Navigation")

    page = st.sidebar.radio("Go to", ["Attack vs Defense Scatter", "Top 10 Pokémon", "Pokémon Comparison", "Type Heatmap", "Pokémon Team Recommender"])

    if page == "Attack vs Defense Scatter":
        st.header("Attack vs Defense Scatter")
        st.write("Explore the relationship between a Pokémon's attack and defense scores.")
        fig = create_attack_defense_scatter(pokemon_df)
        st.plotly_chart(fig)
    
    elif page == "Top 10 Pokémon":
        st.header("Top 10 Pokémon by Stat")
        st.write("Discover the top 10 Pokémon based on different stats. Filter the results to refine your search.")
        
        # Filters
        type1 = st.selectbox("Select Type 1", ["All"] + list(pokemon_df['type1'].unique()))
        generation = st.selectbox("Select Generation", ["All"] + list(pokemon_df['generation'].unique()))
        legendary = st.radio("Is it Legendary?", ["All", "Yes", "No"])
        stat = st.selectbox("Select Stat", ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'])

        # Apply filters
        filtered_df = pokemon_df.copy()
        if type1 != "All":
            filtered_df = filtered_df[filtered_df['type1'] == type1]
        if generation != "All":
            filtered_df = filtered_df[filtered_df['generation'] == int(generation)]
        if legendary == "Yes":
            filtered_df = filtered_df[filtered_df['is_legendary'] == 1]
        elif legendary == "No":
            filtered_df = filtered_df[filtered_df['is_legendary'] == 0]

        fig = create_top10_pokemon_plot(filtered_df, stat=stat)
        st.plotly_chart(fig)

    elif page == "Pokémon Comparison":
        st.header("Pokémon Comparison")
        st.write("Compare the stats of two Pokémon side by side.")
        
        pokemon1 = st.selectbox("Select Pokémon 1", list(pokemon_df['name']))
        pokemon2 = st.selectbox("Select Pokémon 2", list(pokemon_df['name']))
        
        if st.button("Compare"):
            fig = create_pokemon_comparison_plot(pokemon_df, pokemon1, pokemon2)
            st.plotly_chart(fig)
    
    elif page == "Type Heatmap":
        st.header("Pokémon Type Heatmap")
        st.write("See the distribution of Pokémon combinations by primary and secondary types.")
        
        fig = create_type_heatmap(pokemon_df)
        st.plotly_chart(fig)

    elif page == "Pokémon Team Recommender":
        st.header("Pokémon Team Recommender")
        st.write("Get the best Pokémon recommendations to counter an enemy team!")

        team_size = st.slider("Select the size of the enemy team", 1, 6)

        enemy_team = []
        for i in range(team_size):
            pokemon = st.selectbox(f"Select Enemy Pokémon {i + 1}", list(pokemon_df['name']))
            enemy_team.append(pokemon)

        # Filters
        type_filter = st.selectbox("Preferred Pokémon Type", ["Any"] + list(pokemon_df['type1'].unique()))
        generation_filter = st.selectbox("Preferred Pokémon Generation", ["Any"] + list(pokemon_df['generation'].unique()))
        legendary_filter = st.radio("Preferred Legendary Status", ["Any", "Yes", "No"])

        # Convert filters to a dictionary format for the recommendation function
        filters = {}
        if type_filter != "Any":
            filters['type1'] = type_filter
        if generation_filter != "Any":
            filters['generation'] = int(generation_filter)
        if legendary_filter == "Yes":
            filters['is_legendary'] = 1
        elif legendary_filter == "No":
            filters['is_legendary'] = 0

        # Get recommendations and their scores
        if st.button("Recommend"):
            recommended_pokemon, recommended_scores = recommend_pokemon_with_scores(enemy_team, pokemon_df, N=team_size, filters=filters)
            st.write(f"Recommended Pokémon to counter the enemy team: {', '.join(recommended_pokemon)}")
            
            # Display top 10 recommended Pokémon with their scores
            top_10_recommendations, top_10_scores = recommend_pokemon_with_scores(enemy_team, pokemon_df, N=10, filters=filters)
            for pokemon, score in zip(top_10_recommendations, top_10_scores):
                st.write(f"{pokemon}: Score = {score:.2f}")


if __name__ == "__main__":
    main()