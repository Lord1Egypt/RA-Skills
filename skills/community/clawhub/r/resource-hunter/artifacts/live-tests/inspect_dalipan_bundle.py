from pathlib import Path
import re

text = Path('skills/resource-hunter/artifacts/live-tests/dalipan-app-bundle.js').read_text(encoding='utf-8')
for key in ['axios', 'fetch(', '/search', '/api', 'keyword', 'query', 'baidu', 'quark', 'aliyun', 'xunlei']:
    print(key, text.lower().count(key.lower()))
print('---MATCHES---')
pattern = re.compile(r'https?://[^\"\'""`\s)]+|/[A-Za-z0-9_./?=%-]{3,}')
seen = set()
for match in pattern.finditer(text):
    s = match.group(0)
    if any(token in s.lower() for token in ['search', 'api', 'dalipan', 'pan', 'baidu', 'quark', 'aliyun']):
        if s not in seen:
            seen.add(s)
            print(s)
