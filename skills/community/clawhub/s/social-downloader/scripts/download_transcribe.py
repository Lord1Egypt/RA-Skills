#!/usr/bin/env python3
import argparse, json, os, pathlib, subprocess, sys, urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('--out', default='reel-download')
args = parser.parse_args()
out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)
video_tpl = str(out / 'video.%(ext)s')
subprocess.run(['yt-dlp', '-f', 'bv*+ba/best', '--merge-output-format', 'mp4', '-o', video_tpl, args.url], check=True)
mp4 = next(out.glob('video.*'))
audio = out / 'audio.wav'
subprocess.run(['ffmpeg', '-y', '-i', str(mp4), '-vn', '-ac', '1', '-ar', '16000', str(audio)], check=True)
result = {'video': str(mp4), 'audio': str(audio)}
key = os.environ.get('OPENAI_API_KEY')
if key:
    import mimetypes, uuid
    boundary = '----openclaw' + uuid.uuid4().hex
    body = []
    def part(name, value, filename=None, ctype='text/plain'):
        body.append(f'--{boundary}\r\n'.encode())
        if filename:
            body.append(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\nContent-Type: {ctype}\r\n\r\n'.encode()); body.append(value); body.append(b'\r\n')
        else:
            body.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    part('model', 'gpt-4o-mini-transcribe')
    part('response_format', 'json')
    part('file', audio.read_bytes(), audio.name, 'audio/wav')
    body.append(f'--{boundary}--\r\n'.encode())
    req = urllib.request.Request('https://api.openai.com/v1/audio/transcriptions', data=b''.join(body), headers={'Authorization': f'Bearer {key}', 'Content-Type': f'multipart/form-data; boundary={boundary}'})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode())
    (out / 'transcript.txt').write_text(data.get('text',''))
    result['transcript'] = str(out / 'transcript.txt')
else:
    result['transcript'] = None
(out / 'result.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
