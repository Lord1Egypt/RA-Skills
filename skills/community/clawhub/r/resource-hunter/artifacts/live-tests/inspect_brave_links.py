import re
from pathlib import Path

html = Path('skills/resource-hunter/artifacts/live-tests/brave-attack-on-titan.html').read_text(encoding='utf-8')
pattern = re.compile(r'<a href="(https?://[^"]+)" target="_self" class="svelte-14r20fy l1">', re.S)
for idx, match in enumerate(pattern.finditer(html), 1):
    start = max(0, match.start() - 120)
    end = min(len(html), match.start() + 900)
    print(f'RESULT {idx}: {match.group(1)}')
    print(html[start:end])
    print('---')
    if idx >= 5:
        break
