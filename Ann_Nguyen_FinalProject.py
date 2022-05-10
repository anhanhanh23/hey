"""
Name:       Ann Nguyen
CS230:      Section 003
Data:       UFO Sightings
URL:        Link to your web application online

Description:

This program allows users to give input and view a brief summary of a data set
of 8000 UFO sightings in the world. Users are able to select to see the data
based on countries, shape, and duration of sightings. The app also visualized
the data using different types of charts including bar chart, pie chart, and
histogram. There are also options to view a scatter plot map of reported sightings
based on the coutry.

"""

import matplotlib as plt
import pandas as pd
import streamlit as st
import numpy as np
import pydeck as pdk
import csv

# Dataframe modification
ufo = pd.read_csv('ufo_sightings_8000_sample.csv')
df_ufo = ufo.drop(labels=6742, axis = 0)
df_ufo = ufo.dropna()
df_ufo = df_ufo.drop(df_ufo.columns[[1,6,7,8]], axis=1)
df = pd.DataFrame(df_ufo)
for s in df.index:
    df.at[s,'state'] = df.at[s,'state'].upper()
    df.at[s,'shape'] = df.at[s,'shape'].capitalize()
df.reset_index(drop=True, inplace=True)
df = df.replace('us','United States')
df = df.replace('ca','Canada')
df = df.replace('au', 'Australia')

# HTLM
st.markdown(""" <style> .font {
font-size:50px; color: #e65319;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font2 {
font-size:30px; color: navy;} 
</style> """, unsafe_allow_html=True)

# Header for the page
st.markdown('<h class="font"><b>UFO SIGHTINGS SUMMARY</b></h>', unsafe_allow_html=True)

# Header for sidebar
st.sidebar.title('INPUTS')

country = df.country.unique()
ct = df.country.value_counts()
df_country = pd.DataFrame(ct)
df_country.columns = ['Sightings']
sightings_num = df_country.Sightings.tolist()

# Prompt users to select countries
selected_countries = st.sidebar.multiselect("Please select countries:", country)

#Prompt users to select a chart type
selected_chart = st.sidebar.selectbox("Please select chart type:",["","Bar Chart", "Pie Chart"])

# Subplots
fig, ax = plt.pyplot.subplots()
fig1, ax1 = plt.pyplot.subplots()
fig2, ax2 = plt.pyplot.subplots()

st.markdown('<h class ="font2"><b>Countries</b>', unsafe_allow_html=True)
countries_l =[]
sightings_l =[]
# Loop to add countries and their # of sightings to lists and summarize data
for i in selected_countries:
    countries_l.append(i)
    n = df_country._get_value(i,'Sightings')
    sightings_l.append(n)
    st.write(f"{i} has {n} UFO sightings.")

# Create a bar chart based on the number of sightings in each country
if selected_chart == 'Bar Chart':
    if len(selected_countries) == 0:
        st.write("Please select countries.")
    else:
        selected_color = st.sidebar.radio("Please select a color:",['Coral','Orange','Green','Navy'])
        ax.bar(countries_l,sightings_l, color = selected_color)
        ax.set_title('Number of UFO Sightings by Countries')
        ax.set_xlabel('Country')
        ax.set_ylabel('Number of Sightings')
        st.pyplot(fig)

# Create a pie chart based on the number of sightings in each countries
if selected_chart == 'Pie Chart':
    if len(selected_countries) == 0:
        st.write('Please select countries.')
    else:
        ax1.pie(sightings_l, labels = countries_l, autopct= '%.2f%%')
        ax1.set_title('Percentages of UFO Sightings by Countries')
        st.pyplot(fig1)

# Dataframe for shape
st.markdown('<h class ="font2"><b>Shapes</b>', unsafe_allow_html=True)
df_shape = df[(df['shape'] != 'Other')&(df['shape'] != 'Unknown')]
df_shape = df_shape.drop(df_shape.columns[[0,1,2,4,5,6]], axis=1)
shape = df_shape.value_counts()
check = st.sidebar.checkbox('Check to view data on shapes.')
if check:
    st.write('Here is a list of identifiable shapes of UFOs and their number of sightings:')
    st.write(shape)

# List comprehension based on duration
selected_duration = st.sidebar.slider(f"Duration of sightings in seconds:",0,10000)
duration_l = [x for x in df['duration (seconds)'] if x <= selected_duration]

