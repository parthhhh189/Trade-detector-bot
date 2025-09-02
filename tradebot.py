import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- PARAMETERS ---
STOCK = 'AAPL'
START = '2023-01-01'
END = '2023-12-31'
FAST_MA = 10
SLOW_MA = 30

def get_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data

def add_signals(df, fast, slow):
    df['fast_ma'] = df['Close'].rolling(fast).mean()
    df['slow_ma'] = df['Close'].rolling(slow).mean()
    df['signal'] = 0
    df['signal'][fast:] = (
        (df['fast_ma'][fast:] > df['slow_ma'][fast:]).astype(int) -
        (df['fast_ma'][fast:] < df['slow_ma'][fast:]).astype(int)
    )
    df['trade_action'] = df['signal'].diff().fillna(0).map({1: 'BUY', -1: 'SELL', 0: ''})
    return df

def plot_signals(df):
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label='Close Price')
    plt.plot(df['fast_ma'], label=f'Fast MA ({FAST_MA})')
    plt.plot(df['slow_ma'], label=f'Slow MA ({SLOW_MA})')
    buy = df[df['trade_action'] == 'BUY']
    sell = df[df['trade_action'] == 'SELL']
    plt.scatter(buy.index, buy['Close'], marker='^', color='green', label='Buy Signal')
    plt.scatter(sell.index, sell['Close'], marker='v', color='red', label='Sell Signal')
    plt.legend()
    plt.title(f'Trade Detection for {STOCK}')
    plt.grid()
    plt.show()

def main():
    df = get_data(STOCK, START, END)
    df = add_signals(df, FAST_MA, SLOW_MA)
    print(df[['Close','trade_action']][df['trade_action'] != ''].dropna())
    df.to_csv('trade_signals.csv')
    plot_signals(df)
    print("Signals saved to trade_signals.csv")

if __name__ == "__main__":
    main()
