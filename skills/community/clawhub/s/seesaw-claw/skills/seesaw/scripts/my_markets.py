from seesaw import SeesawClient

api = SeesawClient()
markets = api.list_markets(status="active", limit=100)
markets_waiting = api.list_markets(status="waiting", limit=100)

if isinstance(markets, dict):
    markets = markets.get("items", markets.get("data", []))
if isinstance(markets_waiting, dict):
    markets_waiting = markets_waiting.get("items", markets_waiting.get("data", []))

all_m = markets + markets_waiting

MY_ID = "fca3cb34-04f0-4af6-b0cc-9c05281f341b"
my_markets = [m for m in all_m if m.get("creator", {}).get("id") == MY_ID]

for m in my_markets:
    print(f"ID: {m['id']}")
    print(f"Title: {m['title']}")
    print(f"Status: {m['status']}")
    print(f"End Time: {m.get('end_time')}")
    for opt in m['options']:
        print(f"  Option: {opt['id']} - {opt['name']} (Prob: {opt.get('current_probability')})")
    print("---")
    
if not my_markets:
    print("No markets found created by", MY_ID)
