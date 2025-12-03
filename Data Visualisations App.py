import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

st.title('Data Visualisation App')
st.write('This app show different visualisations graphs!!')

uploaded_file = st.file_uploader("Upload CSV file:", type=['csv'])
option = st.radio("Choose Data Source:",['uploaded_file', 'Sample Data'])

if option == "uploaded_file" and uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
else:
  df =  pd.DataFrame({
        "Category": ["A", "B", "C", "D"],
        "Values": [10, 30, 20, 40],
        "X": [1, 2, 3, 4],
        "Y": [10, 15, 13, 18]
    })
  
st.write('Dataset Preview')
st.dataframe(df)


numeric_col = list(df.select_dtypes(include= ['int', 'float']).columns)
category_col = list(df.select_dtypes(include= ['object']).columns)

st.write("### Selected Column Types")
st.write("**Numeric Columns:**", numeric_col)
st.write("**Categorical Columns:**", category_col)
# ------------------------------------------------------------------


# Bar Chart

st.write('### Bar Chart')
if numeric_col:
  st.bar_chart(df[numeric_col])
else:
  st.info('No numeric columns')

# Line Chart

st.write('### Line Chart')
if numeric_col:
  st.line_chart(df[numeric_col])
else:
  st.info('No numeric columns')

# Area Chart 

st.write('### Area Chart')
if numeric_col:
  st.area_chart(df[numeric_col])
else:
  st.info('No numeric columns')

# Scatter Chart

st.write('### Scatter Plot')
if len(numeric_col) >= 2 :
  x_val = st.selectbox("Select X-axis", numeric_col)
  y_val = st.selectbox("Select Y-axis", numeric_col)

  st.write(f"Scatter Plot  {x_val}  VS  {y_val} ")
  st.scatter_chart(df[[x_val, y_val]])
else:
  st.info('No numeric columns')


# Histogram
st.write('### Histogram')
if numeric_col:
  col = st.selectbox('Select Columns',numeric_col)
  fig, ax = plt.subplots()
  ax.hist(df[col] , bins= 10)
  ax.set_title(f'Histogram of {col}')
  st.pyplot(fig)
else:
    st.info('No numeric columns')


# Piechart
st.write('### Pie Chart ')
if numeric_col and category_col:
  cat_col = st.selectbox("Select Category columns",category_col)
  num_col = st.selectbox("Select Numeric column", numeric_col)
  fig, ax= plt.subplots()
  grouped_col= df.groupby(cat_col)[num_col].sum()
  ax.pie(grouped_col, labels= grouped_col.index)
  ax.set_title('Pie Chart')
  st.pyplot(fig)

else:
    st.info('No numeric columns')


# Box Plot
st.write('### Box Plot')
if numeric_col:
  fig, ax = plt.subplots()
  ax.boxplot(df[numeric_col])
  ax.set_xticklabels(numeric_col, rotation = 45)
  ax.set_title("Box Plot")
  st.pyplot(fig)
else:
    st.info('No numeric columns')


