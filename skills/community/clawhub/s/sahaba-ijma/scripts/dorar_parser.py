import sys, json, re, html, urllib.parse

raw = sys.stdin.read()
match = re.search(r'^\?\((.*)\)$', raw, re.DOTALL)
if not match:
    print('Error: Invalid response')
    sys.exit(1)

try:
    data = json.loads(match.group(1))
except json.JSONDecodeError as e:
    print(f'Error: JSON parse failed - {e}')
    sys.exit(1)

result_html = data.get('ahadith', {}).get('result', '')

if not result_html:
    print('No results found')
    sys.exit(0)

blocks = re.split(r'-{3,}', result_html)
results = []
for block in blocks:
    if not block.strip():
        continue
    clean = re.sub(r'<[^>]+>', '', block)
    clean = html.unescape(clean).strip()
    if clean:
        results.append(clean)

# Get query from environment or use empty
import os
query = os.environ.get('DORAR_QUERY', '')
search_url = 'https://dorar.net/hadith/search?q=' + urllib.parse.quote(query) if query else ''

for i, r in enumerate(results, 1):
    print(f'=== نتيجة {i} ===')
    print(r)
    if search_url:
        print()
        print(f'🔗 الرابط: {search_url}')
    print()
