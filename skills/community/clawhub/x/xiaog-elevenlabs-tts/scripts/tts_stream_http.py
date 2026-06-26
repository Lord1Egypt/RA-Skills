#!/usr/bin/env python3
import argparse, json, os, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

API='https://api.elevenlabs.io/v1'

def die(msg, code=1):
    print(msg, file=sys.stderr); sys.exit(code)

def request_json(path, key):
    req=urllib.request.Request(API+path,headers={'xi-api-key':key,'User-Agent':'openclaw-elevenlabs-skill/1'})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def resolve_voice_id(key, voice_id, voice_name):
    if voice_id: return voice_id
    data=request_json('/voices',key)
    voices=data.get('voices',[])
    if voice_name:
        q=voice_name.lower()
        for v in voices:
            if v.get('name','').lower()==q:
                return v.get('voice_id')
        for v in voices:
            if q in v.get('name','').lower():
                return v.get('voice_id')
        die(f'Voice not found: {voice_name}')
    if not voices: die('No voices available')
    return voices[0].get('voice_id')

p=argparse.ArgumentParser(description='ElevenLabs HTTP streaming TTS with TTFB benchmark')
p.add_argument('--text',required=True)
p.add_argument('--voice-id')
p.add_argument('--voice-name')
p.add_argument('--model',default='eleven_flash_v2_5')
p.add_argument('--output-format',default='mp3_44100_128')
p.add_argument('--optimize-streaming-latency',type=int,default=2)
p.add_argument('--stability',type=float,default=0.5)
p.add_argument('--similarity-boost',type=float,default=0.75)
p.add_argument('--style',type=float,default=0.0)
p.add_argument('--speaker-boost',action='store_true',help='Enable speaker boost; increases latency')
p.add_argument('--out',required=True)
args=p.parse_args()
key=os.environ.get('ELEVENLABS_API_KEY')
if not key: die('Missing ELEVENLABS_API_KEY',2)
try:
    voice_id=resolve_voice_id(key,args.voice_id,args.voice_name)
except Exception as e:
    die(f'Voice resolution failed: {type(e).__name__}: {e}')

query=urllib.parse.urlencode({'output_format':args.output_format,'optimize_streaming_latency':str(args.optimize_streaming_latency)})
url=f'{API}/text-to-speech/{urllib.parse.quote(voice_id)}/stream?{query}'
payload={
    'text':args.text,
    'model_id':args.model,
    'voice_settings':{
        'stability':args.stability,
        'similarity_boost':args.similarity_boost,
        'style':args.style,
        'use_speaker_boost':bool(args.speaker_boost),
    }
}
body=json.dumps(payload,ensure_ascii=False).encode('utf-8')
req=urllib.request.Request(url,data=body,method='POST',headers={'xi-api-key':key,'Content-Type':'application/json','User-Agent':'openclaw-elevenlabs-skill/1'})
out=Path(args.out).expanduser(); out.parent.mkdir(parents=True,exist_ok=True)
start=time.perf_counter(); first=None; chunks=0; total=0
try:
    with urllib.request.urlopen(req,timeout=120) as r, out.open('wb') as f:
        status=getattr(r,'status',None)
        while True:
            chunk=r.read(8192)
            if not chunk: break
            if first is None: first=time.perf_counter()
            chunks+=1; total+=len(chunk); f.write(chunk)
except urllib.error.HTTPError as e:
    err=e.read().decode('utf-8','ignore')[:1500]
    die(f'HTTP {e.code}: {err}')
except Exception as e:
    die(f'Request failed: {type(e).__name__}: {e}')
end=time.perf_counter()
if total<=0: die('No audio bytes returned')
print(json.dumps({
    'ok':True,
    'voice_id':voice_id,
    'model':args.model,
    'output_format':args.output_format,
    'optimize_streaming_latency':args.optimize_streaming_latency,
    'out':str(out),
    'bytes':total,
    'chunks':chunks,
    'ttfb_seconds':None if first is None else round(first-start,4),
    'elapsed_seconds':round(end-start,4),
    'chars':len(args.text),
    'speaker_boost':bool(args.speaker_boost)
},ensure_ascii=False,indent=2))
