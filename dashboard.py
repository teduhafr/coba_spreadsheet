import streamlit as st
from streamlit_gsheets import GSheetsConnection
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Create a connection object.
sheet_name='dashboard'
sheet_id = '18e2A5cpq2wSXladfDhhlX1zaXR-FU5vYharZ54W__9k'

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

data_awal = pd.read_csv(url)
#get unique list dari penyelenggara
unit_penyelenggara = list(set(data_awal['Unit Penyelenggara']))
#tambahkan semua di depan
unit_penyelenggara.insert(0,"Semua")


def pilihunit (data_awal, pilihan):
    semua = 'Semua'
    if semua in pilihan:
        return data_awal
    else:
        filterunit = data_awal[data_awal['Unit Penyelenggara'].isin(pilihan)]
        return filterunit

unit_pilihan = 'Semua'

#tampilan
with st.sidebar:
    #judul
    left_co, cent_co,last_co = st.columns(3)
    st.subheader("Load Kelas")
    st.markdown("***")
    unit_option = st.multiselect(
    label="Unit Penyelenggara",
    options= unit_penyelenggara,
    default= ['Semua'])
    unit_pilihan = unit_option
    st.write("You selected:", unit_option)




# Expand the dates for each event




#munculkan di streamlite
st.subheader('Load Pekerjaan di ' + str(unit_pilihan), divider='rainbow')
if not unit_pilihan:
    st.subheader('Silakan Pilih data di Sebelah Kiri')
else:
    data = pilihunit( data_awal, unit_pilihan)
    data['Tanggal Mulai'] = pd.to_datetime(data['Tanggal Mulai'])
    data['Tanggal Selesai'] = pd.to_datetime(data['Tanggal Selesai'])

    # Create a DataFrame with all dates in the range
    all_dates = pd.date_range(start=data['Tanggal Mulai'].min(), end=data['Tanggal Selesai'].max())
    heatmap_data = pd.DataFrame(0, index=all_dates, columns=['Jumlah Kelas'])

    # Aggregate the data
    for _, row in data.iterrows():
        event_dates = pd.date_range(start=row['Tanggal Mulai'], end=row['Tanggal Selesai'])
        heatmap_data.loc[event_dates, 'Jumlah Kelas'] += row['Jumlah Kelas']
    heatmap_data['Jumlah Kelas'].plot(kind='line', figsize=(8, 4), title='Kelas')
    plt.gca().spines[['top', 'right']].set_visible(False)
    st.line_chart(heatmap_data, y="Jumlah Kelas")
