import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
# from snowflake_utils import get_provider_summary
from sklearn.preprocessing import StandardScaler
from snowflake.snowpark.context import get_active_session
 
st.set_page_config(layout="wide")
st.title("Clinical Productivity & Risk Dashboard")
 
# df = get_provider_summary()
session = get_active_session()
df = session.table("ENT_AI_HACKATHON_BTWS.PERUMALLA.PROVIDER_SUMMARY").to_pandas()

# Data Preprocessing - Fill NaN values to avoid plotly breaking the chart
df["AVG_PATIENT_RISK"] = df["AVG_PATIENT_RISK"].fillna(0)
 
features = df[["TOTAL_ENCOUNTERS", "TOTAL_PROCEDURES", "AVG_PATIENT_RISK"]].fillna(0)
 
scaler = StandardScaler()
scaled = scaler.fit_transform(features)
 
kmeans = KMeans(n_clusters=3, random_state=42)
df["CLUSTER"] = kmeans.fit_predict(scaled)

# Add cluster labels
cluster_labels = {
    0: "Balanced Performer",
    1: "Procedure Heavy",
    2: "Encounter Heavy"
}
df["CLUSTER_LABEL"] = df["CLUSTER"].map(cluster_labels)

# Categorize risk into descriptive labels using quantiles
q1 = df["AVG_PATIENT_RISK"].quantile(0.33)
q2 = df["AVG_PATIENT_RISK"].quantile(0.66)
 
def categorize_risk(score):
    if score <= q1:
        return "Stable"
    elif score <= q2:
        return "Monitor"
    else:
        return "Chronic Risk"
 
df["RISK_LEVEL"] = df["AVG_PATIENT_RISK"].apply(categorize_risk)

# Remove providers with no risk score
df = df[df["AVG_PATIENT_RISK"] > 0]

# Sidebar filters
specialties = st.sidebar.multiselect("Select Specialties", options=sorted(df["SPECIALITY"].dropna().unique()), default=["GENERAL PRACTICE"])
states = st.sidebar.multiselect("Select States", options=sorted(df["STATE"].dropna().unique()))
search_name = st.sidebar.text_input("Search by Provider Name", placeholder="Enter provider name")
 
# Filter the data
if specialties:
    df = df[df["SPECIALITY"].isin(specialties)]
if states:
    df = df[df["STATE"].isin(states)]
if search_name:
    df = df[df["NAME"].str.contains(search_name, case=False, na=False)]
 
# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Providers", df["PROVIDER_ID"].nunique())
col2.metric("Avg Risk Score", round(df["AVG_PATIENT_RISK"].mean(), 2))
col3.metric("Total Procedures", int(df["TOTAL_PROCEDURES"].sum()))
 
# Bubble Chart
st.subheader("Provider Productivity vs Patient Risk")
scatter_df = df.dropna(subset=["TOTAL_ENCOUNTERS","TOTAL_PROCEDURES","AVG_PATIENT_RISK"])
if not scatter_df.empty:
    fig = px.scatter(
        scatter_df,
        x="TOTAL_ENCOUNTERS",
        y="TOTAL_PROCEDURES",
        size="AVG_PATIENT_RISK",
        color="CLUSTER_LABEL",
        hover_name="NAME",
        title="Provider Productivity Clustering"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data to display. Try adjusting the filters.")

st.subheader("Patient Risk Level Distribution")
 
risk_counts = df["RISK_LEVEL"].value_counts().reset_index()
risk_counts.columns = ["Risk Level", "Count"]
 
fig_risk = px.pie(risk_counts, names="Risk Level", values="Count", title="Risk Category Breakdown")
st.plotly_chart(fig_risk, use_container_width=True)

df = df[df["LAT"].notna() & df["LON"].notna()]

if "LAT" in df.columns and "LON" in df.columns:
    st.subheader("Provider Location Map")
    fig_map = px.scatter_mapbox(
        df,
        lat="LAT",
        lon="LON",
        color="RISK_LEVEL",
        size="AVG_PATIENT_RISK",
        hover_name="NAME",
        mapbox_style="open-street-map",
        zoom=3,
        title="Provider Locations Colored by Risk Level"
    )
    fig_map.update_layout(
        mapbox=dict(
           zoom=3,
           center={"lat":37.5, "lon":-95}
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("Location data not available in dataset.")

st.subheader("Provider Distribution by Cluster")
 
# Count providers in each cluster label
cluster_distribution = df["CLUSTER_LABEL"].value_counts().reset_index()
cluster_distribution.columns = ["Cluster Label", "Count"]
 
# Create the pie chart
fig_cluster_pie = px.pie(
    cluster_distribution,
    names="Cluster Label",
    values="Count",
    title="Provider Distribution by Cluster Type",
    hole=0.3  # Optional: creates a donut-style chart
)
 
st.plotly_chart(fig_cluster_pie, use_container_width=True)

st.subheader("Filtered Provider Table")
st.dataframe(df[[
    "NAME", "SPECIALITY", "STATE",
    "TOTAL_ENCOUNTERS", "TOTAL_PROCEDURES",
    "AVG_PATIENT_RISK", "RISK_LEVEL", "CLUSTER_LABEL"
]])
st.plotly_chart(fig, use_container_width=True)
 
# Download
st.download_button("Download Provider Summary", df.to_csv(index=False), "provider_summary.csv")
