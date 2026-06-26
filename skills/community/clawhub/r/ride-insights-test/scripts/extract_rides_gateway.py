#!/usr/bin/env python3
"""Extract ride records from emails.json using OpenClaw Gateway /v1/responses into rides.json."""

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_CFG = Path.home() / '.openclaw' / 'openclaw.json'

SYSTEM_PROMPT = """You are extracting a structured ride record from ONE ride receipt email.
Use text_html as primary. Use snippet only if text_html is empty.
Return EXACTLY one JSON object matching this schema:
{
  \"provider\": \"Uber|Bolt|Yandex|Lyft|FreeNow|Curb|Via|Other\",
  \"source\": {\"gmail_message_id\":\"...\",\"email_date\":\"YYYY-MM-DD HH:MM\",\"subject\":\"...\"},
  \"ride\": {
    \"start_time_text\": \"...\",
    \"end_time_text\": \"...\",
    \"total_text\": \"...\",
    \"currency\": \"3-letter ISO code or null\",
    \"amount\": 12.34,
    \"pickup\": \"...\",
    \"dropoff\": \"...\",
    \"pickup_city\": \"...\",
    \"pickup_country\": \"...\",
    \"dropoff_city\": \"...\",
    \"dropoff_country\": \"...\",
    \"payment_method\": \"...\",
    \"driver\": \"...\",
    \"distance_text\": \"...\",
    \"duration_text\": \"...\",
    \"notes\": \"...\"
  }
}
Rules:
- Never hallucinate explicit facts that are not supported by the email. If unclear, use null.
- Keep addresses and time strings verbatim.
- Normalize currency to a 3-letter code only when confidently inferable.
- amount must be numeric; otherwise set amount=null and preserve the string in total_text.
- For Yandex, `р.` may mean BYN, and `₽` means RUB when clearly shown.
- For cancellation or adjustment receipts, route/time/distance fields may legitimately be null.
- Try hard to infer pickup_city, pickup_country, dropoff_city, and dropoff_country from the full email context, provider branding, language, currency, repeated route/location clues, and the pickup/dropoff address text.
- For city/country fields, use your best supported guess from the email when the address strongly implies a location, even if the city/country is not explicitly printed next to that field.
- If multiple plausible city/country interpretations remain and the email does not support one clearly enough, set the field to null.
- Do not invent street addresses or overwrite verbatim pickup/dropoff strings.
- Return JSON only. No markdown fences, no explanation."""


def is_trusted_gateway_host(hostname: str | None) -> bool:
    if not hostname:
        return False
    host = hostname.lower()
    if host in {'localhost', '127.0.0.1', '::1'}:
        return True
    if host.startswith('10.') or host.startswith('192.168.'):
        return True
    if re.match(r'^172\.(1[6-9]|2\d|3[0-1])\.', host):
        return True
    if host.endswith('.local') or host.endswith('.internal') or host.endswith('.ts.net'):
        return True
    return False


def load_gateway_settings():
    cfg = {}
    if DEFAULT_CFG.exists():
        cfg = json.loads(DEFAULT_CFG.read_text(encoding='utf-8'))
    port = cfg.get('gateway', {}).get('port', 18789)
    token = os.environ.get('OPENCLAW_GATEWAY_TOKEN') or cfg.get('gateway', {}).get('auth', {}).get('token')
    base_url = os.environ.get('OPENCLAW_GATEWAY_URL') or f'http://127.0.0.1:{port}'
    model = os.environ.get('OPENCLAW_GATEWAY_MODEL', 'openclaw:main')
    allow_nonlocal = os.environ.get('OPENCLAW_ALLOW_NONLOCAL_GATEWAY') == '1'
    if not token:
        raise RuntimeError('Missing Gateway token. Set OPENCLAW_GATEWAY_TOKEN or configure ~/.openclaw/openclaw.json')
    parsed = urlparse(base_url)
    if not allow_nonlocal and not is_trusted_gateway_host(parsed.hostname):
        raise RuntimeError(
            f'Refusing to send ride email content to non-local Gateway host {parsed.hostname}. '
            'Use localhost/private hosts only, or set OPENCLAW_ALLOW_NONLOCAL_GATEWAY=1 to override.'
        )
    return base_url.rstrip('/'), token, model


def extract_json(text: str):
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1 or end <= start:
        raise ValueError('No JSON object found')
    return json.loads(text[start:end+1])


def call_gateway(email_obj: dict, timeout: int = 180):
    base_url, token, model = load_gateway_settings()
    prompt = SYSTEM_PROMPT + "\n\nEmail JSON:\n" + json.dumps(email_obj, ensure_ascii=False)
    payload = {
        'model': model,
        'input': prompt,
    }
    req = urllib.request.Request(
        f'{base_url}/v1/responses',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode('utf-8'))
    for item in body.get('output', []):
        if item.get('type') == 'message':
            texts = [p.get('text', '') for p in item.get('content', []) if p.get('type') == 'output_text']
            joined = '\n'.join(t for t in texts if t)
            if joined.strip():
                return extract_json(joined)
    raise RuntimeError('No output_text in Gateway response')


def normalize(result: dict, email_obj: dict):
    result = result or {}
    source = result.get('source') or {}
    ride = result.get('ride') or {}
    return {
        'provider': result.get('provider') or email_obj.get('provider') or 'Other',
        'source': {
            'gmail_message_id': source.get('gmail_message_id') or email_obj.get('gmail_message_id'),
            'email_date': source.get('email_date') or email_obj.get('email_date'),
            'subject': source.get('subject') or email_obj.get('subject'),
        },
        'ride': {k: ride.get(k) for k in [
            'start_time_text','end_time_text','total_text','currency','amount','pickup','dropoff',
            'pickup_city','pickup_country','dropoff_city','dropoff_country','payment_method','driver',
            'distance_text','duration_text','notes'
        ]},
    }


def write_results(out_path: Path, results: list[dict]):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--emails-json', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--delay-ms', type=int, default=0)
    args = ap.parse_args()

    emails = json.loads(Path(args.emails_json).read_text(encoding='utf-8'))
    if args.limit > 0:
        emails = emails[:args.limit]

    out_path = Path(args.out)
    results = []
    completed_ids = set()
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text(encoding='utf-8'))
            if isinstance(existing, list):
                results = existing
                for item in existing:
                    mid = ((item.get('source') or {}).get('gmail_message_id'))
                    if mid:
                        completed_ids.add(mid)
        except Exception:
            pass

    remaining = [e for e in emails if e.get('gmail_message_id') not in completed_ids]

    for idx, email_obj in enumerate(remaining, start=1):
        mid = email_obj.get('gmail_message_id')
        for attempt in range(1, 4):
            try:
                extracted = normalize(call_gateway(email_obj), email_obj)
                results.append(extracted)
                if mid:
                    completed_ids.add(mid)
                write_results(out_path, results)
                break
            except Exception as err:
                if attempt == 3:
                    raise RuntimeError(f'Failed on gmail_message_id={mid}: {err}') from err
                time.sleep(2 * attempt)
        if args.delay_ms > 0 and idx < len(remaining):
            time.sleep(args.delay_ms / 1000.0)

    write_results(out_path, results)
    print(f'Wrote {len(results)} rides to {out_path}')


if __name__ == '__main__':
    main()
