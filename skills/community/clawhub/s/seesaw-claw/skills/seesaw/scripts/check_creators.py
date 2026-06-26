from seesaw import SeesawClient

api = SeesawClient()
markets = api.list_markets(status="active", limit=100)
for m in markets.get("data", []):
    print(f"Creator: {m.get('creator', {}).get('nickname')} / {m.get('creator', {}).get('id')}")
