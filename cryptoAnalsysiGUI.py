import tkinter as tk
from tkinter import ttk
from pycoingecko import CoinGeckoAPI
import pandas as pd
import plotly.graph_objects as go


cg = CoinGeckoAPI()


class CryptoGUI():
    crypto = None
    date = None

    def __init__(self) -> None:
        self.Window()
        self.createButton()
        self.initVariables()
        self.runUI()

    def initVariables(self):
        self.crypto = tk.StringVar()
        self.date = tk.IntVar()

    # window
    def Window(self):
        self.root = tk.Tk()
        self.root.title('Cryptocurrency')
        self.root.geometry('500x200')

        entry_style = ttk.Style()
        entry_style.configure("TEntry", font=("Helvetica", 12))

        # Label|Crypto
        tk.Label(self.root, text="Enter Cryptocurrency", anchor="e").grid(
            row=0, column=0, padx=10, pady=5, sticky="e")
        self.cryptoEntry = ttk.Entry(
            self.root, textvariable=self.crypto, style="TEntry")
        self.cryptoEntry.grid(row=1, column=0, padx=10, pady=5)

        # Create a ttk.Combobox for cryptocurrency selection
        # List of popular cryptocurrencies
        self.crypto_options = [
            "bitcoin", "ethereum", "binancecoin", "cardano", "dogecoin"
        ]
        self.cryptoEntry = ttk.Combobox(
            self.root, textvariable=self.crypto, values=self.crypto_options, style="TCombobox"
        )
        self.cryptoEntry.grid(row=1, column=0, padx=10, pady=5)

        # Label|Date
        tk.Label(self.root, text="Enter how many days to go back", anchor="e").grid(
            row=2, column=0, padx=10, pady=5, sticky="e")
        self.dateEntry = ttk.Entry(
            self.root, textvariable=self.date, style="TEntry")
        self.dateEntry.grid(row=3, column=0, padx=10, pady=5)

        # Create a normal Tkinter Button, not a themed one
        graphButton = tk.Button(self.root, text='Candlestick', width=25,
                                command=self.createGraphCommand)
        graphButton.grid(row=2, column=1, padx=10, pady=5)

    def createGraphCommand(self):
        # get user input
        crypto = self.cryptoEntry.get()
        date = int(self.dateEntry.get())

        # store values in the instance variables
        self.crypto.set(crypto)
        self.date.set(date)

        # use values to create graph
        crypto_data = cg.get_coin_market_chart_by_id(
            id=crypto, vs_currency='usd', days=date)

        crypto_price_data = crypto_data['prices']

        data = pd.DataFrame(crypto_price_data, columns=['Timestamp', 'Price'])

        data['Date'] = pd.to_datetime(data['Timestamp'], unit='ms')

        candlestick_data = data.groupby(data.Date.dt.date).agg({'Price':
                                                                ['min', 'max', 'first', 'last']})

        fig = go.Figure(data=[go.Candlestick(x=candlestick_data.index,
                                             open=candlestick_data['Price']['first'],
                                             high=candlestick_data['Price']['max'],
                                             low=candlestick_data['Price']['min'],
                                             close=candlestick_data['Price']['last'],)
                              ])

        fig.update_layout(xaxis_rangeslider_visible=False, xaxis_title='Date',
                          yaxis_title='Price (USD$)', title=f'{crypto.upper()} Candlestick Chart Over Past 30 Days')

        fig.show()

    def createButton(self):
        graphButton = tk.Button(self.root, text='Candlestick', width=25,
                                command=self.createGraphCommand)
        graphButton.grid(row=2, column=1)

    # Run GUI

    def runUI(self):
        tk.mainloop()


if __name__ == "__main__":
    server = CryptoGUI()
