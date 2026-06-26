import sys
from scrapling.fetchers import StealthyFetcher

sys.stdout.reconfigure(encoding='utf-8')
url = "https://yandex.ru/archive/catalog/40a9f877-75c1-4d9a-bc5e-25cad37ad7db/697"
print(f"Fetching {url}...")

try:
    page = StealthyFetcher.fetch(url, headless=True, network_idle=True)
    
    # Try to get the recognized text. Yandex Archive usually puts it in a specific div.
    all_text = " ".join(page.css('body::text').getall())
    
    # Find the context around "Визжалов"
    idx = all_text.find("Визжалов")
    if idx != -1:
        start = max(0, idx - 500)
        end = min(len(all_text), idx + 500)
        print(f"Context around 'Визжалов':\n{all_text[start:end]}")
    else:
        print("Word 'Визжалов' not found in direct text dump.")
        
        # Let's try to find any elements containing the text
        # Scrapling uses css/xpath, let's try xpath
        elements = page.xpath('//*[contains(text(), "Визжалов")]')
        for el in elements:
            print(f"Found in element: {el.text}")
            
    # Let's also print the breadcrumbs or title to get the year
    breadcrumbs = page.css('a[class*="breadcrumb"], span[class*="breadcrumb"], h1, h2, h3').getall()
    for b in breadcrumbs:
        print(f"Header/Breadcrumb: {b.text}")

except Exception as e:
    print(f"Error: {e}")
