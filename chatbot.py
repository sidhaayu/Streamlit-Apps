# CHATBOT:-
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import PyPDF2
import pathlib as Path
import streamlit as st
from openai import OpenAI

mykey = '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'

client = OpenAI(api_key=mykey)

def load_data():
    # Load the sales transactions data
    sales = pd.read_excel('sales_transactions_2022_2024.xlsx')
    feedback = pd.read_csv('customer_feedback_large.csv')

    with open ('market_trends_extended.txt','r') as f:
        market = f.read()
          
    reader = PyPDF2.PdfReader('board_meeting_summary_long.pdf')
    pdf =" "
    for page in reader.pages:
        pdf += page.extract_text()
    
    return sales, feedback, market, pdf


# storing the data in variables
df, feedback_df, market_text, pdf_text = load_data()

# Preprocess the sales data
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')
df['Quater'] = df['Date'].dt.to_period('Q')
df['Year'] = df['Date'].dt.year

top_product = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(5)
region_pref = df.groupby('Region')['Revenue'].sum()
product_units = df.groupby('Product')['Units Sold'].sum().sort_values(ascending=False)
feedback_summary = feedback_df['Feedback'].value_counts().head(5)

st.title("Business Insights Dashboard")
query = st.text_input("Ask a question to the AI Business Analyst")

if st.button("Get Insight from AI Agent") and query and mykey:
    client.api_key = mykey
    prompt = f"""
    You are a highly skilled business analyst AI Assistant
            Here is the business context to use in your answer.

            Top Product by Revenue:
            {top_product.to_string()}

            Product Units Sold Per Product:
            {product_units.to_string()}

            Revenue By Region:
            {region_pref.to_string()}

            Market Trend Highlights:
            {market_text[:100]}

            Board Meeting Summary:
            {pdf_text[:100]}

            Feedback Summary of the Customers:
            {feedback_summary.to_string()}

            Now analyze and answer the query:
            {query}
    """
    with st.spinner("Analyzing your query..."):
        try:
            response = client.chat.completions.create(
                model ="gpt-3.5-turbo",
                messages = [{"role" : "user", "content":prompt}]
            )
            st.success("Response from the AI Agent:...")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"An error occurred: {e}")
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



