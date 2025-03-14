
from fastapi import FastAPI
import requests

app = FastAPI()

DEFAULT_STOCKS = ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]
DEFAULT_CRYPTOS = ["bitcoin", "ethereum", "dogecoin", "solana", "cardano"]

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Live Market Data FinTech API",
        "endpoints": {
            "/stock/{symbol}": "Get real-time stock prices (e.g., AAPL, GOOGL, etc.)",
            "/crypto/{coin}": "Get real-time crypto prices (e.g., bitcoin, ethereum, etc.)"
        }
    }

@app.get("/stock/{symbol}")
def get_stock_price(symbol: str):
    API_KEY = "E51WWVGBCDS1VHDP"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    try:
        price = data["Global Quote"]["05. price"]
        return {"symbol": symbol, "price": float(price)}
    except:
        return {"error": "Stock not found or API limit exceeded"}

@app.get("/crypto/{coin}")
def get_crypto_price(coin: str):
    coin = coin.lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "API request failed"}

    data = response.json()
    
    if coin in data:
        return {"coin": coin, "price": data[coin]["usd"]}
    else:
        return {"error": f"Crypto '{coin}' not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
