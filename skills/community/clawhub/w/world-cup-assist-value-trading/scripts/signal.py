import os
import re
import requests
from simmer_sdk import SimmerClient

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
DRY_RUN = True
THRESHOLD = 0.08
MIN_PRICE = 0.02
MAX_TRADE_USD = 10
MAX_TRADES_PER_RUN = 5
SKILL_SLUG = "world-cup-assist-value-trading"

client = SimmerClient.from_env()

def get_all_players():
    markets = client.get_markets(q="assists", limit=50)
    players = []
    for m in markets:
        if "assist" in m.question.lower():
            players.append({"name": m.question, "market_id": m.id, "price": m.current_probability})
    return players

def tavily_search(query):
    r = requests.post("https://api.tavily.com/search", json={"api_key": TAVILY_API_KEY, "query": query, "max_results": 3, "include_domains": ["fbref.com", "espn.com", "whoscored.com"]})
    results = r.json().get("results", [])
    return " ".join([x.get("content", "") for x in results])

def find_number(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None

def get_expected_price(name):
    club = tavily_search(name + " 2024-2025 season assists statistics fbref")
    wc = tavily_search(name + " World Cup 2026 assists goal contributions")
    combined = club + " " + wc
    assists = find_number(combined, [r"(\d+\.?\d*)\s*assists", r"Ast[:\s]+(\d+\.?\d*)"])
    score = 0.08
    if assists:
        score += min(float(assists) / 50 * 0.12, 0.12)
    if "assist" in wc.lower():
        score += 0.02
    return min(score, 0.45)

print("=== World Cup Assist Value SIGNAL TOOL (template, not a tested edge) ===")
print("Dry-run by default. Caps: $" + str(MAX_TRADE_USD) + "/trade, " + str(MAX_TRADES_PER_RUN) + " trades/run.")
print("This prints signals only; it does not place trades. Fair-value formula is an unbacktested first pass.")
print()

players = get_all_players()
print("Found " + str(len(players)) + " players")
print()

signals = []
for player in players:
    name = player["name"]
    price = player["price"]
    if price < MIN_PRICE:
        continue
    expected = get_expected_price(name)
    discount = (expected - price) / expected if expected > 0 else 0
    if discount >= THRESHOLD:
        signals.append({"name": name, "price": price, "expected": expected, "discount": discount, "market_id": player["market_id"]})

signals.sort(key=lambda x: x["discount"], reverse=True)
signals = signals[:MAX_TRADES_PER_RUN]

print("=== SIGNALS ===")
for s in signals:
    print(s["name"] + " | Market: " + str(round(s["price"],3)) + " | Expected: " + str(round(s["expected"],3)) + " | Discount: " + str(round(s["discount"]*100,1)) + "%")
    if not DRY_RUN:
        client.trade(market_id=s["market_id"], side="yes", amount=MAX_TRADE_USD, venue="sim", source="sdk:" + SKILL_SLUG, reasoning="Form-based expected price " + str(round(s["expected"],3)) + " vs market " + str(round(s["price"],3)) + ", discount " + str(round(s["discount"]*100,1)) + "%")
print()
print("Total signals: " + str(len(signals)))
