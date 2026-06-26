from pathlib import Path
import re

text = Path('skills/resource-hunter/artifacts/live-tests/pansearch-search-bundle.js').read_text(encoding='utf-8')
for key in ['axios', 'fetch(', '/search', '/api', 'keyword', 'pageProps', 'pansearch.me', 'q:', 'data.total']:
    print(key, text.lower().count(key.lower()))
print('---MATCHES---')
pattern = re.compile(r'https?://[^\"\'""`\s)]+|/[A-Za-z0-9_./?=%-]{3,}')
seen = set()
for match in pattern.finditer(text):
    s = match.group(0)
    if ('search' in s or 'api' in s or 'pansearch' in s) and s not in seen:
        seen.add(s)
        print(s)
