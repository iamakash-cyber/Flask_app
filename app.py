import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Function to fetch real-time stock data
def fetch_stock_data(ticker, period='1mo', interval='1d'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

# Function to plot stock data
def plot_stock_data(data, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label=f'{ticker} Close Price')
    plt.title(f'{ticker} Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.legend()
    plt.grid()
    plt.show()

# Function to display portfolio and track gains/losses
def track_portfolio(portfolio):
    print("\nYour Portfolio:")
    total_value = 0
    for ticker, shares in portfolio.items():
        current_price = fetch_stock_data(ticker, period='1d', interval='1d')['Close'][-1]
        stock_value = current_price * shares
        total_value += stock_value
        print(f"{ticker}: {shares} shares, Current Price: ${current_price:.2f}, Value: ${stock_value:.2f}")
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")

# Main program function
def main():
    portfolio = {}
    
    while True:
        print("\n--- Stock Market App ---")
        print("1. Check Stock Price")
        print("2. Plot Stock Data")
        print("3. Add to Portfolio")
        print("4. View Portfolio")
        print("5. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
            data = fetch_stock_data(ticker)
            current_price = data['Close'][-1]
            print(f"\n{ticker} Current Price: ${current_price:.2f}")
        
        elif choice == '2':
            ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
            data = fetch_stock_data(ticker)
            plot_stock_data(data, ticker)
        
        elif choice == '3':
            ticker = input("Enter stock ticker symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio[ticker] = portfolio.get(ticker, 0) + shares
            print(f"{shares} shares of {ticker} added to your portfolio.")
        
        elif choice == '4':
            if portfolio:
                track_portfolio(portfolio)
            else:
                print("Your portfolio is empty.")
        
        elif choice == '5':
            print("Exiting the app.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
