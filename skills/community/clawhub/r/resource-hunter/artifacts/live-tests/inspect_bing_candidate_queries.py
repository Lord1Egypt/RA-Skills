import html
import re
import urllib.parse
import urllib.request

queries = [
    "quarkpan 网盘 搜索",
    "lanzou 网盘 搜索",
    "znds 阿里云盘",
    "site:pan.quark.cn 资源",
    "site:lanzoux.com 分享",
]

pattern = re.compile(r'<li class="b_algo".*?<h2><a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.S)

for query in queries:
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    text = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    hits = pattern.findall(text)
    print("QUERY", query)
    print("COUNT", len(hits))
    for href, title in hits[:10]:
        print("URL", href)
        print("TITLE", re.sub(r"<[^>]+>", " ", html.unescape(title)).strip())
        print("---")
    print("====")
