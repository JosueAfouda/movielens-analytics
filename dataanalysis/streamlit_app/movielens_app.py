import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide",
    page_title="MovieLens Data Analysis",
    page_icon="🎬"  # Emoji Unicode directement
)

# Navigation
page_1 = st.Page("page1.py", title="Overview", icon="🎬")     # Film clapperboard
page_2 = st.Page("page2.py", title="Tags Insights", icon="📊")  # Bar chart

pg = st.navigation([page_1, page_2])
pg.run()
