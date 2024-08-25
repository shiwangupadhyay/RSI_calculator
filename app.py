import streamlit as st
import pandas as pd
import yfinance as yf
import ta

# Define forex pairs
forex_pairs = [
    'EURUSD=X', 'USDJPY=X', 'GBPUSD=X',
    'AUDUSD=X', 'USDCAD=X', 'USDCHF=X',
    'NZDUSD=X', 'EURJPY=X', 'GBPJPY=X',
    'EURGBP=X', 'AUDJPY=X', 'EURAUD=X',
    'EURCHF=X', 'AUDNZD=X', 'NZDJPY=X',
    'GBPAUD=X', 'GBPCAD=X', 'EURNZD=X',
    'AUDCAD=X', 'GBPCHF=X', 'AUDCHF=X',
    'EURCAD=X', 'CADJPY=X', 'GBPNZD=X',
    'CADCHF=X', 'CHFJPY=X', 'NZDCAD=X',
    'NZDCHF=X', 'USDINR=X'
]

# Define the indicator function
def indicator(df):
    indicate = []
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df.dropna(inplace=True)
    for i in range(len(df['RSI'])):
        if df['RSI'].iloc[i] > 70:
            indicate.append('Overbought')
        elif df['RSI'].iloc[i] < 30:
            indicate.append('Underbought')
        else:
            indicate.append('Neutral')
    return indicate

# Define the output function
def output(dataframe):
    Underbought = []
    Overbought = []
    Neutral = []
    date = None
    for i in forex_pairs:
        if i in dataframe:
            date = dataframe[i].index.max()
            if dataframe[i]['indication'].iloc[-1] == 'Underbought':
                Underbought.append(i)
            elif dataframe[i]['indication'].iloc[-1] == 'Overbought':
                Overbought.append(i)
            else:
                Neutral.append(i)
    return Underbought, Overbought, Neutral, date

# Streamlit app
st.set_page_config(layout="wide")
st.title('Forex RSI Indicator Analysis')

# Sidebar for user input
st.sidebar.header('Settings')
select_all = st.sidebar.checkbox('Select All Forex Pairs', value=True)
if select_all:
    selected_pairs = forex_pairs
else:
    selected_pairs = st.sidebar.multiselect('Select Forex Pairs', forex_pairs, default=forex_pairs[:5])

# Download data
results = {}
results1 = {}

for pair in selected_pairs:
    data = yf.download(pair, period='1mo', interval='1h')
    data.index = data.index.tz_convert('Asia/Kolkata')
    data1 = yf.download(pair, period='1mo', interval='1d')
    data['indication'] = indicator(data)
    data1['indication'] = indicator(data1)
    results[pair] = data
    results1[pair] = data1

# Process data
Underbought, Overbought, Neutral, date = output(results)
Underbought1, Overbought1, Neutral1, date1 = output(results1)

# Display results
st.write(f'For Date: {date}')
st.subheader('FOR 1 HOUR INTERVAL')
col1, col2, col3 = st.columns(3)
with col1:
    st.write('FOREX Pairs having RSI less than 30:', Underbought)
with col2:
    st.write('FOREX Pairs having RSI more than 70:', Overbought)
with col3:
    st.write('FOREX Pairs having RSI between 30 and 70:', Neutral)

st.subheader('1 HOUR + 1 DAY COMBINED')
Underbought_combined = []
Overbought_combined = []
for i in forex_pairs:
    if (i in Underbought) and (i in Underbought1):
        Underbought_combined.append(i)
    elif (i in Overbought) and (i in Overbought1):
        Overbought_combined.append(i)
st.write('FOREX Pairs having RSI less than 30:', Underbought_combined)
st.write('FOREX Pairs having RSI more than 70:', Overbought_combined)

