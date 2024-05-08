import pandas as pd
import streamlit as st
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf


st.title('S&P 500 Stocks Plots application')

st.markdown("""
This app retrieves the list of selected **S&P 500** stocks and their closing prices (year-to-date).
**Data source:** https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
""")

st.sidebar.header('User Input Features')

# Web scraping the stocks data

@st.cache
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar for sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering the data
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

st.header('Display companies in selected sector')
st.write('Data dimensions: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)


# Downloading the stock data

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # strings to byte conversion
    href = f'<a href="data:file/csv;base64, {b64}" download="SP500.csv">Download CSV</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# pypi.org/project/yfinance/

data = yf.download(
    tickers=list(df_selected_sector[:10].Symbol),
    period="ytd",
    interval="1d",
    group_by="ticker",
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None
    )


# Plotting the closing prices of the stocks using query symbol

def plot_price(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Close, color='blue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='blue', alpha=0.3)
    plt.xticks(rotation=45)
    plt.title(symbol)
    plt.xlabel('Date')
    plt.ylabel('Closing price')
    return st.pyplot()

number_of_companies = st.sidebar.slider("Number of Companies:", 1, 10)

if st.button('Show charts'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:number_of_companies]:
        plot_price(i)