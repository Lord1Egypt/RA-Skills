import sys, json
from urllib.parse import urlparse

def get_domain(url):
    try:
        host = urlparse(url).netloc.lower()
        if ':' in host:
            host = host.split(':')[0]
        return host
    except:
        return ''

if len(sys.argv) < 3:
    print("Usage: filter_blocklist.py <blocklist.json> <input.json>", file=sys.stderr)
    sys.exit(1)

blocklist_file = sys.argv[1]
input_file = sys.argv[2]

try:
    with open(blocklist_file, 'r') as f:
        blocklist = json.load(f)
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Build blocked set from root domains only
    blocked = set(item['domain'] for item in blocklist.get('blocked', []))
    
    orig = len(data.get('results', []))
    kept = []
    for r in data.get('results', []):
        d = get_domain(r.get('url', ''))
        if not any(d == b or d.endswith('.' + b) for b in blocked):
            kept.append(r)
    data['results'] = kept
    
    dropped = orig - len(data['results'])
    if dropped:
        print(f'[BLOCKLIST] Filtered {dropped} results', file=sys.stderr)
    print(json.dumps(data, ensure_ascii=False))

except Exception as e:
    print(f'[BLOCKLIST] Error: {e}', file=sys.stderr)
    try:
        with open(input_file, 'r') as f:
            print(f.read(), end='')
    except:
        pass
