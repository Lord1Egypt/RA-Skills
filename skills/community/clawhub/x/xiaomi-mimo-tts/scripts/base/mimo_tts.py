#!/usr/bin/env python3
"""Python base implementation for xiaomi-mimo-tts with dry-run and robust error handling
Usage: python3 mimo_tts.py "文本" [output.ogg] [--voice VOICE] [--style STYLE] [--dry-run]
"""
import sys,os,subprocess, json, base64, urllib.request
if len(sys.argv)<2:
    print('Usage: python3 mimo_tts.py "TEXT" [OUTPUT] [--voice VOICE] [--style STYLE] [--dry-run]')
    sys.exit(2)
text=sys.argv[1]
output=sys.argv[2] if len(sys.argv)>2 and not sys.argv[2].startswith('--') else os.path.join(os.getcwd(),'output.mock.ogg')
voice='mimo_default'
style=''
args=sys.argv[2:]
for i,a in enumerate(args):
    if a=='--voice' and i+1<len(args): voice=args[i+1]
    if a=='--style' and i+1<len(args): style=args[i+1]
DRY = '--dry-run' in sys.argv

XIAOMI_API_KEY=os.environ.get('XIAOMI_API_KEY') or os.environ.get('MIMO_API_KEY')
MOCK = not XIAOMI_API_KEY
if DRY:
    body = {
        "model": "mimo-v2-tts",
        "messages": [
            {"role": "user", "content": "请朗读"},
            {"role": "assistant", "content": text}
        ],
        "audio": {"format": "wav", "voice": voice}
    }
    print('DRY RUN: request payload preview:')
    print(json.dumps(body, ensure_ascii=False, indent=2))
    sys.exit(0)

if MOCK:
    # generate mock silent ogg using ffmpeg if available
    try:
        subprocess.run(['ffmpeg','-f','lavfi','-i','anullsrc=r=16000:cl=mono','-t','0.5','-q:a','9','-acodec','libopus',output,'-y'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except Exception:
        open(output,'wb').close()
    print(output)
    sys.exit(0)

# Real implementation: call Xiaomi MiMo API and decode returned base64 audio
body = {
    "model": "mimo-v2-tts",
    "messages": [
        {"role": "user", "content": "请朗读"},
        {"role": "assistant", "content": text}
    ],
    "audio": {"format": "wav", "voice": voice}
}

req = urllib.request.Request(
    'https://api.xiaomimimo.com/v1/chat/completions',
    data=json.dumps(body).encode('utf-8'),
    headers={
        'Authorization': f'Bearer {XIAOMI_API_KEY}',
        'Content-Type': 'application/json'
    }
)
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        status = getattr(resp, 'status', None)
        resp_text = resp.read().decode('utf-8')
except Exception as e:
    print('API request failed:', e)
    sys.exit(1)

try:
    j = json.loads(resp_text)
except Exception as e:
    print('Invalid JSON response from API')
    print(resp_text)
    sys.exit(1)
if not status or status<200 or status>=300:
    print(f'API returned status {status}')
    if isinstance(j, dict) and j.get('error'):
        print('API error:', j['error'])
    sys.exit(1)

try:
    audio_b64 = j.get('choices', [])[0].get('message', {}).get('audio', {}).get('data')
    if not audio_b64:
        raise ValueError('no audio in response')
except Exception as e:
    print('Failed to parse audio from response:', e)
    print(resp_text)
    sys.exit(1)

wav = base64.b64decode(audio_b64)
wav_path = output + '.wav'
with open(wav_path, 'wb') as f:
    f.write(wav)

# convert wav to ogg if ffmpeg exists
try:
    subprocess.run(['ffmpeg','-y','-i',wav_path,'-acodec','libopus','-b:a','128k',output], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(wav_path)
except Exception as e:
    print('ffmpeg conversion failed:', e)
    print('Leaving wav at', wav_path)
    # keep wav as output
    if not os.path.exists(output):
        os.rename(wav_path, output)

print(output)
sys.exit(0)
