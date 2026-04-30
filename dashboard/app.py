import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Sugar Trap — Market Gap Analysis",
    page_icon="🍫",
    layout="wide"
)

# ============================================
# LOAD & PREPARE DATA
# ============================================

@st.cache_data
def load_data():
    import os
    DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard_data.csv')
    df = pd.read_csv(DATA_PATH)
    return df


# Load data
with st.spinner('Loading data... this may take a minute ⏳'):
    df = load_data()

sugar_avg = df['sugars_100g'].median()
protein_avg = df['proteins_100g'].median()
blue_ocean = df[(df['sugars_100g'] < 5.0) & (df['proteins_100g'] > 6.67)]

# ============================================
# HEADER
# ============================================
st.title("🍫 The Sugar Trap — Market Gap Analysis")
st.markdown("**Client:** Helix CPG Partners | **Analyst:** Ghansah Godbless Boabeng")
st.markdown("---")

# ============================================
# KPI METRICS ROW
# ============================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products Analyzed", f"{len(df):,}")
col2.metric("Products in Blue Ocean", f"{len(blue_ocean):,}")
col3.metric("Median Sugar per 100g", f"{sugar_avg:.1f}g")
col4.metric("Median Protein per 100g", f"{protein_avg:.1f}g")

st.markdown("---")

# ============================================
# KEY INSIGHT BOX
# ============================================
st.success("""
💡 KEY INSIGHT: Based on the data, the biggest market opportunity is in **CONFECTIONERY**, 
specifically targeting products with at least **13g of protein** and less than **1g of sugar** per 100g.
Only **3.8%** of confectionery products meet this criteria — meaning **96.2%** of the market 
is stuck in the Sugar Trap. The top protein sources to use are **Soy, Nuts, and Peanuts**.
""")

st.markdown("---")

# ============================================
# SCATTER PLOT
# ============================================
st.subheader("📊 Nutrient Matrix — Sugar vs Protein by Category")

# Category filter
all_cats = sorted(df['primary_category'].unique().tolist())
selected_cats = st.multiselect(
    "Filter by Category:",
    options=all_cats,
    default=all_cats
)

filtered_df = df[df['primary_category'].isin(selected_cats)]

fig = px.scatter(
    filtered_df,
    x='sugars_100g',
    y='proteins_100g',
    color='primary_category',
    title='Sugar vs Protein — The Nutrient Matrix',
    labels={
        'sugars_100g': 'Sugar per 100g (g)',
        'proteins_100g': 'Protein per 100g (g)',
        'primary_category': 'Category'
    },
    opacity=0.5,
    hover_data=['product_name']
)

fig.add_hline(y=protein_avg, line_dash="dash", line_color="white",
              annotation_text=f"Avg Protein: {protein_avg:.1f}g")
fig.add_vline(x=sugar_avg, line_dash="dash", line_color="white",
              annotation_text=f"Avg Sugar: {sugar_avg:.1f}g")

fig.update_layout(height=600, template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# OPPORTUNITY SCORECARD
# ============================================
st.subheader("🎯 Market Opportunity Scorecard (Candidate's Choice)")
st.markdown("*Custom metric: Gap Size × Market Size — higher score = bigger opportunity*")

opportunity_data = []
for cat in df['primary_category'].unique():
    cat_df = df[df['primary_category'] == cat]
    cat_blue = blue_ocean[blue_ocean['primary_category'] == cat]
    total = len(cat_df)
    in_blue_ocean = len(cat_blue)
    gap_pct = 100 - (in_blue_ocean / total * 100)
    avg_protein = cat_df['proteins_100g'].mean()
    avg_sugar = cat_df['sugars_100g'].mean()
    opportunity_score = (gap_pct / 100) * np.log(total) * 10
    opportunity_data.append({
        'Category': cat,
        'Total Products': total,
        'Healthy Products': in_blue_ocean,
        'Gap %': round(gap_pct, 1),
        'Avg Protein (g)': round(avg_protein, 1),
        'Avg Sugar (g)': round(avg_sugar, 1),
        'Opportunity Score': round(opportunity_score, 1)
    })

opp_df = pd.DataFrame(opportunity_data).sort_values('Opportunity Score', ascending=False).reset_index(drop=True)
opp_df.index += 1

# Bar chart
fig2 = px.bar(
    opp_df,
    x='Opportunity Score',
    y='Category',
    orientation='h',
    color='Opportunity Score',
    color_continuous_scale='Reds',
    title='Market Opportunity Score by Category'
)
fig2.update_layout(height=500, template='plotly_dark', yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig2, use_container_width=True)

st.dataframe(opp_df, use_container_width=True)

st.markdown("---")

# ============================================
# HIDDEN GEM
# ============================================
st.subheader("💎 The Hidden Gem — Top Protein Sources")
st.markdown("*Analyzing ingredients of High Protein Confectionery products*")

conf_high_protein = df[
    (df['primary_category'] == 'Confectionery') &
    (df['proteins_100g'] > 13) &
    (df['ingredients_text'].notna())
]

protein_sources = ['whey', 'soy', 'peanut', 'almond', 'cashew',
                   'milk protein', 'egg', 'casein', 'pea protein',
                   'rice protein', 'hemp', 'collagen', 'gelatin',
                   'nut', 'seed', 'quinoa', 'chickpea', 'lentil']

source_counts = {}
for source in protein_sources:
    count = conf_high_protein['ingredients_text'].str.lower().str.contains(source, na=False).sum()
    source_counts[source] = count

source_df = pd.DataFrame(list(source_counts.items()), columns=['Protein Source', 'Product Count'])
source_df = source_df.sort_values('Product Count', ascending=False).reset_index(drop=True)
source_df['Protein Source'] = source_df['Protein Source'].str.title()

fig3 = px.bar(
    source_df.head(10),
    x='Protein Source',
    y='Product Count',
    color='Product Count',
    color_continuous_scale='Greens',
    title='Top Protein Sources in High Protein Confectionery'
)
fig3.update_layout(height=400, template='plotly_dark')
st.plotly_chart(fig3, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("🥇 #1 Protein Source", source_df.iloc[0]['Protein Source'], f"{source_df.iloc[0]['Product Count']} products")
col2.metric("🥈 #2 Protein Source", source_df.iloc[1]['Protein Source'], f"{source_df.iloc[1]['Product Count']} products")
col3.metric("🥉 #3 Protein Source", source_df.iloc[2]['Protein Source'], f"{source_df.iloc[2]['Product Count']} products")

st.markdown("---")
st.caption("Data Source: Open Food Facts | Analysis by Godbless Godbey | Helix CPG Partners Capstone")