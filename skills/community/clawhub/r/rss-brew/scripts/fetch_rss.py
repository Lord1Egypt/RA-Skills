import sys
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_feed(url):
    articles = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            # Atom format
            if 'http://www.w3.org/2005/Atom' in root.tag:
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                for entry in root.findall('atom:entry', ns)[:10]:
                    title = entry.find('atom:title', ns)
                    link = entry.find('atom:link', ns)
                    pub = entry.find('atom:published', ns) or entry.find('atom:updated', ns)
                    if title is not None and link is not None:
                        articles.append({
                            'source': url,
                            'title': title.text,
                            'link': link.attrib.get('href', ''),
                            'published': pub.text if pub is not None else ''
                        })
            # RSS 2.0 format
            else:
                for item in root.findall('.//item')[:10]:
                    title = item.find('title')
                    link = item.find('link')
                    pub = item.find('pubDate')
                    if title is not None and link is not None:
                        articles.append({
                            'source': url,
                            'title': title.text,
                            'link': link.text,
                            'published': pub.text if pub is not None else ''
                        })
    except Exception as e:
        return {"error": str(e), "url": url}
    return articles

if __name__ == "__main__":
    urls = sys.argv[1:]
    results = {}
    for url in urls:
        results[url] = parse_feed(url)
    print(json.dumps(results, indent=2))
