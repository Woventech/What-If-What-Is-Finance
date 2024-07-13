import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime


# Funzione per calcolare la crescita dell'investimento
def calcola_crescita_investimento(ticker, start_date, end_date,
                                  investimento_iniziale):
    df = yf.download(ticker, start=start_date, end=end_date)
    df['Rendimento'] = df['Adj Close'].pct_change()
    df['Valore Investimento'] = investimento_iniziale * (
        1 + df['Rendimento']).cumprod()
    return df


# Interfaccia Streamlit
st.title("Simulatore di Crescita dell'Investimento")

# Input dell'utente
investimento_iniziale = st.number_input("Inserisci l'importo iniziale (€)",
                                        value=2000)
prodotto_finanziario = st.selectbox("Seleziona il prodotto finanziario",
                                    ["VUSA", "AGG", "SPY", "TLT"])
anni = st.slider("Seleziona lo span temporale (anni)",
                 min_value=1,
                 max_value=20,
                 value=10)

# Calcolo delle date
oggi = datetime.now()
start_date = oggi.replace(year=oggi.year - anni).strftime('%Y-%m-%d')
end_date = oggi.strftime('%Y-%m-%d')

# Calcolo della crescita dell'investimento
df = calcola_crescita_investimento(prodotto_finanziario, start_date, end_date,
                                   investimento_iniziale)

# Grafico
fig = px.line(df,
              x=df.index,
              y='Valore Investimento',
              title=f'Crescita del tuo investimento in {prodotto_finanziario}')
st.plotly_chart(fig)

# Mostra la tabella dei dati
st.write(df)

# Run Streamlit in Replit terminal
# streamlit run app.py
