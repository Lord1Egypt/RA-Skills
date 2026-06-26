import json
from pathlib import Path

p = Path('skills/resource-hunter/artifacts/live-tests/the-merry-widow-1952.json')
raw = p.read_bytes()
text = raw.decode('utf-16')
data = json.loads(text)

print('query=', data.get('query'))
print('candidate_count=', data.get('meta', {}).get('candidate_count'))
print('has_direct=', data.get('meta', {}).get('success_estimate', {}).get('has_direct'))
print('has_actionable=', data.get('meta', {}).get('success_estimate', {}).get('has_actionable'))
print('has_clues=', data.get('meta', {}).get('success_estimate', {}).get('has_clues'))
print('retrieval_layers=', [item.get('name') for item in data.get('meta', {}).get('retrieval_layers', [])])
print('top_results=')
for i, r in enumerate(data.get('results', [])[:5], 1):
    print(f"{i}. source={r.get('source')} provider={r.get('provider')} status={r.get('validation_status')} actionability={r.get('actionability')} bucket={r.get('match_bucket')} score={r.get('score')}")
    print('   title=', r.get('title'))
    print('   link=', r.get('link_or_magnet'))
    print('   password=', r.get('password'))
    print('   corroboration=', r.get('corroboration_count'), 'cluster=', r.get('cluster_id'))
    print('   reasons=', r.get('reasons'))
    print('   penalties=', r.get('penalties'))
    print('   validation_signals=', r.get('validation_signals'))
