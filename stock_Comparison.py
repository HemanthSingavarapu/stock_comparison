import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Function to fetch stock data
def get_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

# Function to fetch ticker symbols from Yahoo Finance
def get_ticker_symbol(company_name):
    ticker_info = yf.Ticker(company_name)
    return ticker_info.info.get('symbol', None)

# Function to fetch company information
def get_company_info(symbol):
    ticker_info = yf.Ticker(symbol)
    return ticker_info.info

# Function to fetch data for both uploaded files and manual input
def fetch_data(company_names_list, start_date, end_date):
    data = {}
    company_info = {}
    for company_name in company_names_list:
        try:
            symbol = get_ticker_symbol(company_name)
            if symbol:
                stock_data = get_stock_data(symbol, start_date, end_date)
                data[symbol] = stock_data
                company_info[symbol] = get_company_info(symbol)
        except Exception as e:
            st.warning(f"Couldn't fetch data for {company_name}: {str(e)}")
    return data, company_info

# Title and description
st.title("Stock Comparison Tool")
st.write(
    "This tool allows you to compare the stock prices of different companies over time. "
    "You can enter company names in the text input field, and the tool will automatically fetch the corresponding ticker symbols from Yahoo Finance."
    "for example Microsoft(MSFT),amazon(AMZN),APPLE(AAPL) and so on..........."
)

# User input for company names and date range
st.subheader("Enter Company Names to Compare")
company_names_input = st.text_area("Enter company names (separate with commas):")
selected_company_names = [name.strip() for name in company_names_input.split(',') if name.strip()]

# Fetch ticker symbols from Yahoo Finance
selected_symbols = [get_ticker_symbol(name) for name in selected_company_names if get_ticker_symbol(name)]

# Date range input
start_date = st.date_input("Select start date:", pd.to_datetime('2020-01-01'))
end_date = st.date_input("Select end date:", pd.to_datetime('2023-01-01'))

# Compare button
compare_button = st.button("Compare Now")

# Fetch stock data and company information
if compare_button and selected_company_names:
    data, company_info = fetch_data(selected_company_names, start_date, end_date)

    # Display stock data and company information horizontally
    for symbol, stock_data in data.items():
        col1, col2 = st.columns(2)

        # Display company information
        with col1:
            st.write(f"**{symbol} ({company_info[symbol]['longName']})**")
            st.write("Company Information:")
            st.write(f"Industry: {company_info[symbol].get('industry', 'N/A')}")
            st.write(f"Sector: {company_info[symbol].get('sector', 'N/A')}")

        # Display stock data
        with col2:
            st.write("Stock Data:")
            st.dataframe(stock_data)

    # Create separate graphs for each parameter horizontally
    for param in ['Open', 'Close', 'High', 'Low', 'Volume']:
        st.subheader(f"Stock Comparison Over {param}")
        fig = go.Figure()

        for symbol, stock_data in data.items():
            fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data[param], mode='lines', name=f"{symbol}"))

        fig.update_layout(xaxis_title="Date", yaxis_title=f"{param}", title=f"Stock Comparison Over {param}")
        st.plotly_chart(fig)
