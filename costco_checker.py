import time, requests

URL = "https://www.costco.ca/danby-12,000-btu-sacc-quick-connect-mini-split-air-conditioner-with-heat-pump-and-variable-speed-inverter.product.100789691.html"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# We'll fill these in GitHub Secrets later
PUSHOVER_USER = None
PUSHOVER_TOKEN = None

def check():
    r = requests.get(URL, headers=HEADERS, timeout=15)
    return "add to cart" in r.text.lower()

def notify():
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "message": f"Costco item IN STOCK!\n{URL}"
        }
    )

def main():
    while True:
        print("Checking stock...")
        if check():
            print("IN STOCK")
            notify()
            break
        time.sleep(600)

if __name__ == "__main__":
    main()
