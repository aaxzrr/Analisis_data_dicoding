import pandas as pd
import numpy as np
import os
import glob
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes

# Judul Dashboard
st.title("Dashboard Kualitas Udara Antar Stasiun")

folder_path = st.text_input("Masukkan path folder CSV:","analisis_data_dicoding/data")  

if os.path.exists(folder_path):
    all_files = glob.glob(folder_path + "/*.csv")
    
    df_list = []
    nan_counts = {}
    for file in all_files:
        try:
            df = pd.read_csv(file)
            if not df.empty:
                df_list.append(df)
                nan_count = df[['wd', 'WSPM', 'PM2.5', 'PM10']].isna().sum().sum()
                nan_counts[file] = nan_count
        except Exception as e:
            st.error(f'Error reading {file}: {e}')
    
    if df_list:
        data = pd.concat(df_list, ignore_index=True)
        best_file = min(nan_counts, key=nan_counts.get)
        st.write(f"File dengan jumlah NaN paling sedikit adalah: {best_file}")
        st.write(f"Jumlah NaN di file tersebut: {nan_counts[best_file]}")

        problem_selection = st.selectbox("Pilih masalah untuk dianalisis:", ["PM2.5 Analysis", "PM10 Analysis", "Wind Rose Analysis"])

        if problem_selection == "PM2.5 Analysis":
            st.subheader("Visualisasi Kualitas Udara - PM2.5")
            pm25_data = data.groupby('station')['PM2.5'].sum().reset_index()

            # Bar Chart
            st.subheader("Total PM2.5 per Stasiun")
            fig, ax = plt.subplots()
            sns.barplot(x='station', y='PM2.5', data=pm25_data, ax=ax)
            ax.set_title('Total PM2.5 per Station')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Grouped Boxplot
            st.subheader("Distribusi Tingkat PM2.5 per Stasiun")
            fig, ax = plt.subplots()
            sns.boxplot(x='station', y='PM2.5', data=data, ax=ax)
            ax.set_title('PM2.5 Levels Distribution per Station')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Multiseries Line Plot
            st.subheader("Tren PM2.5 di Beberapa Stasiun")
            fig, ax = plt.subplots()
            for station in data['station'].unique():
                subset = data[data['station'] == station]
                ax.plot(subset.index, subset['PM2.5'], label=station)

            ax.set_title('PM2.5 Trend Across Stations')
            ax.set_xlabel('Time Index')
            ax.set_ylabel('PM2.5 Level')
            ax.legend()
            st.pyplot(fig)

        # Analisis PM10
        elif problem_selection == "PM10 Analysis":
            st.subheader("Visualisasi Kualitas Udara - PM10")
            pm10_data = data.groupby('station')['PM10'].sum().reset_index()

            # Bar Chart
            st.subheader("Total PM10 per Stasiun")
            fig, ax = plt.subplots()
            sns.barplot(x='station', y='PM10', data=pm10_data, ax=ax)
            ax.set_title('Total PM10 per Station')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Grouped Boxplot
            st.subheader("Distribusi Tingkat PM10 per Stasiun")
            fig, ax = plt.subplots()
            sns.boxplot(x='station', y='PM10', data=data, ax=ax)
            ax.set_title('PM10 Levels Distribution per Station')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Multiseries Line Plot
            st.subheader("Tren PM10 di Beberapa Stasiun")
            fig, ax = plt.subplots()
            for station in data['station'].unique():
                subset = data[data['station'] == station]
                ax.plot(subset.index, subset['PM10'], label=station)

            ax.set_title('PM10 Trend Across Stations')
            ax.set_xlabel('Time Index')
            ax.set_ylabel('PM10 Level')
            ax.legend()
            st.pyplot(fig)

       
    else:
        st.warning("Tidak ada data untuk ditampilkan.")
else:
    st.error("Folder tidak ditemukan. Silakan masukkan path yang benar.")

