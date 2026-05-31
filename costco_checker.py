import time, requests, os

URL = "https://www.costco.ca/danby-12,000-btu-sacc-quick-connect-mini-split-air-conditioner-with-heat-pump-and-variable-speed-inverter.product.100789691.html"
HEADERS = {"User-Agent": "Mozilla/5.0"}

PUSHOVER_USER = os.environ.get("PUSHOVER_USER")
PUSHOVER_TOKEN = os.environ.get("PUSHOVER_TOKEN")

def check():
 def check():
    print("TEST MODE: forcing IN STOCK result")
    return True

def notify():
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "message": f"🔥 Costco item IN STOCK!\n{URL}"
        }
    )

def main():
    print("Checking Costco once...")
    if check():
        print("IN STOCK → sending alert")
        notify()
    else:
        print("Out of stock")

if __name__ == "__main__":
    main()
