import streamlit as st
chart_type = st.radio("Chart type", ["Bar", "Pie"], horizontal=True)
gov_col = mapping["governorate"]


if chart_type == "Bar":
fig = px.bar(
agg, x=gov_col, y=metric_col,
title=f"{metric} by Governorate",
labels={gov_col: "Governorate", metric_col: metric},
text_auto=True,
)
fig.update_layout(height=500, xaxis_tickangle=-30)
st.plotly_chart(fig, use_container_width=True)
else:
fig = px.pie(
agg, names=gov_col, values=metric_col,
title=f"{metric} share by Governorate", hole=0.3
)
st.plotly_chart(fig, use_container_width=True)


with right:
# VIS 2: Scatter with bubble size
st.subheader("Hotels vs. Cafes by Governorate")
gov_col = mapping["governorate"]
xcol = mapping["hotels"]
ycol = mapping["cafes"]
sizecol = mapping.get("restaurants")
fig2 = px.scatter(
agg,
x=xcol, y=ycol,
size=sizecol if sizecol in agg.columns else None,
color=gov_col,
hover_name=gov_col,
title="Relationship between Hotels and Cafes (size ~ Restaurants)",
)
st.plotly_chart(fig2, use_container_width=True)


# Optional visuals if Tourism Index exists
idx_col = mapping.get("tourism_idx")
if idx_col and idx_col in filtered.columns:
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
st.subheader("Tourism Index by Governorate")
gov_col = mapping["governorate"]
agg_idx = filtered.groupby(gov_col, dropna=False)[idx_col].mean().reset_index()
fig3 = px.line(
agg_idx, x=gov_col, y=idx_col, markers=True,
title="Average Tourism Index across Governorates"
)
fig3.update_layout(height=450, xaxis_tickangle=-30)
st.plotly_chart(fig3, use_container_width=True)
with c2:
st.subheader("Distribution of Tourism Index (Towns)")
fig4 = px.histogram(filtered, x=idx_col, nbins=20, title="Tourism Index Distribution")
st.plotly_chart(fig4, use_container_width=True)


with st.expander("ℹ️ Notes & Context"):
st.write(
"""
- Two key interactions that change the **data/visuals**:
1) **Governorate multiselect** – updates every chart.
2) **Tourism Index range** – filters towns included in aggregates & distribution.
- Bar ↔ Pie toggle offers absolute vs. share comparisons.
"""
)


if __name__ == "__main__":
main()
