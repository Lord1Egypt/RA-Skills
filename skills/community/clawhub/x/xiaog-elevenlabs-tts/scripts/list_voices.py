#!/usr/bin/env python3
import json, os, sys, urllib.request, urllib.error
KEY=os.environ.get('ELEVENLABS_API_KEY')
if not KEY:
    print('Missing ELEVENLABS_API_KEY', file=sys.stderr); sys.exit(2)
req=urllib.request.Request('https://api.elevenlabs.io/v1/voices',headers={'xi-api-key':KEY,'User-Agent':'openclaw-elevenlabs-skill/1'})
try:
    with urllib.request.urlopen(req,timeout=30) as r:
        data=json.loads(r.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: '+e.read().decode('utf-8','ignore')[:1000], file=sys.stderr); sys.exit(1)
except Exception as e:
    print(f'Request failed: {type(e).__name__}: {e}', file=sys.stderr); sys.exit(1)
voices=data.get('voices',[])
for v in voices:
    print(json.dumps({
        'name':v.get('name'),
        'voice_id':v.get('voice_id'),
        'category':v.get('category'),
        'labels':v.get('labels',{}),
        'preview_url':v.get('preview_url')
    },ensure_ascii=False))
