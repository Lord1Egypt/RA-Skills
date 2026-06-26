import datetime as dt
import xml.etree.ElementTree as ET
from typing import List, Dict
import requests

RSS_URL = "https://v2.velog.io/rss/{username}"


def fetch_user_rss(username: str) -> str:
    url = RSS_URL.format(username=username)
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text


def parse_rss(xml_text: str, limit: int = 10) -> List[Dict]:
    root = ET.fromstring(xml_text)
    # Typical RSS: <rss><channel><item>...</item></channel></rss>
    channel = root.find("channel")
    if channel is None:
        # Sometimes Atom? Try alternate namespace-aware
        # Fallback: return empty
        return []
    items = channel.findall("item")
    results = []
    for item in items[: max(1, limit)]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        # Normalize date if possible
        iso_date = pub_date
        try:
            # Example: Tue, 09 Apr 2024 13:24:00 GMT
            dt_obj = dt.datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
            iso_date = dt_obj.date().isoformat()
        except Exception:
            pass
        results.append({
            "title": title,
            "link": link,
            "date": iso_date,
        })
    return results
