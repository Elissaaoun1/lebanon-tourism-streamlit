
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Lebanon Tourism Explorer", page_icon="🗺️", layout="wide")

@st.cache_data
def load_data():
    towns = pd.read_csv("data/tourism_clean.csv")
    gov = pd.read_csv("data/tourism_by_governorate.csv")
    return towns, gov

towns, gov = load_data()

st.title("🗺️ Lebanon Tourism Explorer")
st.markdown("""
This app is based on your tourism dataset. It provides **two related visualizations** with **interactive controls**:
1) A **comparison chart** across governorates for the selected supply metric (Hotels, Cafes, Restaurants, Guest houses).
2) A **relationship view** (scatter) to see how two infrastructure metrics relate (e.g., Hotels vs Cafes), with optional color by Tourism Index.

Use the controls in the sidebar to filter and change the view. All interactions **directly impact** the charts.
""")

with st.sidebar:
    st.header("Controls")
    # Governorate filter
    all_govs = sorted(gov["Governorate"].unique().tolist())
    selected_govs = st.multiselect("Governorates", all_govs, default=all_govs)

    # Metric selection for bar
    metric = st.selectbox("Bar Metric", ["hotels","cafes","restaurants","guest_houses"], index=0, help="Choose which metric to compare across governorates.")

    # Scatter axes selection
    x_axis = st.selectbox("Scatter X", ["hotels","cafes","restaurants","guest_houses"], index=0)
    y_axis = st.selectbox("Scatter Y", ["cafes","hotels","restaurants","guest_houses"], index=1)

    # Tourism Index threshold
    idx_min, idx_max = float(towns["tourism_index"].min()), float(towns["tourism_index"].max())
    idx_range = st.slider("Tourism Index filter (towns-level used for color)", min_value=idx_min, max_value=idx_max, value=(idx_min, idx_max), step=0.5)

# Apply filters
gov_f = gov[gov["Governorate"].isin(selected_govs)].copy()
towns_f = towns[towns["Governorate"].isin(selected_govs)].copy()
towns_f = towns_f[(towns_f["tourism_index"] >= idx_range[0]) & (towns_f["tourism_index"] <= idx_range[1])]

# Visualization 1: Bar by governorate for selected metric
bar_title = f"{metric.replace('_',' ').title()} by Governorate"
fig_bar = px.bar(
    gov_f.sort_values(metric, ascending=False),
    x="Governorate", y=metric,
    title=bar_title
)
st.plotly_chart(fig_bar, use_container_width=True)

# Visualization 2: Scatter relationship (aggregated to governorate for clearer pattern)
# Compute governorate-level for chosen axes
scatter_df = gov_f[["Governorate", x_axis, y_axis]].copy()
# Merge an average tourism index for color (optional)
avg_idx = towns_f.groupby("Governorate", as_index=False)["tourism_index"].mean().rename(columns={"tourism_index":"avg_tourism_index"})
scatter_df = scatter_df.merge(avg_idx, on="Governorate", how="left")

fig_scatter = px.scatter(
    scatter_df,
    x=x_axis, y=y_axis, color="avg_tourism_index",
    hover_name="Governorate",
    title=f"{x_axis.replace('_',' ').title()} vs {y_axis.replace('_',' ').title()} (color: avg Tourism Index)",
    trendline="ols"
)
st.plotly_chart(fig_scatter, use_container_width=True)

with st.expander("Insights & Tips"):
    st.markdown("""
    - **Compare supply**: Use the **Bar Metric** selector to see which governorates lead in *Hotels/Cafes/Restaurants/Guest houses*.
    - **Relationship**: The **scatter** helps confirm the **positive relationship** you observed (e.g., Hotels vs Cafes). Toggle axes to explore other pairs.
    - **Tourism Index**: Narrow the **Index filter** to check if higher-index governorates also have higher infrastructure.
    - **Governorate focus**: Use the **Governorates** multiselect to focus on specific areas like *Mount Lebanon, South, Baalbek-Hermel* vs *Bekaa, Nabatieh*.
    """)

st.caption("Data cleaning: normalized Governorate from refArea URIs; summed infrastructure metrics per governorate; averaged tourism index.")