st.markdown('<h class ="font2"><b>Duration</b>', unsafe_allow_html=True)
# Create a histogram based on durations of sightings
if selected_duration != 0:
    st.write(f"There are {len(duration_l)} UFO sightings with a duration less than or equal to {selected_duration} seconds.")
    st.write('Top 5 Highest UFO Sighting Durations:')
    df_duration = df.sort_values(['duration (seconds)'], ascending=False)
    df_duration.reset_index(drop=True, inplace=True)
    df_topDuration = df_duration.loc[0:4,['duration (seconds)']]
    st.write(df_topDuration)
    ax2.hist(duration_l, bins = [0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000], color= 'mediumslateblue')
    ax2.set_title('Number of UFO Sightings Based on Duration (s)')
    ax2.set_ylabel('Number of sightings')
    ax2.set_xlabel('Seconds')
    ax2.set_xticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000])
    st.pyplot(fig2)

# Dataframes for maps
st.markdown('<h class ="font2"><b>Scatter Plot Maps</b>', unsafe_allow_html=True)
df_usMap = df.loc[:,['state','shape','latitude','longitude']][df.country =='United States']
df_auMap = df.loc[:,['state','shape','latitude','longitude']][df.country =='Australia']
df_caMap = df.loc[:,['state','shape','latitude','longitude']][df.country =='Canada']

# Prompt users to select a country
selected_map = st.sidebar.selectbox('Select a country to view map:', ['','United States','Canada','Australia'])

df_usMap.rename(columns={"latitude":"lat", "longitude": "lon"}, inplace= True)
df_caMap.rename(columns={"latitude":"lat", "longitude": "lon"}, inplace= True)
df_auMap.rename(columns={"latitude":"lat", "longitude": "lon"}, inplace= True)

# Create a map for the U.S.
if selected_map == 'United States':
    # Create a view of the map:
    view_state = pdk.ViewState(
    latitude=df_usMap["lat"].mean(),
    longitude=df_usMap["lon"].mean(),
    zoom=3.5,
    pitch=0)

    # Create a map layer with the given coordinates
    layer1 = pdk.Layer(type = 'ScatterplotLayer',
    data=df_usMap,
    get_position='[lon, lat]',
    get_radius=7200,
    get_color=[255,0,0],
    pickable=True
    )

    # stylish tool tip
    tool_tip = {"html": "Shape:<br/> <b>{shape}</b>",
            "style": {"backgroundColor": "white",
            "color": "navy"}
              }
    # Plot the map
    map = pdk.Deck(
    map_style='mapbox://styles/mapbox/outdoors-v11',
    initial_view_state=view_state,
    layers=[layer1],
    tooltip= tool_tip
    )
    st.pydeck_chart(map)
# Create a map for Canada
elif selected_map == 'Canada':
    # Create a view of the map:
    view_state = pdk.ViewState(
    latitude=df_caMap["lat"].mean(),
    longitude=df_caMap["lon"].mean(),
    zoom=3.5,
    pitch=0)
    # Create a map layer with the given coordinates
    layer1 = pdk.Layer(type = 'ScatterplotLayer',
    data=df_caMap,
    get_position='[lon, lat]',
    get_radius=7200,
    get_color=[255,0,0],
    pickable=True
    )
    # stylish tool tip
    tool_tip = {"html": "Shape:<br/> <b>{shape}</b>",
            "style": {"backgroundColor": "white",
            "color": "navy"}
              }
    # Plot the map
    map = pdk.Deck(
    map_style='mapbox://styles/mapbox/outdoors-v11',
    initial_view_state=view_state,
    layers=[layer1],
    tooltip= tool_tip
    )
    st.pydeck_chart(map)
# Create a map for Australia:
elif selected_map == 'Australia':
    # Create a view of the map:
    view_state = pdk.ViewState(
    latitude=df_auMap["lat"].mean(),
    longitude=df_auMap["lon"].mean(),
    zoom=3.5,
    pitch=0)
    # Create a map layer with the given coordinates
    layer1 = pdk.Layer(type = 'ScatterplotLayer',
    data=df_auMap,
    get_position='[lon, lat]',
    get_radius=7200,
    get_color=[255,0,0],
    pickable=True
    )
    # stylish tool tip
    tool_tip = {"html": "Shape:<br/> <b>{shape}</b>",
            "style": {"backgroundColor": "white",
            "color": "navy"}
              }
    # Plot the map
    map = pdk.Deck(
    map_style='mapbox://styles/mapbox/outdoors-v11',
    initial_view_state=view_state,
    layers=[layer1],
    tooltip= tool_tip
    )
    st.pydeck_chart(map)






