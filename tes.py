import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
url = "https://docs.google.com/spreadsheets/d/1K-DFoxm98JWA8U6s2DSQUfgMh1h7gH64UnSHeBVw4sY/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url)
st.dataframe(data, use_container_width=True)