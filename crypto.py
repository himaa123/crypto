import http.client
import json

class PortfolioTracker:
    def __init__(self):
        self.portfolio = {}
        self.api_host = "api.coingecko.com"
        self.api_endpoint = "/api/v3/simple/price"

    def add_crypto(self, symbol, amount):
        """Add or update a cryptocurrency in the portfolio."""
        self.portfolio[symbol] = amount
        print(f"Added/Updated {symbol} with amount {amount}")

    def get_portfolio_value(self):
        """Fetch current prices and calculate portfolio value."""
        symbols = ','.join(self.portfolio.keys())
        conn = http.client.HTTPSConnection(self.api_host)
        params = f"?ids={symbols}&vs_currencies=usd"
        conn.request("GET", self.api_endpoint + params)
        
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()
        
        prices = json.loads(data)
        
        total_value = 0
        for symbol, amount in self.portfolio.items():
            price = prices.get(symbol, {}).get('usd', 0)
            total_value += price * amount
            print(f"{symbol.upper()}: ${price:.2f} x {amount} = ${price * amount:.2f}")
        
        return total_value

    def display_portfolio(self):
        """Display the current portfolio and its value."""
        if not self.portfolio:
            print("Portfolio is empty.")
            return
        
        print("\nYour Cryptocurrency Portfolio:")
        for symbol, amount in self.portfolio.items():
            print(f"{symbol.upper()}: {amount}")

        total_value = self.get_portfolio_value()
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")

def main():
    tracker = PortfolioTracker()

    while True:
        print("\nCryptocurrency Portfolio Tracker")
        print("1. Add/Update Cryptocurrency")
        print("2. View Portfolio")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            symbol = input("Enter the cryptocurrency symbol (e.g., bitcoin, ethereum): ").lower()
            try:
                amount = float(input("Enter the amount you own: "))
                tracker.add_crypto(symbol, amount)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '2':
            tracker.display_portfolio()
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")

if __name__ == "__main__":
    main()
