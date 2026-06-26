import html
import re
import urllib.parse
import urllib.request
from itertools import islice

queries = [
    "进击的巨人 夸克",
    "奥本海默 阿里云盘",
    "赤橙黄绿青蓝紫 网盘",
]
pattern = re.compile(r'<h3 class="c-title">\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.S)

for query in queries:
    url = "https://www.znds.com/search.php?mod=forum&searchsubmit=yes&srchtxt=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    text = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    hits = pattern.findall(text)
    print("QUERY", query)
    print("COUNT", len(hits))
    for href, title in islice(hits, 0, 15):
        print("URL", href)
        print("TITLE", re.sub(r"<[^>]+>", " ", html.unescape(title)).strip())
        print("---")
    print("====")
