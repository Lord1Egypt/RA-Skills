import urllib.request
import json
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")

def validate_subreddits():
    if not os.path.exists(CONFIG_FILE):
        print("Error: Config file not found.")
        return

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    subreddits = config.get("subreddits", [])
    valid_subs = []
    
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'}

    print("Checking subreddits...")
    for sub in subreddits:
        # Check if subreddit starts with r/
        if not sub.startswith("r/"):
            sub_name = f"r/{sub}"
        else:
            sub_name = sub
            
        url = f"https://www.reddit.com/{sub_name}/.rss"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    print(f"[OK] {sub_name}")
                    valid_subs.append(sub_name)
                else:
                    print(f"[WARN] {sub_name} returned status {response.status}")
        except Exception as e:
            print(f"[ERROR] {sub_name} failed: {e}")

    print(f"\nValidation complete. {len(valid_subs)}/{len(subreddits)} subreddits are valid.")

if __name__ == "__main__":
    validate_subreddits()
