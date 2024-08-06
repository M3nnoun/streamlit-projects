import streamlit as st
import plotly.express as px
import pandas as pd

# Changing the title and icon page
st.set_page_config(page_title="My Webpage", page_icon=":chart_with_upwards_trend:", layout="wide")

st.title("Retail Sales Dashboard")

# Load the dataset
@st.cache_data
def loud_data():
  df = pd.read_csv('data/retail_sales_dataset.csv',
     index_col='Transaction_ID')
  df['Transaction_Date'] = pd.to_datetime(df['Date'],format= '%Y-%m-%d')
  return df

df=loud_data()

# Add a boolean variable to track whether filters have been applied
filters_applied = False

# Building the sidebar
st.sidebar.header("Please Filter Here:")

category = st.sidebar.multiselect(
    'Please select a category',
    options=df['Product_Category'].unique(),
    default=df['Product_Category'].unique()
)

gender = st.sidebar.multiselect(
    'Please select a gender',
    options=df['Gender'].unique(),
    default=df['Gender'].mode().values[0]
)

age = st.sidebar.slider("Filter by Age?", 
                        df['Age'].min(), 
                        df['Age'].max(),
                        23)

# Check if any filters have been applied
if category or gender or age:
    filters_applied = True

# Display the initial data frame if no filters have been applied
if not filters_applied:
    st.dataframe(df.head(10))
    st.caption("A full Dataframe whitout any filter.")
else:
    # Display the filtered data
    filter_data = df.query(
        "Product_Category==@category & Gender==@gender & Age==@age"
    )
    st.dataframe(filter_data.head(10), use_container_width=True)
    st.caption("The filtred Dataframe")


st.divider()  # 👈 Draws a horizontal rule

#Main page KPI
st.title(':bar_chart: Sales Dashboard')
st.markdown("##")
total_sales=int(filter_data['Total_Amount'].sum())
avarage_price=round(filter_data['Price'].mean(),1)
sale_price=f":dollar: \t {int(avarage_price)}"
quantities=f":package: \t {filter_data['Quantity'].sum()}"

left_column, right_column ,middle_column= st.columns(3)
with left_column:
  st.subheader("Totale Sales")
  st.subheader(f":moneybag: \t {total_sales}")
with right_column:
  st.subheader("Avarage Price")
  st.subheader(f"{sale_price}")
with middle_column:
  st.subheader("Quantities")
  st.subheader(f"{quantities}")

##ploting charts 
#product sale by category

sales_by_category=filter_data.groupby('Product_Category')[['Total_Amount']].sum().sort_values(by='Total_Amount',ascending=False)

fig1=px.bar(sales_by_category,x=sales_by_category.index,y='Total_Amount',title='Product Sales by Category',orientation='h')

st.plotly_chart(fig1,use_container_width=True)


#product seeling time line
filter_on = st.toggle("Use Filtter inputs")
if filter_on:
  sales_by_time=filter_data.groupby('Transaction_Date')[['Total_Amount']].sum()
  fig2=px.line(sales_by_time,x=sales_by_time.index,y='Total_Amount')
else:
  sales_by_time=df.groupby('Transaction_Date')[['Total_Amount']].sum()
  fig2=px.line(sales_by_time,x=sales_by_time.index,y='Total_Amount')

st.plotly_chart(fig2,use_container_width=True)

