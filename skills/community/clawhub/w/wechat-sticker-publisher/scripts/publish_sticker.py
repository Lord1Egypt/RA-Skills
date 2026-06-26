#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / 'outputs'
OUTPUTS.mkdir(parents=True, exist_ok=True)

DEFAULT_ENV_CANDIDATES = [
    ROOT / 'wechat.env',
]
API_BASE = 'https://api.weixin.qq.com/cgi-bin'


def load_env_file(path: Path):
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[len('export '):]
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def load_default_envs():
    for candidate in DEFAULT_ENV_CANDIDATES:
        load_env_file(candidate)


def require_creds():
    load_default_envs()
    app_id = os.environ.get('WECHAT_APP_ID')
    app_secret = os.environ.get('WECHAT_APP_SECRET')
    if not app_id or not app_secret:
        raise SystemExit('Missing WECHAT_APP_ID / WECHAT_APP_SECRET')
    return app_id, app_secret


def get_access_token(app_id: str, app_secret: str) -> str:
    r = requests.get(
        f'{API_BASE}/token',
        params={
            'grant_type': 'client_credential',
            'appid': app_id,
            'secret': app_secret,
        },
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if 'access_token' not in data:
        raise RuntimeError(f'get_access_token failed: {data}')
    return data['access_token']


def add_material_image(access_token: str, image_path: Path):
    mime = mimetypes.guess_type(str(image_path))[0] or 'image/jpeg'
    with image_path.open('rb') as f:
        r = requests.post(
            f'{API_BASE}/material/add_material',
            params={'access_token': access_token, 'type': 'image'},
            files={'media': (image_path.name, f, mime)},
            timeout=120,
        )
    r.raise_for_status()
    data = r.json()
    if 'media_id' not in data:
        raise RuntimeError(f'add_material_image failed for {image_path.name}: {data}')
    return data


def draft_add_newspic(access_token: str, title: str, text: str, image_media_ids: list[str], author: str):
    payload = {
        'articles': [
            {
                'article_type': 'newspic',
                'title': title,
                'content': text,
                'digest': text,
                'author': author,
                'image_info': {
                    'image_list': [{'image_media_id': mid} for mid in image_media_ids]
                },
            }
        ]
    }
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    r = requests.post(
        f'{API_BASE}/draft/add',
        params={'access_token': access_token},
        data=body,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    if 'media_id' not in data:
        raise RuntimeError(f'draft_add_newspic failed: {data}')
    return payload, data


def write_output(name: str, data: dict):
    ts = time.strftime('%Y%m%d-%H%M%S')
    path = OUTPUTS / f'{ts}-{name}.json'
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', action='append', required=True, help='Absolute image path; can repeat up to 20')
    ap.add_argument('--title', required=True)
    ap.add_argument('--text', required=True)
    ap.add_argument('--author', default='OpenClaw')
    args = ap.parse_args()

    images = [Path(p).expanduser() for p in args.image]
    if len(images) > 20:
        raise SystemExit('At most 20 images allowed')
    for p in images:
        if not p.is_absolute():
            raise SystemExit(f'Image path must be absolute: {p}')
        if not p.exists():
            raise SystemExit(f'Image not found: {p}')

    app_id, app_secret = require_creds()
    access_token = get_access_token(app_id, app_secret)

    upload_results = []
    image_media_ids = []
    for p in images:
        res = add_material_image(access_token, p)
        upload_results.append({'file_name': p.name, 'result': res})
        image_media_ids.append(res['media_id'])

    draft_payload, draft_result = draft_add_newspic(access_token, args.title, args.text, image_media_ids, args.author)

    out = {
        'ok': True,
        'mode': 'newspic',
        'draft_only': True,
        'title': args.title,
        'text': args.text,
        'author': args.author,
        'image_file_names': [p.name for p in images],
        'uploads': upload_results,
        'draft_request': draft_payload,
        'draft_result': draft_result,
    }

    out_path = write_output('publish-sticker', out)
    print(json.dumps({
        'ok': True,
        'draft_only': True,
        'draft_media_id': draft_result.get('media_id'),
        'output': str(out_path),
    }, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except requests.HTTPError as e:
        detail = None
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text if e.response is not None else str(e)
        print(json.dumps({'ok': False, 'error': 'http_error', 'detail': detail}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
