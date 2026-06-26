#!/usr/bin/env python3
"""
X5 Protocol Client CLI

Sends X5 protocol API requests from the terminal.
Implements Xiaomi's X5 protocol: signature generation, Base64 encoding, and HTTP transport.

Usage:
    python3 x5_client.py --file request.x5 --json
    python3 x5_client.py --appid X --appkey Y --url Z --method M --body '{"k":"v"}' --json
    python3 x5_client.py --file request.x5 --curl
    python3 x5_client.py --file request.x5 --list
"""

import argparse
import base64
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Compact JSON serialization to match Node.js JSON.stringify behavior
COMPACT_SEPARATORS = (',', ':')


# ─── .x5 File Parser ───────────────────────────────────────────────────────────

def parse_x5_file(content: str) -> list[dict]:
    """Parse a .x5 file and return a list of request dicts.

    Each request dict has keys: name, appid, appkey, url, method, body, headers.
    """
    requests: list[dict] = []
    sections = re.split(r'^###\s*.*$', content, flags=re.MULTILINE)

    for section in sections:
        section = section.strip()
        if not section:
            continue
        req = _parse_single_request(section)
        if req:
            requests.append(req)

    return requests


def _parse_single_request(content: str) -> dict | None:
    """Parse a single X5 request block."""
    lines = content.split('\n')
    result: dict = {}
    variables: dict[str, str] = {}
    headers: dict[str, str] = {}
    body_lines: list[str] = []
    in_body = False

    for i, raw_line in enumerate(lines):
        line = raw_line.strip()

        # Skip ### separators and # comments
        if line.startswith('###') or line.startswith('#'):
            continue

        # Body starts with { or [
        if not in_body and (line.startswith('{') or line.startswith('[')):
            in_body = True

        # Parse @ directives (only before body)
        if line.startswith('@') and not in_body:
            m = re.match(r'^@(\w+)\s*=\s*(.+)$', line)
            if m:
                key, value = m.group(1), _remove_quotes(m.group(2).strip())
                key_lower = key.lower()
                if key_lower == 'name':
                    result['name'] = value
                elif key_lower == 'appid':
                    result['appid'] = value
                elif key_lower == 'appkey':
                    result['appkey'] = value
                elif key_lower == 'url':
                    result['url'] = value
                elif key_lower == 'method':
                    result['method'] = value
                else:
                    variables[key] = value
            continue

        # Parse HTTP method line (only before body)
        m = re.match(r'^(POST|GET|PUT|DELETE|PATCH)\s+(.+)$', line, re.IGNORECASE)
        if m and not in_body:
            result['method'] = m.group(1).upper()
            url = m.group(2).strip()
            # Handle @url reference
            if url.startswith('@'):
                ref = url[1:].strip()
                resolved = variables.get(ref) or result.get('url')
                if resolved:
                    result['url'] = resolved
            else:
                result['url'] = url
            continue

        # Parse X5-Method header (only before body) — overwrites method from POST line
        if line.lower().startswith('x5-method:') and not in_body:
            method_value = line.split(':', 2)[1]
            if method_value:
                result['method'] = method_value.strip()
            continue

        # Parse custom headers (not X5-Method, not HTTP method line)
        if not in_body and ':' in line:
            if not line.lower().startswith('x5-method:') and not re.match(r'^(POST|GET|PUT|DELETE|PATCH)\s+', line, re.IGNORECASE):
                hm = re.match(r'^([^:]+):\s*(.+)$', line)
                if hm:
                    headers[hm.group(1).strip()] = hm.group(2).strip()
            continue

        # Skip empty lines before body
        if not in_body and not line:
            continue

        # Collect body content (preserve original indentation for JSON parsing)
        if in_body:
            body_lines.append(lines[i])

    if headers:
        result['headers'] = headers

    # Parse JSON body
    body_str = '\n'.join(body_lines)
    if body_str:
        try:
            result['body'] = json.loads(body_str)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from the content
            jm = re.search(r'\{[\s\S]*\}', content)
            if jm:
                try:
                    result['body'] = json.loads(jm.group(0))
                except json.JSONDecodeError:
                    result['body'] = {}
            else:
                result['body'] = {}

    # Validate required fields
    if not all(k in result for k in ('appid', 'appkey', 'url', 'method')):
        return None
    if 'body' not in result:
        result['body'] = {}

    return result


