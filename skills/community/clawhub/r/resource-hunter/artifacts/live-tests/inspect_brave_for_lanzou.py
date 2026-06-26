import html
import re
import urllib.parse
import urllib.request

queries = [
    "lanzou 网盘 搜索",
    "quarkpan 网盘 搜索",
    "site:lanzoux.com 分享",
    "site:pan.quark.cn 资源",
]
pattern = re.compile(r'<a href="(https?://[^"]+)" target="_self" class="svelte-14r20fy l1">.*?<div class="title .*?"[^>]*>(.*?)</div>', re.S | re.I)

for query in queries:
    url = "https://search.brave.com/search?" + urllib.parse.urlencode({"q": query})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    text = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    hits = pattern.findall(text)
    print("QUERY", query)
    print("COUNT", len(hits))
    for href, title in hits[:10]:
        print("URL", html.unescape(href))
        print("TITLE", re.sub(r"<[^>]+>", " ", html.unescape(title)).strip())
        print("---")
    print("====")
