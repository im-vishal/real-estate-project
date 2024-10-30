import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from wordcloud import WordCloud
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# plt.style.use('ggplot')

plt.rcParams['figure.facecolor'] = (0, 0, 0, 0)  # Set figure background to transparent
plt.rcParams['axes.facecolor'] = (0, 0, 0, 0)    # Set axes background to transparent

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

app_dir = Path(__file__).parent.parent
data_dir = app_dir / 'datasets'

new_df = pd.read_csv(data_dir / 'data_viz1.csv')
feature_text = joblib.load(data_dir / 'feature_text.joblib')

dfg = new_df[['sector', 'price','price_per_sqft','built_up_area','latitude','longitude']].copy()

group_df = dfg.groupby('sector').mean()[['price','price_per_sqft','built_up_area','latitude','longitude']]

st.header('Sector Price per Sqft Geomap')

fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)

st.header('Features Wordcloud')

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='black',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

# Create a figure
fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)

# Display the figure in Streamlit
st.pyplot(fig)

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)



st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side KdePlot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.kdeplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.kdeplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
plt.grid(visible=False)
st.pyplot(fig3)