def _remove_quotes(value: str) -> str:
    """Remove surrounding quotes from a value."""
    if len(value) >= 2 and ((value[0] == '"' and value[-1] == '"') or
                             (value[0] == "'" and value[-1] == "'")):
        return value[1:-1]
    return value


# ─── Signature Generation ──────────────────────────────────────────────────────

def generate_signature(appid: str, body_obj: dict, appkey: str) -> str:
    """Generate X5 protocol signature: md5(appid + JSON.stringify(body) + appkey).toUpperCase()"""
    body_json = json.dumps(body_obj, separators=COMPACT_SEPARATORS, ensure_ascii=False)
    payload = appid + body_json + appkey
    return hashlib.md5(payload.encode('utf-8')).hexdigest().upper()


# ─── Request Encoding ──────────────────────────────────────────────────────────

def encode_request(appid: str, body_obj: dict, method: str, appkey: str) -> tuple[str, dict]:
    """Build X5 envelope, JSON-serialize, and Base64 encode.

    Returns (base64_string, envelope_dict).
    """
    sign = generate_signature(appid, body_obj, appkey)
    body_json = json.dumps(body_obj, separators=COMPACT_SEPARATORS, ensure_ascii=False)

    envelope = {
        "header": {
            "appid": appid,
            "sign": sign,
            "method": method
        },
        "body": body_json
    }

    envelope_json = json.dumps(envelope, separators=COMPACT_SEPARATORS, ensure_ascii=False)
    b64 = base64.b64encode(envelope_json.encode('utf-8')).decode('utf-8')
    return b64, envelope


def build_form_data(base64_str: str) -> str:
    """Build URL-encoded form data: data=<base64>"""
    return f"data={urllib.parse.quote(base64_str, safe='')}"


# ─── HTTP Request ──────────────────────────────────────────────────────────────

def send_request(url: str, form_data: str, custom_headers: dict[str, str],
                 timeout: int = 30000) -> dict:
    """Send X5 POST request and return response dict."""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        **custom_headers
    }

    req = urllib.request.Request(url, data=form_data.encode('utf-8'), headers=headers, method='POST')
    start = time.time()

    try:
        with urllib.request.urlopen(req, timeout=timeout / 1000) as resp:
            duration_ms = int((time.time() - start) * 1000)
            status = resp.status
            status_text = resp.reason or 'OK'
            resp_headers = dict(resp.headers)
            raw_body = resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        duration_ms = int((time.time() - start) * 1000)
        status = e.code
        status_text = str(e.reason) if e.reason else 'Error'
        resp_headers = dict(e.headers) if e.headers else {}
        raw_body = e.read().decode('utf-8', errors='replace')
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection failed: {e.reason}") from e
    except Exception as e:
        if 'timed out' in str(e).lower():
            raise RuntimeError(f"Request timeout after {timeout}ms") from e
        raise

    # Decode response body
    decoded_body = decode_response(raw_body, resp_headers.get('Content-Type', ''))

    return {
        'status': status,
        'status_text': status_text,
        'duration_ms': duration_ms,
        'timestamp': int(time.time() * 1000),
        'headers': resp_headers,
        'body': decoded_body
    }


def decode_response(raw_body: str, content_type: str) -> dict | str:
    """Decode response: try X5 Base64, then JSON, then raw text."""
    if not raw_body:
        return {}

    # If content-type is JSON, parse directly
    if 'application/json' in content_type:
        try:
            return json.loads(raw_body)
        except json.JSONDecodeError:
            return raw_body

    # If content-type is text, return as-is
    if 'text/' in content_type:
        return raw_body

    # Try X5 Base64 decode
    try:
        decoded_b64 = base64.b64decode(raw_body).decode('utf-8')
        parsed = json.loads(decoded_b64)
        # Try to parse X5 envelope body field
        if isinstance(parsed, dict) and 'body' in parsed:
            if isinstance(parsed['body'], str):
                try:
                    parsed['body'] = json.loads(parsed['body'])
                except json.JSONDecodeError:
                    pass
        return parsed
    except Exception:
        pass

    # Fallback: try plain JSON
    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        return raw_body


# ─── cURL Generation ───────────────────────────────────────────────────────────

def generate_curl(url: str, form_data: str, custom_headers: dict[str, str]) -> str:
    """Generate an equivalent cURL command."""
    parts = [f"curl -X POST '{url}'"]
    parts.append("  -H 'Content-Type: application/x-www-form-urlencoded'")
    for key, value in custom_headers.items():
        parts.append(f"  -H '{key}: {value}'")
    parts.append(f"  --data-raw '{form_data}'")
    return ' \\\n'.join(parts)


