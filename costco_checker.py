import requests
from bs4 import BeautifulSoup
import os

PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]

URL = "https://www.costco.ca/danby-12,000-btu-sacc-quick-connect-mini-split-air-conditioner-with-heat-pump-and-variable-speed-inverter.product.100789691.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def check():
    r = requests.get(URL, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    print("DEBUG: parsing Costco DOM...")

    page_text = soup.get_text(" ", strip=True).lower()
    html_lower = str(soup).lower()

    # -----------------------------
    # HARD NEGATIVE SIGNALS
    # -----------------------------
    negative_signals = [
        "sold out",
        "out of stock",
        "currently unavailable",
        "temporarily unavailable"
    ]

    if any(sig in page_text for sig in negative_signals):
        print("DEBUG: explicit out-of-stock signal detected")
        return False

    # -----------------------------
    # BUTTON / PURCHASE SIGNALS
    # -----------------------------
    buttons = soup.find_all(["button", "a", "div"])

    purchase_signals = [
        "add to cart",
        "buy now",
        "add to basket"
    ]

    button_hits = 0

    for b in buttons:
        text = b.get_text(" ", strip=True).lower()
        if any(sig in text for sig in purchase_signals):
            button_hits += 1

    print(f"DEBUG: button_hits={button_hits}")

    # -----------------------------
    # ATTRIBUTE SIGNALS
    # -----------------------------
    attribute_signals = [
        "add-to-cart",
        "pdp-add-to-cart",
        "addtocart",
        "button--add"
    ]

    attr_hits = sum(sig in html_lower for sig in attribute_signals)

    print(f"DEBUG: attr_hits={attr_hits}")

    score = button_hits + attr_hits

    print(f"DEBUG: total_score={score}")

    return score >= 1

def notify():
    print("Sending Pushover notification...")

    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "title": "Costco Restock Alert",
            "message": f"Danby Mini Split may be in stock!\n\n{URL}"
        },
        timeout=20
    )

if check():
    print("IN STOCK -> notifying")
    notify()
else:
    print("OUT OF STOCK")
