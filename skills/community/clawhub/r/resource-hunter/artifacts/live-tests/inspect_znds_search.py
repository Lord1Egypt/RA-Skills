import html
import re
import urllib.request
from itertools import islice

url = 'https://www.znds.com/search.php?mod=forum&searchsubmit=yes&srchtxt=Attack%20on%20Titan'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
text = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'replace')
pattern = re.compile(r'<h3 class="c-title">\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.S)
hits = pattern.findall(text)
print('count', len(hits))
for href, title in islice(hits, 0, 20):
    print('URL', href)
    print('TITLE', re.sub(r'<[^>]+>', ' ', html.unescape(title)).strip())
    print('---')
