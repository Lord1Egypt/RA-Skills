#!/usr/bin/env python3
import json
import pathlib
import sys
import requests

CONFIGS = [
    pathlib.Path('E:/openclaw/.openclaw/openclaw.json'),
    pathlib.Path('E:/openclaw/.openclaw/openclaw.json'),
]
API_URL = 'https://api.siliconflow.cn/v1/images/generations'
MODEL = 'Kwai-Kolors/Kolors'


def load_key() -> str:
    import os
    for name in ('SILICONFLOW_API_KEY', 'API_KEY'):
        v = os.environ.get(name)
        if v:
            return v
    for p in CONFIGS:
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
            models = (data.get('models') or {}).get('providers') or {}
            key = (models.get('siliconflow') or {}).get('apiKey')
            if key:
                return key
            memory_remote = (((data.get('agents') or {}).get('defaults') or {}).get('memorySearch') or {}).get('remote') or {}
            key = memory_remote.get('apiKey')
            base_url = memory_remote.get('baseUrl', '')
            if key and 'siliconflow.cn' in base_url:
                return key
        except Exception:
            continue
    raise SystemExit(json.dumps({'ok': False, 'error': 'missing_siliconflow_api_key'}, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        raise SystemExit('Usage: txt2img.py \'{"prompt":"..."}\'')
    body = json.loads(sys.argv[1])
    prompt = body.get('prompt')
    if not prompt:
        raise SystemExit(json.dumps({'ok': False, 'error': 'prompt_required'}, ensure_ascii=False))

    payload = {
        'model': MODEL,
        'prompt': prompt,
        'image_size': body.get('image_size', '1024x1024'),
        'batch_size': int(body.get('batch_size', 1)),
        'num_inference_steps': int(body.get('num_inference_steps', 20)),
        'guidance_scale': float(body.get('guidance_scale', 7.5)),
    }

    headers = {
        'Authorization': f'Bearer {load_key()}',
        'Content-Type': 'application/json',
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=180)
    try:
        data = resp.json()
    except Exception:
        data = {'raw': resp.text}
    print(json.dumps({'ok': resp.ok, 'status': resp.status_code, 'data': data}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
