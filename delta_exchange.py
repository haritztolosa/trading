import requests
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def obtener_fecha_desde_ticker(ticker):
    try:
        dia = ticker.split("-")[-1]
        end_date = datetime.strptime(dia, '%d%m%y') + timedelta(days=1)
        start_date = end_date - timedelta(days=6)
        return start_date, end_date
    except ValueError:
        raise ValueError("Ticker no reconocido, prueba a poner: C-BTC-28000-170323")

def obtener_datos(ticker, start_date, end_date):
    headers = {'Accept': 'application/json'}
    params = {
        'resolution': '1m',
        'symbol': 'MARK:' + ticker,
        'start': str(int(start_date.timestamp())),
        'end': str(int(end_date.timestamp()))
    }

    response = requests.get('https://api.delta.exchange/v2/history/candles', params=params, headers=headers)
    response.raise_for_status()
    return response.json()["result"]

def crear_grafico(df, ticker):
    df["time"] = pd.to_datetime(df["time"], unit="s")
    candlesticks = go.Candlestick(
        x=df["time"],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        showlegend=False
    )

    fig = go.Figure(candlesticks)
    fig.update_layout(title=ticker, height=1000)
    fig.update_yaxes(title="Price $", showgrid=True)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,1)',
        spikedistance=-1,
        hovermode="x"
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        showspikes=True,
        spikesnap="cursor",
        spikemode="across+toaxis",
        spikedash='solid',
        spikecolor="#FFFFFF",
        spikethickness=0.5
    )
    fig.update_yaxes(
        showgrid=True,
        showline=True,
        gridwidth=1,
        gridcolor='#464646',
        showspikes=True,
        spikesnap="cursor",
        spikemode="across+toaxis",
        spikedash='solid',
        spikecolor="#FFFFFF",
        spikethickness=0.5
    )

    fig.show()

def main():
    ticker = input("Pon el ticker: ")
    try:
        start_date, end_date = obtener_fecha_desde_ticker(ticker)
    except ValueError as e:
        print(e)
        return

    try:
        datos = obtener_datos(ticker, start_date, end_date)
        df = pd.DataFrame.from_records(datos)
        crear_grafico(df, ticker)
    except requests.RequestException as e:
        print(f"Error en la solicitud de datos: {e}")
    except KeyError:
        print("No hay datos para el ticker " + str(ticker))

if __name__ == "__main__":
    main()
