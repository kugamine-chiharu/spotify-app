import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plot
import seaborn as sns


st.markdown("<h2 style='text-align: center; color: white;'>Wrapped in Python </h2>", unsafe_allow_html=True)
st.markdown(":blue[This application will go over your spotify listening trends and give you insight into your habits and listening history]")

uploaded_file = st.file_uploader("Upload your `StreamingHistory.json` file from Spotify", type="json")

if uploaded_file:
    data = json.load(uploaded_file)

    df = pd.DataFrame(data)

    df = df[df['master_metadata_track_name'].notna()]

    df = df[df['ms_played'] >= 15000]  # Only keep plays >= 15 seconds cuz

    df['ts'] = pd.to_datetime(df['ts'])
    df['minutes_played'] = df['ms_played'] / 60000
    df['hours_played'] = df['ms_played'] / 3600000
    df['date'] = df['ts'].dt.date

    st.write("file uploaded successfully")

    total_hours = df['hours_played'].sum()
    total_tracks = len(df)
    total_unique_artists = df['master_metadata_album_artist_name'].nunique()
    
    

    col1, col2, col3 = st.columns(3,border = True,gap="medium")
    col1.metric("you've listened to songs for", f"{total_hours:.2f} hours..")
    col2.metric("you've played ", f"{total_tracks} different songs....")
    col3.metric("you've listened to ", f"{total_unique_artists} different artists")
    
    container = st.container(border=True)

    top_artists = df.groupby('master_metadata_album_artist_name')['hours_played'].sum().sort_values(ascending=False).head(10)
    with container:
        st.subheader("Your top 10 artists for this month: ")
        st.bar_chart(top_artists,y_label="Hours",x_label="Artists",)

    container2 = st.container(border=True)

    daily_listening = df.groupby('date')['minutes_played'].sum()
    with container2:
        st.subheader("Listening Time Per Day:")
        st.line_chart(daily_listening, x_label= "Dates",y_label="Minutes")
    
    
    top_albums = (
    df.groupby('master_metadata_album_album_name')['minutes_played'].sum().sort_values(ascending=False).head(6))
    top_albums = top_albums.dropna()


    
    container3 = st.container(border = True)
    with container3:

        fig, ax = plot.subplots()
        fig.patch.set_facecolor('black') 
        ax.set_facecolor('black')    

        wedges,texts,autotexts = ax.pie(top_albums,labels=top_albums.index,autopct='%1.1f%%',startangle=90,wedgeprops={'edgecolor': 'white'})
        ax.set_title("Top 6 Most Listened Albums",color = "white")
        for text in texts + autotexts:
            text.set_color('white')
            
        st.pyplot(fig)
    
    container4 = st.container(border = True)
    with container4:
        st.subheader("Your top 10 most played Tracks:")

        top_tracks = (df.groupby('master_metadata_track_name')['minutes_played'].sum().sort_values(ascending=False).head(10))
        top_tracks = top_tracks[::-1]

        st.bar_chart(top_tracks, y_label="Minutes", x_label="Track Name", use_container_width=True)




