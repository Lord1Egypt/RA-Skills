import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUOTES_FILE = os.path.join(SKILL_DIR, "data", "prepared_quotes.md")

# Interests based on our conversation and context
INTERESTS = ["AI", "OpenAI", "Google", "Apple", "MacBook", "Steam", "Valve", "Technology", "China", "Tesla", "GPU"]

def get_curated_quotes():
    if not os.path.exists(QUOTES_FILE):
        return []
    
    curated = []
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if '|' in line:
                parts = line.strip().split('|', 1)
                title = parts[0]
                # If title contains any interest, keep it. 
                # Also keep it if it looks like a major tech headline (broad filter)
                if any(interest.lower() in title.lower() for interest in INTERESTS) or len(title.split()) > 10:
                    curated.append(parts)
    return curated

if __name__ == "__main__":
    quotes = get_curated_quotes()
    # Limit to top 5 items for "precision curation" instead of 20 items
    for title, link in quotes[:5]:
        print(f"**[{title.strip()}]({link.strip()})**")
