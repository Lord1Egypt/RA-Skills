import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUOTES_FILE = os.path.join(SKILL_DIR, "data", "prepared_quotes.md")

def get_quotes():
    if not os.path.exists(QUOTES_FILE):
        return []
    quotes = []
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if '|' in line:
                # Use split with maxsplit=1 to handle titles containing pipes
                parts = line.strip().split('|', 1)
                if len(parts) == 2:
                    quotes.append(parts)
    return quotes

if __name__ == "__main__":
    quotes = get_quotes()
    for title, link in quotes:
        print(f"**[{title.strip()}]({link.strip()})**")
