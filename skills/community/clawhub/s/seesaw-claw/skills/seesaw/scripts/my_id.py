from seesaw import SeesawClient
import json

api = SeesawClient()
try:
    print(json.dumps(api._request("GET", "users/me"), indent=2))
except Exception as e:
    print("Failed to get me:", e)
    
