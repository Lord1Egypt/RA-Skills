import sys
from duckduckgo_search import DDGS

def search(query):
    print(f"Searching for: {query}...")
    results = DDGS().text(query, max_results=3)
    
    if not results:
        print("No results found.")
        return

    for i, r in enumerate(results):
        print(f"--- Result {i+1} ---")
        print(f"Title: {r['title']}")
        print(f"Link: {r['href']}")
        print(f"Snippet: {r['body']}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        search(query)
    else:
        print("Error: No search query provided.")
