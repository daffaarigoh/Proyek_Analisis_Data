import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.title('E-Commerce Public Dashboard')

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('/Dashboard/main_data.csv')
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'], errors='coerce')
    return data

all_data = load_data()

# Sidebar untuk filter
st.sidebar.title('Filters')
state_filter = st.sidebar.multiselect(
    'Select Customer State:', 
    options=all_data['customer_state'].unique()
)

# Filter data berdasarkan pilihan pengguna
if state_filter:
    filtered_data = all_data[all_data['customer_state'].isin(state_filter)]
else:
    filtered_data = all_data

# Visualisasi tren pembelian berdasarkan waktu
st.subheader('Customer Purchase Trend Over Time (Quarterly)')
filtered_data['order_month'] = filtered_data['order_purchase_timestamp'].dt.to_period('M').astype(str)
monthly_sales = filtered_data.groupby('order_month').size().reset_index(name='num_orders')
monthly_sales['order_month'] = pd.to_datetime(monthly_sales['order_month'])

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='order_month', y='num_orders', data=monthly_sales, marker='o', ax=ax)
ax.set_title('Sales Trends Over Time')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

# Visualisasi Top 10 Cities with Highest Sales
geo_sales = filtered_data.groupby('customer_city').size()
top_geo_sales = geo_sales.nlargest(10)
top_geo_sales_df = top_geo_sales.reset_index(name='total_sales')
top_geo_sales_df.columns = ['customer_city', 'total_sales'] 

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='total_sales', y='customer_city', data=top_geo_sales_df, palette='viridis', ax=ax)
ax.set_title('Top 10 Cities with Highest Sales')
ax.set_xlabel('Total Sales')
ax.set_ylabel('City')
plt.grid(axis='x')
st.pyplot(fig)

# Analisis Freight dan Price
st.subheader('Freight Value and Price by State and Product Category')
freight_price_df = filtered_data.groupby(by=["customer_state", "product_category_name"]).agg({
    "freight_value": "sum",
    "price": "sum"
}).sort_values(by="freight_value", ascending=False)

st.dataframe(freight_price_df.head())

# Menambahkan interaktivitas dengan chart (contoh bar chart)
st.subheader('Top 10 Product Categories by Freight Value')
top_10_freight = freight_price_df.groupby('product_category_name')['freight_value'].sum().nlargest(10)

fig, ax = plt.subplots()
top_10_freight.plot(kind='bar', ax=ax)
plt.title('Top 10 Product Categories by Freight Value')
plt.xlabel('Product Category')
plt.ylabel('Freight Value')
st.pyplot(fig)

# Footer
st.text("Dashboard Created by Muhammad Daffa Arigoh")