# ─── Output Formatting ─────────────────────────────────────────────────────────

def format_output(result: dict, json_mode: bool) -> str:
    """Format the result for display."""
    if json_mode:
        return json.dumps(result, indent=2, ensure_ascii=False)

    if 'error' in result:
        return f"Error: {result['error']}"
    if result.get('mode') == 'list':
        return _format_request_list(result['requests'])
    if result.get('mode') == 'curl':
        return result['curl_command']
    if result.get('mode') == 'dry_run':
        return _format_dry_run(result)
    return _format_response(result)


def _format_request_list(requests: list[dict]) -> str:
    """Format a list of requests for display."""
    lines = [f"Found {len(requests)} request(s):\n"]
    for i, req in enumerate(requests, 1):
        name = req.get('name', '(unnamed)')
        method = req.get('method', '?')
        url = req.get('url', '?')
        lines.append(f"  {i}. {name}")
        lines.append(f"     Method: {method}")
        lines.append(f"     URL: {url}")
        if req.get('headers'):
            for k, v in req['headers'].items():
                lines.append(f"     Header: {k}: {v}")
        lines.append('')
    return '\n'.join(lines)


def _format_dry_run(result: dict) -> str:
    """Format dry-run output."""
    req = result['request']
    lines = [
        "=== X5 Request (Dry Run) ===",
        f"Name:    {req.get('name', '(unnamed)')}",
        f"Method:  {req.get('method')}",
        f"URL:     {req.get('url')}",
        f"AppID:   {req.get('appid')}",
    ]
    if req.get('headers'):
        lines.append("Headers:")
        for k, v in req['headers'].items():
            lines.append(f"  {k}: {v}")
    lines.append(f"Body:    {json.dumps(req.get('body', {}), ensure_ascii=False)}")
    lines.append("")
    lines.append("=== Encoded ===")
    lines.append(f"Signature: {result['signature']}")
    lines.append(f"Base64:    {result['base64'][:80]}...")
    lines.append(f"Form Data: data={result['base64'][:80]}...")
    return '\n'.join(lines)


def _format_response(result: dict) -> str:
    """Format a response for display."""
    req = result.get('request', {})
    resp = result.get('response', {})
    lines = [
        "=== X5 Response ===",
        f"Status:   {resp.get('status')} {resp.get('status_text', '')}",
        f"Duration: {resp.get('duration_ms', 0)}ms",
        f"Request:  {req.get('method')} {req.get('url')}",
    ]
    body = resp.get('body')
    if isinstance(body, dict):
        lines.append(f"Body:\n{json.dumps(body, indent=2, ensure_ascii=False)}")
    elif isinstance(body, str):
        lines.append(f"Body:\n{body}")
    return '\n'.join(lines)


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='X5 Protocol Client - Send X5 API requests from the terminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Send from .x5 file:     python3 x5_client.py --file request.x5 --json
  Inline request:         python3 x5_client.py --appid X --appkey Y --url Z --method M --body '{"k":"v"}'
  Generate cURL:          python3 x5_client.py --file request.x5 --curl
  List requests:          python3 x5_client.py --file request.x5 --list
  Dry run (debug):        python3 x5_client.py --file request.x5 --dry-run --json
