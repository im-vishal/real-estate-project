from pathlib import Path

import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Apartments")

app_dir = Path(__file__).parent.parent
data_dir = app_dir / 'datasets'

location_df = joblib.load(data_dir / 'location_df.joblib')
cosine_sim_facilities = joblib.load(data_dir / 'cosine_sim_facilities.joblib')
cosine_sim_price = joblib.load(data_dir / 'cosine_sim_price.joblib')
cosine_sim_location = joblib.load(data_dir / 'cosine_sim_location.joblib')

def recommend_properties_with_scores(property_name, top_n=247):
    
    cosine_sim_matrix = 30*cosine_sim_facilities + 20*cosine_sim_price + 8*cosine_sim_location
    # cosine_sim_matrix = cosine_sim3
    
    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    
    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
    
    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()
    
    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })
    
    return recommendations_df



# st.dataframe(location_df)

st.title('Select Location and Radius')

selected_location = st.selectbox('Location', sorted(location_df.columns.to_list()))

radius = st.number_input('Radius in Kms')


# Check if 'results' key exists in session state
if 'results' not in st.session_state:
    st.session_state['results'] = None

if st.button('Search'):
    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()

    appartments = []
    distance = []
    for key, val in result_ser.items():
        appartments.append(str(key))
        distance.append(str(round(val / 1000)) + ' kms')

    # Store results in session state
    st.session_state['results'] = (appartments, distance)

# Retrieve results from session state
if st.session_state['results']:
    appartments, distance = st.session_state['results']

    selected_appartment = st.radio(
        'Select any Appartment for recommendation',
        appartments,
        captions=distance
        # format_func=lambda x: f"{x} ({distance[appartments.index(x)]})"
    )

    if st.button('Recommend'):
        st.text('Below are recommended Appartments based on your selection...')
        recommendation_df = recommend_properties_with_scores(selected_appartment)
        recommendation_df['SimilarityScore'] = recommendation_df['SimilarityScore'].round(2)
        st.dataframe(recommendation_df.head(10), hide_index=True)