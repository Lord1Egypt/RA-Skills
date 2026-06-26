import sys
import json
from scrapling.fetchers import StealthyFetcher

sys.stdout.reconfigure(encoding='utf-8')
url = "https://yandex.ru/archive/search?text=%D0%92%D0%B8%D0%B7%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2&rankMode=by_relevance&index=archive"

try:
    page = StealthyFetcher.fetch(url, headless=True, network_idle=True)
    
    # Look for Next.js data
    next_data = page.css('#__NEXT_DATA__::text').get()
    if next_data:
        data = json.loads(next_data)
        
        # Navigate to search results
        try:
            items = data['props']['pageProps']['items']
            print(f"Found {len(items)} items in JSON.")
            
            if items:
                first = items[0]
                print(json.dumps(first, indent=2, ensure_ascii=False))
        except KeyError as e:
            print(f"KeyError navigating JSON: {e}")
            
except Exception as e:
    print(f"Error: {e}")