""")
    parser.add_argument('--file', help='Path to .x5 file')
    parser.add_argument('--request-name', help='Specific request name to send (for multi-request files)')
    parser.add_argument('--list', action='store_true', help='List all requests in .x5 file')
    parser.add_argument('--appid', help='App ID')
    parser.add_argument('--appkey', help='App Key')
    parser.add_argument('--url', help='Target URL')
    parser.add_argument('--method', help='X5 method name')
    parser.add_argument('--body', help='JSON body string')
    parser.add_argument('--body-file', help='JSON body file path (alternative to --body)')
    parser.add_argument('--header', action='append', default=[], help='Custom header KEY=VALUE (repeatable)')
    parser.add_argument('--curl', action='store_true', help='Generate cURL command (no HTTP call)')
    parser.add_argument('--dry-run', action='store_true', help='Show encoded request without sending')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--timeout', type=int, default=30000, help='Timeout in ms (default: 30000)')

    args = parser.parse_args()

    # Parse custom headers
    custom_headers: dict[str, str] = {}
    for h in args.header:
        if '=' in h:
            key, value = h.split('=', 1)
            custom_headers[key.strip()] = value.strip()
        else:
            _error(f"Invalid header format: '{h}'. Use KEY=VALUE", json_mode=args.json, exit_code=2)

    # ─── File mode ─────────────────────────────────────────────────────────
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            _error(f"File not found: {args.file}", json_mode=args.json)

        content = file_path.read_text(encoding='utf-8')
        requests = parse_x5_file(content)

        if not requests:
            _error(f"No valid requests found in {args.file}", json_mode=args.json)

        # List mode
        if args.list:
            result = {'mode': 'list', 'requests': requests}
            print(format_output(result, args.json))
            return

        # Select request
        if args.request_name:
            matched = [r for r in requests if r.get('name') == args.request_name]
            if not matched:
                names = [r.get('name', '(unnamed)') for r in requests]
                _error(f"Request '{args.request_name}' not found. Available: {names}", json_mode=args.json)
            req = matched[0]
        elif len(requests) == 1:
            req = requests[0]
        else:
            names = [r.get('name', '(unnamed)') for r in requests]
            _error(f"Multiple requests found. Use --request-name to select one.\n"
                   f"Available: {names}", json_mode=args.json)

        # Override with CLI params if provided
        if args.appid:
            req['appid'] = args.appid
        if args.appkey:
            req['appkey'] = args.appkey
        if args.url:
            req['url'] = args.url
        if args.method:
            req['method'] = args.method
        if args.body:
            try:
                req['body'] = json.loads(args.body)
            except json.JSONDecodeError:
                _error(f"Invalid JSON body: {args.body}", json_mode=args.json)
        if args.body_file:
            try:
                req['body'] = json.loads(Path(args.body_file).read_text(encoding='utf-8'))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                _error(f"Failed to read body file: {e}", json_mode=args.json)
        if custom_headers:
            req.setdefault('headers', {}).update(custom_headers)

    # ─── Inline mode ───────────────────────────────────────────────────────
    else:
        missing = []
        if not args.appid:
            missing.append('--appid')
        if not args.appkey:
            missing.append('--appkey')
        if not args.url:
            missing.append('--url')
        if not args.method:
            missing.append('--method')
        if missing:
            _error(f"Missing required arguments: {', '.join(missing)}", json_mode=args.json, exit_code=2)

        body = {}
        if args.body:
            try:
                body = json.loads(args.body)
            except json.JSONDecodeError:
                _error(f"Invalid JSON body: {args.body}", json_mode=args.json)
        elif args.body_file:
            try:
                body = json.loads(Path(args.body_file).read_text(encoding='utf-8'))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                _error(f"Failed to read body file: {e}", json_mode=args.json)

        req = {
            'appid': args.appid,
            'appkey': args.appkey,
            'url': args.url,
            'method': args.method,
            'body': body,
        }
        if custom_headers:
            req['headers'] = custom_headers

    # ─── Encode request ────────────────────────────────────────────────────
    b64, envelope = encode_request(req['appid'], req['body'], req['method'], req['appkey'])
    form_data = build_form_data(b64)
    headers = req.get('headers', {})

    # cURL mode
    if args.curl:
        curl_cmd = generate_curl(req['url'], form_data, headers)
        result = {'mode': 'curl', 'curl_command': curl_cmd, 'request': _safe_request(req)}
        print(format_output(result, args.json))
        return

    # Dry-run mode
    if args.dry_run:
        result = {
            'mode': 'dry_run',
            'request': _safe_request(req),
            'signature': envelope['header']['sign'],
            'base64': b64,
            'envelope': envelope,
            'form_data': form_data,
        }
        print(format_output(result, args.json))
        return

    # ─── Send request ──────────────────────────────────────────────────────
    try:
        response = send_request(req['url'], form_data, headers, args.timeout)
    except RuntimeError as e:
        _error(str(e), json_mode=args.json)

    result = {
        'success': True,
        'request': _safe_request(req),
        'response': response,
    }
    print(format_output(result, args.json))


def _safe_request(req: dict) -> dict:
    """Return request dict with body for output (body is always included)."""
    return {
        'name': req.get('name'),
        'method': req.get('method'),
        'url': req.get('url'),
        'body': req.get('body', {}),
    }


def _error(message: str, json_mode: bool = False, exit_code: int = 1):
    """Print error and exit."""
    if json_mode:
        print(json.dumps({'success': False, 'error': message}, ensure_ascii=False))
    else:
        print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
