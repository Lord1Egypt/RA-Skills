#!/usr/bin/env python3
import json
import sys
import time
import urllib.request

if len(sys.argv) < 2:
    print('用法: python3 scripts/poll-login-status.py <qrcode> [interval_seconds] [max_polls]', file=sys.stderr)
    sys.exit(2)

qrcode = sys.argv[1]
interval = float(sys.argv[2]) if len(sys.argv) >= 3 else 2.0
max_polls = int(sys.argv[3]) if len(sys.argv) >= 4 else 30
url = f'https://ilinkai.weixin.qq.com/ilink/bot/get_qrcode_status?qrcode={qrcode}'
headers = {'iLink-App-ClientVersion': '1'}

for i in range(max_polls):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=40) as resp:
        data = json.loads(resp.read().decode())
    print(time.strftime('%H:%M:%S'), json.dumps(data, ensure_ascii=False))
    status = data.get('status')
    if status in ('confirmed', 'expired') or data.get('bot_token'):
        break
    if i < max_polls - 1:
        time.sleep(interval)
