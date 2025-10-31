import requests, time,sqlite3

API_KEY = "YOUR_ALPHA_VANTAGE_KEY"
SYMBOLS = ["AAPL", "MSFT", "GOOGL"]

conn = sqlite3.connect("stocks.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS prices (symbol TEXT, price REAL, timestamp TEXT)''')

def fetch_price(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    data = requests.get(url).json()
    return float(data['Global Quote']['05. price'])

while True:
    for s in SYMBOLS:
        price = fetch_price(s)
        c.execute("INSERT INTO prices VALUES (?, ?, datetime('now'))", (s, price))
        conn.commit()
    time.sleep(60)
