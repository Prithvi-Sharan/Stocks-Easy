import datetime

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from googlesearch import search
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import plotly
import streamlit as st

st.set_page_config("Stock Easy")
st.header("Stock Prices Made Easy")

st.write()
st.sidebar.subheader('Query')
start_date = st.sidebar.date_input("Start date",datetime.date(2021,5,1))
end_date = st.sidebar.date_input("End date",datetime.date(2021,5,30))
Company = st.sidebar.text_input("Company name","Eg. SBI")
searchval = 'yahoo finance ' + Company
link = []
# limits to the first link
for url in search(searchval, tld='es', lang='es', stop=1):
    link.append(url)

link = str(link[0])
link = link.split("/")
if link[-1] == '':
    ticker = link[-2]
else:
    x = link[-1].split('=')
    ticker = x[-1]
symbol = ticker
Data=yf.Ticker(symbol)
df=Data.history(period='1d',start=start_date,end=end_date)

logo='<img src=%s>' % Data.info['logo_url']
st.markdown(logo,unsafe_allow_html=True)

df1=Data.history(period='1d',start=(datetime.date.today()-datetime.timedelta(5)),end=(datetime.date.today()))
c1,c2,c3=st.beta_columns(3)
st.write("Note:- *All values in USD*")
with c1:
    st.subheader("**Past close date**")
    st.markdown(f"<h3 style='text_align:center ;'>{pd.to_datetime(df1.index.values[len(df1)-1]).strftime('%d/%m/%y')}</h3>",unsafe_allow_html=True)
with c2:
    st.subheader("**Close Price**")
    st.markdown(f"<h3 style='text_align:center ; color:red'>{df1['Close'].values[len(df1)-1]}</h3>",unsafe_allow_html=True)
with c3:
    st.subheader("**High Price**")
    st.markdown(f"<h3 style='text_align:center ;'>{df1['High'].values[len(df1)-1]}</h3>",unsafe_allow_html=True)

summary=Data.info['longBusinessSummary']
st.header("**Business Summary**")
st.write(summary)

st.write(df)

chart_visual = st.sidebar.selectbox('Select Charts/Plot type', ('Candlestick','Line Chart', 'Bar Chart'))
fig = go.Figure()

if chart_visual == 'Line Chart':
    st.line_chart(data=df['Close'], width=0, height=0, use_container_width=True)
elif chart_visual == 'Bar Chart':
    st.bar_chart(data=df['Close'], width=0, height=0, use_container_width=True)
elif chart_visual == 'Candlestick':
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df.Open,
                                 high=df.High,
                                 low=df.Low,
                                 close=df.Close,
                                 visible=True,
                                 name='Candlestick', ))

    fig.add_shape(
        # Line Horizontal
        type="line",
        x0=start_date,
        y0=df.Close[0],
        x1=end_date,
        y1=df.Close[len(df)-1],
        line=dict(
            color="black",
            width=1.5,
            dash="dash",
        ),
        visible=True,
    )
    fig.update_layout(height=800, width=1000, updatemenus=[
        dict(direction="down", pad={"r": 10, "t": 10}, showactive=True, x=0, xanchor="left", y=1.15,
             yanchor="top", )], )
    st.plotly_chart(fig)

st.markdown("Created by *Prithvi* using Python and Stremlit")
