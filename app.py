import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df_all_data = pd.read_csv("E-Commerce Public Dataset/all_data.csv")
df_geolocation = pd.read_csv("E-Commerce Public Dataset/geolocation_dataset.csv")
df_category_name = pd.read_csv("E-Commerce Public Dataset/product_category_name_translation.csv")
df_customer = pd.read_csv("E-Commerce Public Dataset/customers_dataset.csv")
df_product = pd.read_csv("E-Commerce Public Dataset/products_dataset.csv")
df_order_review = pd.read_csv("E-Commerce Public Dataset/order_reviews_dataset.csv")
df_order_item = pd.read_csv("E-Commerce Public Dataset/order_items_dataset.csv")
df_order = pd.read_csv("E-Commerce Public Dataset/orders_dataset.csv")
df_seller = pd.read_csv("E-Commerce Public Dataset/sellers_dataset.csv")

# Melakukan join antara df_product dan df_order_item berdasarkan product_id dan order_id
df_product = df_product[['product_id']]
df_order_item = df_order_item[['order_id', 'product_id']]
df_order_review = df_order_review[['order_id', 'review_score', 'review_creation_date']]

# Merge dataframes
df_merged = pd.merge(df_product, df_order_item, on='product_id')
df_final = pd.merge(df_merged, df_order_review, on='order_id')

# Preprocess your data
selected_product_ids = df_final['product_id'].unique()[:112371]
df_final_selected = df_final[df_final['product_id'].isin(selected_product_ids)]

# Sidebar for personal information
st.sidebar.title('Date Time Selection')
# Add your personal information here, for example:
# your_name = st.sidebar.text_input(' Name', 'Muhammad Zaidan Naufal Fikri')
# your_email = st.sidebar.text_input('Email', 'Zaidan333@etc.com')

# Sidebar for date range selection
start_date = st.sidebar.date_input('Select start date', pd.to_datetime('2017-08-01'))
end_date = st.sidebar.date_input('Select end date', pd.to_datetime('2018-08-31'))

# Convert start_date and end_date to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data based on selected date range
df_final_selected['review_creation_date'] = pd.to_datetime(df_final_selected['review_creation_date'])
df_final_selected = df_final_selected[
    (df_final_selected['review_creation_date'] >= start_date) & (df_final_selected['review_creation_date'] <= end_date)
]
df_final_selected['month_year'] = df_final_selected['review_creation_date'].dt.to_period('M')

# Groupby and calculate summary statistics
summary_df = df_final_selected.groupby('month_year').agg({'review_score': ['count', 'mean']}).reset_index()
summary_df.columns = ['month_year', 'review_count', 'avg_review_score']

# Main content
st.title('E-Commerce Public Dataset Analysis')
st.title('Number of Reviews and Average Review Score')
st.subheader('Number of Reviews')
st.line_chart(summary_df.set_index('month_year')['review_count'])

# Line chart for Average Review Score
st.subheader('Average Review Score')
st.line_chart(summary_df.set_index('month_year')['avg_review_score'])

# Display Total Customer and Seller by State
st.title('Distribution of Customers and Sellers by State')

# Bar chart for Total Customer by State
customer_count_by_state = df_customer['customer_state'].value_counts()
st.subheader('Total Customer by State')
st.bar_chart(customer_count_by_state)

# Bar chart for Total Sellers by State
seller_count_by_state = df_seller['seller_state'].value_counts()
st.subheader('Total Sellers by State')
st.bar_chart(seller_count_by_state)

st.write('Analysis Result for Number of Reviews and Average Review Score: ')
st.write('Based on the processed average review score table to determine when the E-commerce Public received the lowest review score, it was found that in March 2018, the score was 3.4 average review score. This 3.4 is the result of the average of review scores 1-5 calculated over 31 days, covering the period from March 1 to March 31, 2018, which is converted into a monthly average. From the data, there is a decline in customer satisfaction from January 2018, reaching the lowest point in March 2018.')
st.write('              ')
st.write('Analysis Result for Total Customer and Seller by State: ')
st.write('Based on the data from the two histograms, Total Customer by State and Total Sellers by State, it is observed that the distribution of customers and sellers in each state is quite even. For example, in the state of Sao Paulo (SP), there are 40,000 customers, which is the highest among all states, and there are 18,000 sellers in Sao Paulo, making it the state with the highest number of sellers. This contributes to the smooth operation of buying and selling processes and a continuous improvement in review scores since March 2018.')