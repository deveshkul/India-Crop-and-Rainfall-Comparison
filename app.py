import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---- Load Data ----
@st.cache_data
def load_data():
    rainfall = pd.read_csv("Sub_Division_IMD_2017.csv")
    crops = pd.read_csv("crop_yield.csv")
    return rainfall, crops

rainfall_df, crop_df = load_data()

st.title("India Crop and Rainfall Comparison by Devesh")
st.markdown("Rainfall, crop production, and yield across Indian states.")

# ---- Sidebar Filters ----
states = sorted(crop_df["State"].unique())
crops = sorted(crop_df["Crop"].unique())

col1, col2 = st.columns(2)
with col1:
    state1 = st.selectbox("Select State 1", states, index=0)
    state2 = st.selectbox("Select State 2", states, index=1)
with col2:
    crop = st.selectbox("Select Crop", crops, index=0)
    years = st.slider("Select Year Range", 1997, 2017, (2005, 2015))

# ---- Filter Data ----
crop_filtered = crop_df[(crop_df["Crop"] == crop) &
                        (crop_df["Crop_Year"].between(years[0], years[1]))]

state1_data = crop_filtered[crop_filtered["State"] == state1]
state2_data = crop_filtered[crop_filtered["State"] == state2]

# ---- Rainfall Data ----
rainfall_grouped = rainfall_df.groupby(["SUBDIVISION", "YEAR"])["ANNUAL"].mean().reset_index()

rain1 = rainfall_grouped[rainfall_grouped["SUBDIVISION"].str.contains(state1, case=False, na=False)]
rain2 = rainfall_grouped[rainfall_grouped["SUBDIVISION"].str.contains(state2, case=False, na=False)]

# ---- Display Data ----
st.subheader(f"🌧 Average Rainfall ({years[0]}–{years[1]})")
col3, col4 = st.columns(2)
with col3:
    st.metric(label=f"{state1}", value=f"{rain1['ANNUAL'].mean():.2f} mm")
with col4:
    st.metric(label=f"{state2}", value=f"{rain2['ANNUAL'].mean():.2f} mm")

st.subheader(f"🌿 Crop Production & Yield Comparison: {crop}")

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(state1_data["Crop_Year"], state1_data["Production"], label=state1, marker='o')
ax[0].plot(state2_data["Crop_Year"], state2_data["Production"], label=state2, marker='o')
ax[0].set_title("Production (Tonnes)")
ax[0].legend()
ax[0].grid(True)

ax[1].plot(state1_data["Crop_Year"], state1_data["Yield"], label=state1, marker='o')
ax[1].plot(state2_data["Crop_Year"], state2_data["Yield"], label=state2, marker='o')
ax[1].set_title("Yield (Tonnes/ha)")
ax[1].legend()
ax[1].grid(True)

st.pyplot(fig)

# ---- Summary ----
st.markdown("### 📊 Insights Summary")
if not state1_data.empty and not state2_data.empty:
    st.write(f"- **{state1}**: Avg Yield = {state1_data['Yield'].mean():.2f}, Avg Production = {state1_data['Production'].mean():,.0f}")
    st.write(f"- **{state2}**: Avg Yield = {state2_data['Yield'].mean():.2f}, Avg Production = {state2_data['Production'].mean():,.0f}")
    st.write(f"- Average rainfall difference: {abs(rain1['ANNUAL'].mean() - rain2['ANNUAL'].mean()):.2f} mm")
else:
    st.warning("Data not available for the selected combination.")

# ---- Footer ----
st.markdown("---")
st.caption("Data Source: data.gov.in (IMD & Ministry of Agriculture)")


 #.\venv\Scripts\Activate
    # streamlit run app.py