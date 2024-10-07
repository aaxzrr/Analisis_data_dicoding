import numpy as np
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import streamlit as st

# Function to remove outliers
def remove_outliers(df):
    for col in ['PM2.5', 'PM10']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    return df

# Set up the Streamlit app
st.title("Air Quality Data Analysis Dashboard")

# Mode selection
mode = st.radio("Select Mode", ('Wind Rose Plot', 'Pollutant Distribution'))

if mode == 'Wind Rose Plot':
    # Upload a single CSV file
    uploaded_file = st.file_uploader("Upload a CSV file for Wind Rose Plot", type='csv')
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Data Cleaning
        cleaned_data = df.dropna()
        cleaned_data = remove_outliers(cleaned_data)

        # Map wind directions to numeric values
        cleaned_data['wd'] = cleaned_data['wd'].map({'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
                                                      'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
                                                      'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
                                                      'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5})
        
        # Convert wind direction to numeric
        cleaned_data['wd'] = pd.to_numeric(cleaned_data['wd'], errors='coerce')

        # Wind rose for PM10
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(projection='windrose'))
        ax.bar(cleaned_data['wd'], cleaned_data['PM10'], normed=True, 
               opening=0.8, edgecolor='white')
        ax.set_title('Wind Rose for PM10')
        ax.set_legend()
        st.pyplot(fig)

        # Wind rose for Wind Speed
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(projection='windrose'))
        ax.bar(cleaned_data['wd'], cleaned_data['WSPM'], normed=True, 
               opening=0.8, edgecolor='white')
        ax.set_title('Wind Rose for Wind Speed')
        ax.set_legend()
        st.pyplot(fig)

elif mode == 'Pollutant Distribution':
    # Upload multiple CSV files
    uploaded_files = st.file_uploader("Upload CSV files for Pollutant Distribution", type='csv', accept_multiple_files=True)

    if uploaded_files:
        df_list = []
        
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file)
            df_list.append(df)

        # Concatenate all dataframes
        data = pd.concat(df_list, ignore_index=True)

        # Data Cleaning
        cleaned_data = data.dropna()
        cleaned_data = remove_outliers(cleaned_data)

        # Pollutant Distribution Visualization
        st.subheader("Pollutant Distribution Across Stations")

        # Total PM2.5 and PM10 per Station
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        sns.barplot(x='station', y='PM2.5', data=cleaned_data, ax=axes[0], estimator=sum)
        axes[0].set_title('Total PM2.5 per Station')
        axes[0].set_ylabel('Total PM2.5')
        axes[0].tick_params(axis='x', rotation=45)
        
        sns.barplot(x='station', y='PM10', data=cleaned_data, ax=axes[1], estimator=sum)
        axes[1].set_title('Total PM10 per Station')
        axes[1].set_ylabel('Total PM10')
        axes[1].tick_params(axis='x', rotation=45)
        
        st.pyplot(fig)

        # Boxplots for PM2.5 and PM10
        st.subheader("PM2.5 and PM10 Levels Distribution per Station")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        sns.boxplot(x='station', y='PM2.5', data=cleaned_data, ax=axes[0])
        axes[0].set_title('PM2.5 Levels Distribution per Station')
        axes[0].set_ylabel('PM2.5 Level')
        axes[0].tick_params(axis='x', rotation=45)
        
        sns.boxplot(x='station', y='PM10', data=cleaned_data, ax=axes[1])
        axes[1].set_title('PM10 Levels Distribution per Station')
        axes[1].set_ylabel('PM10 Level')
        axes[1].tick_params(axis='x', rotation=45)
        
        st.pyplot(fig)

        # Trend plots for PM2.5 and PM10
        st.subheader("PM2.5 and PM10 Trend Across Stations")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        for station in cleaned_data['station'].unique():
            subset = cleaned_data[cleaned_data['station'] == station]
            axes[0].plot(subset.index, subset['PM2.5'], label=station)

        axes[0].set_title('PM2.5 Trend Across Stations')
        axes[0].set_xlabel('Time Index')
        axes[0].set_ylabel('PM2.5 Level')
        axes[0].legend()
        
        for station in cleaned_data['station'].unique():
            subset = cleaned_data[cleaned_data['station'] == station]
            axes[1].plot(subset.index, subset['PM10'], label=station)

        axes[1].set_title('PM10 Trend Across Stations')
        axes[1].set_xlabel('Time Index')
        axes[1].set_ylabel('PM10 Level')
        axes[1].legend()
        
        st.pyplot(fig)
