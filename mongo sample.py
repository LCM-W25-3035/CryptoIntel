from pymongo import MongoClient

# Connect to the local MongoDB instance
client = MongoClient("mongodb://localhost:27017/")

# Create/select the database
db = client["kraken_data"]

# Create/select the collection
collection = db["trades"]

def save_trade(trade_data):
    """Insert trade data into MongoDB."""
    collection.insert_one(trade_data)
    print("Trade data saved to MongoDB:", trade_data)

# Example usage
if __name__ == "__main__":
    sample_trade = {
        "pair": "BTC/USD",
        "price": 42000.50,
        "volume": 0.1,
        "timestamp": 1707070800  # Example timestamp
    }
    save_trade(sample_trade)


def fetch_prices():
    """Fetch prices from Kraken API with error handling."""
    try:
        response = requests.get(KRAKEN_API_URL, params={"pair": ",".join(PAIRS)}, timeout=5)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        if "result" in data:
            for pair, info in data["result"].items():
                price = info["c"][0]  # Current price
                yield {
                    "pair": pair,
                    "price": float(price),
                    "timestamp": int(time.time())
                }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Kraken API: {e}")

def send_to_kafka():
    """Continuously fetch and send price data to Kafka."""
    while True:
        for price_data in fetch_prices():
            try:
                producer.send("kraken_prices", value=price_data)
                print(f"Sent: {price_data}")
            except Exception as e:
                print(f"Error sending to Kafka: {e}")
        time.sleep(5)  # Fetch price every 5 seconds

if __name__ == "__main__":
    send_to_kafka()
