import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Global Portfolio Dictionary
portfolio = {}

# Fetch stock data function
def fetch_stock_data(ticker, period='1mo', interval='1d'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

# Create the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stock Market Dashboard"), width=12)
    ]),
    
    dbc.Row([
        # Input for stock ticker
        dbc.Col([
            dcc.Input(id="ticker-input", type="text", placeholder="Enter Stock Ticker (e.g., AAPL)", value="AAPL", debounce=True),
            html.Button('Add to Portfolio', id='add-to-portfolio', n_clicks=0, className="ml-2")
        ], width=6)
    ], className="my-2"),
    
    dbc.Row([
        # Display the graph for stock price
        dbc.Col([
            dcc.Graph(id="stock-graph")
        ], width=12)
    ]),
    
    dbc.Row([
        # Display Portfolio
        dbc.Col([
            html.H4("Your Portfolio"),
            html.Div(id='portfolio-div'),
        ], width=12)
    ])
])

# Callback to update the stock graph
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('ticker-input', 'value')]
)
def update_graph(ticker):
    if ticker:
        data = fetch_stock_data(ticker)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=ticker))
        fig.update_layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price in USD')
        return fig
    return go.Figure()

# Callback to update the portfolio and display it
@app.callback(
    Output('portfolio-div', 'children'),
    [Input('add-to-portfolio', 'n_clicks')],
    [State('ticker-input', 'value')]
)
def update_portfolio(n_clicks, ticker):
    global portfolio
    if n_clicks > 0 and ticker:
        data = fetch_stock_data(ticker)
        current_price = data['Close'][-1]
        if ticker not in portfolio:
            portfolio[ticker] = current_price
        # Create portfolio display
        portfolio_display = []
        total_value = 0
        for stock, price in portfolio.items():
            total_value += price
            portfolio_display.append(html.Div(f"{stock}: ${price:.2f}"))
        portfolio_display.append(html.Hr())
        portfolio_display.append(html.Div(f"Total Portfolio Value: ${total_value:.2f}"))
        return portfolio_display
    return "Portfolio is empty."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
