import streamlit as st
import pandas as pd
import pickle

# Load the rules table
# Ensure 'market_basket_rules.pkl' is in the same folder
rules = pickle.load(open('market_basket_rules.pkl', 'rb'))

st.title("🛒 Smart Market Recommender")
st.write("Select an item to see what customers usually buy with it!")

# 1. Get a list of all unique items to show in the dropdown
# The 'antecedents' column contains sets (e.g., {'milk', 'bread'}), so we extract individual items
all_items = set()
for itemset in rules['antecedents']:
    for item in itemset:
        all_items.add(item)
all_items = sorted(list(all_items))

# 2. User selects an item
selected_item = st.selectbox("Select an item you are buying:", all_items)

if st.button("Show Recommendations"):
    # 3. Find rules where the selected item is in the 'antecedents'
    recommendations = rules[rules['antecedents'].apply(lambda x: selected_item in x)]
    
    if not recommendations.empty:
        # Sort by confidence (highest probability first) and take top 5
        top_recs = recommendations.sort_values(by='confidence', ascending=False).head(5)
        
        st.subheader(f"Customers who bought '{selected_item}' also bought:")
        
        for index, row in top_recs.iterrows():
            # Clean up the name (convert set to string)
            items_to_buy = list(row['consequents'])
            item_name = ", ".join(items_to_buy)
            prob = row['confidence'] * 100
            
            st.success(f"👉 **{item_name}** ({prob:.1f}% chance)")
            
    else:
        st.info("No strong recommendations found for this specific item.")
