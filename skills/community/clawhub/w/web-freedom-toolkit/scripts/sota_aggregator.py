import os
import json
from curl_cffi import requests
from lxml import html

def comprehensive_intelligence_gathering():
    """
    SOTA Multi-Source Aggregator.
    """
    print("--- [SOTA AGGREGATOR: MULTI-SOURCE INTEL] ---")
    
    # 1. Target Definition
    targets = [
        {"name": "Cloudflare Security", "url": "https://blog.cloudflare.com/tag/security/"},
        {"name": "ScrapingAnt Tech", "url": "https://scrapingant.com/blog/"}
    ]
    
    knowledge_results = []
    
    for t in targets:
        print(f"Penetrating {t['name']} via Phantom Protocol...")
        try:
            r = requests.get(t['url'], impersonate="chrome124", timeout=15)
            if r.status_code == 200:
                tree = html.fromstring(r.content)
                items = [e.text_content().strip() for e in tree.xpath('//h2')[:5]]
                knowledge_results.append({"source": t['name'], "intel": items})
                print(f"Success: {len(items)} items recovered.")
        except Exception as e:
            print(f"Source {t['name']} bypass failed: {e}")

    # 2. Persistence
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output = os.path.join(base_dir, "assets/KNOWLEDGE_SYNC.json")
    
    with open(output, "w") as f:
        json.dump(knowledge_results, f, indent=2, ensure_ascii=False)
    
    print(f"Intelligence Matrix synced to: {output}")

if __name__ == "__main__":
    comprehensive_intelligence_gathering()
