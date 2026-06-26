import argparse
import requests
from bs4 import BeautifulSoup
import chromadb
import uuid
import datetime
import json

# Filename: SanFrancisco-Today-FestivalEvents-Harvester-Agent.py
# Optimized for: NVIDIA DGX Spark / Jetson Orin NX

class SFEventHarvester:
    def __init__(self, db_path="./rag_db"):
        self.target_url = "https://sf.funcheap.com/today/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_or_create_collection(name="sf_today_events")

    def fetch_live_data(self, scope="top"):
        """Scrapes today's SF events with targeted metadata extraction."""
        try:
            response = requests.get(self.target_url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"Scraper connection failed: {e}"}

        soup = BeautifulSoup(response.content, "html.parser")
        events = []
        seen = set()
        
        # Scoping logic: 'top' for curated list, 'full' for entire page
        items = soup.select(".fc-topevents ol li") if scope == "top" else soup.find_all("div", class_="post")

        for item in items:
            anchor = item.find("a")
            if not anchor: continue
            
            title = anchor.get_text(strip=True)
            link = anchor.get("href", "")
            
            # Identify "Free" status from surrounding text
            raw_text = item.get_text(" ", strip=True)
            is_free = any(word in raw_text for word in ["Free", "$0", "No Cover"])
            
            if len(title) > 12 and title not in seen:
                seen.add(title)
                events.append({
                    "title": title,
                    "url": link,
                    "is_free": is_free,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "source": "SF Funcheap Today"
                })
        
        return events[:30]

    def sync_to_rag(self, data):
        """Vectorizes today's events for autonomous RAG retrieval."""
        count = 0
        for entry in data:
            uid = f"sf_today_{uuid.uuid4().hex[:6]}"
            content = f"Event: {entry['title']}. Cost: {'Free' if entry['is_free'] else 'Paid'}. URL: {entry['url']}"
            
            self.collection.upsert(
                documents=[content],
                metadatas=[entry],
                ids=[uid]
            )
            count += 1
        return count

    def query_memory(self, prompt):
        """Semantic search over harvested today-only events."""
        results = self.collection.query(query_texts=[prompt], n_results=5)
        return results["documents"][0]

def main():
    parser = argparse.ArgumentParser(description="San Francisco Today Festival & Events Harvester Agent")
    parser.add_argument("--action", choices=["list", "ingest", "search", "json"], default="list")
    parser.add_argument("--query", type=str, help="Search query for RAG")
    parser.add_argument("--scope", choices=["top", "full"], default="top")
    args = parser.parse_args()

    agent = SFEventHarvester()

    if args.action == "list":
        data = agent.fetch_live_data(scope=args.scope)
        for i, ev in enumerate(data, 1):
            status = "FREE" if ev['is_free'] else "PAID"
            print(f"{i}. [{status}] {ev['title']}")

    elif args.action == "ingest":
        data = agent.fetch_live_data(scope=args.scope)
        added = agent.sync_to_rag(data)
        print(f"[Agent] Successfully ingested {added} events into RAG context.")

    elif args.action == "search":
        if not args.query: 
            print("Error: Provide --query")
            return
        matches = agent.query_memory(args.query)
        print(f"\n--- RAG Results for: {args.query} ---")
        for m in matches: 
            print(f"- {m}")

    elif args.action == "json":
        data = agent.fetch_live_data(scope=args.scope)
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()