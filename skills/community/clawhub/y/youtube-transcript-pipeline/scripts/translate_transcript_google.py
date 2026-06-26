#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys
import urllib.parse
import urllib.request
import time
import re

TS_RE = re.compile(r"^(\[\d{2}:\d{2}:\d{2}\]\s*[^:]+:\s*)(.*)$")

def translate_batch(lines, source='en', target='zh-CN', retries=3):
    text = "\n".join(lines)
    qs = urllib.parse.urlencode({
        'client': 'gtx',
        'sl': source,
        'tl': target,
        'dt': 't',
        'q': text,
    })
    url = 'https://translate.googleapis.com/translate_a/single?ie=UTF-8&oe=UTF-8&hl=zh-CN&' + qs.replace('+','%20')
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0'
    })
    for _ in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read().decode('utf-8')
            # response is nested JSON-like list
            obj = json.loads(data)
            chunks = obj[0]
            out = []
            for seg in chunks:
                if seg and isinstance(seg, list) and seg[0]:
                    out.append(seg[0])
            return ''.join(out)
        except Exception:
            time.sleep(1)
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='infile', required=True)
    ap.add_argument('--out', dest='outfile', required=True)
    args = ap.parse_args()

    in_path = Path(args.infile)
    out_path = Path(args.outfile)
    if not in_path.exists():
        raise SystemExit(f'missing input: {in_path}')

    lines = in_path.read_text(encoding='utf-8').splitlines()
    out_lines = []
    for line in lines:
        m = TS_RE.match(line)
        if not m:
            out_lines.append(line)
            continue
        prefix, body = m.groups()
        translated = translate_batch([body])
        if not translated:
            out_lines.append(line)
        else:
            out_lines.append(f"{prefix}{translated}")

    out_path.write_text('\n'.join(out_lines) + ('\n' if lines and not lines[-1].endswith('\n') else ''), encoding='utf-8')

if __name__ == '__main__':
    main()
