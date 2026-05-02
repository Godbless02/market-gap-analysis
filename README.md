 
# The Sugar Trap : Market Gap Analysis
### Powered by Open Food Facts Data
### Helix CPG Partners | Healthy Snacking Line Research

---

## A. Executive Summary

The global snack market is overwhelmingly dominated by high sugar, low protein products and this analysis set out to find where the real opportunity lies for a health focused manufacturer. Using over 46,000 categorized food products from the Open Food Facts database, I mapped the nutritional landscape of the snack aisle and found a striking pattern. The vast majority of products cluster in what I call the "Sugar Trap" zone, high in sugar and low in protein, leaving the High Protein and Low Sugar quadrant almost completely empty. The data points clearly to Confectionery as the biggest market opportunity, where 96.2% of products fail to meet basic health criteria. A new product targeting at least 13g of protein and less than 1g of sugar per 100g, built around Soy, Nuts, and Peanuts as primary protein sources, would enter a space with virtually no competition.

---

## B. Project Links

**Notebook:** https://github.com/Godbless02/market-gap-analysis/blob/main/notebooks/analysis.ipynb

**Dashboard:** https://sugar-trap-market-gap.streamlit.app

**Presentation:** https://canva.link/ejeylvmmu8pu7h7

**Notebook Export:** https://github.com/Godbless02/market-gap-analysis/blob/main/notebooks/analysis.html
---

## C. Technical Explanation

### Data Cleaning

The raw Open Food Facts dataset came with significant gaps. Out of 500,000 rows loaded, nearly 79% were missing sugar values and 78% were missing protein values. Rather than filling these gaps with estimates, I chose to drop any row missing the core nutritional columns that the analysis depends on, specifically product name, sugar content and protein content. I also filtered out biologically impossible values, anything exceeding 100g per 100g of product, which are clearly data entry errors. This brought the dataset down to 103,682 reliable rows. From there I removed products with no category information at all, since uncategorized products cannot contribute to a market gap analysis, leaving a final working dataset of 46,697 products across 16 meaningful categories.

### Candidate's Choice : Market Opportunity Scorecard

Beyond the scatter plot the brief asked for, I built a custom Market Opportunity Score for each product category. The score combines two factors: how large the gap is (what percentage of products in that category fail the health criteria) and how big the market is (the total number of products in that category). The formula rewards categories that are both large and underserved, because a 96% gap in a category with only 10 products is far less valuable than a 96% gap in a category with 6,000 products. This scoring approach gives the client a single ranked list they can take directly into a strategic planning meeting, rather than having to interpret a scatter plot themselves. Confectionery scored 83.7, the highest of all 16 categories, confirming it as the clear number one opportunity.