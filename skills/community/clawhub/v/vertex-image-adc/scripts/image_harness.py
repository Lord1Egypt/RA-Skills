#!/usr/bin/env python3
"""
Image harness updated to call Vertex AI generateContent (aiplatform.googleapis.com) with ADC
Usage:
  python3 image_harness.py --prompt-file /path/to/prompt.txt --out /abs/path/out.png --auth-mode adc \
    --project <project_id> --location <location> --model <model>

Behavior:
- Builds payload in the official example shape: {"contents": [{"role": "user", "parts": [{"text": "..."}]}]}
- Posts to the aiplatform generateContent endpoint for the requested project/location/publisher/model
- Tries to locate an image in the JSON response by scanning common fields (imageBytes, bytesBase64Encoded, image, content, data)
- Falls back to imageUri download if present
- Supports GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables
"""
import argparse
import subprocess
import json
import base64
import sys
import os
import re
import tempfile
from typing import Any

BASE64_RE = re.compile(r'^[A-Za-z0-9+/\n\r]+=*$')


# 严格限制执行命令的白名单
ALLOWED_COMMANDS = {
    "gcloud_auth": ["gcloud", "auth"],
    "curl": ["curl", "-sS"],
    "gcloud_predict": ["gcloud", "ai", "endpoints", "predict"]
}

def run_safe_cmd(cmd_key: str, *args: str) -> subprocess.CompletedProcess:
    base_cmd = ALLOWED_COMMANDS.get(cmd_key)
    if not base_cmd:
        raise ValueError(f"Unauthorized command execution requested: {cmd_key}")
    
    # 将参数列表安全传递给 subprocess，禁止 shell=True
    full_cmd = base_cmd + list(args)
    return subprocess.run(full_cmd, capture_output=True, text=True)

def get_token(auth_mode: str) -> str:
    args = ['application-default', 'print-access-token'] if auth_mode == 'adc' else ['print-access-token']
    proc = run_safe_cmd('gcloud_auth', *args)
    if proc.returncode != 0:
        print(json.dumps({
            "ok": False, 
            "error": "Failed to get auth token via gcloud.", 
            "debug": proc.stderr.strip()
        }))
        sys.exit(2)
    return proc.stdout.strip()


def find_base64_strings(obj: Any) -> list:
    """Recursively search obj for strings that look like base64 or data URIs."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                found.extend(find_base64_strings(v))
            elif isinstance(v, str):
                s = v.strip()
                # data URI
                if s.startswith('data:image/'):
                    # format: data:<mime>;base64,xxxxx
                    parts = s.split(',', 1)
                    if len(parts) == 2:
                        found.append((parts[0], parts[1]))
                # heuristic: long base64-like string
                elif len(s) > 200 and BASE64_RE.match(s.replace('\n', '').replace('\r', '')):
                    found.append((None, s))
            # also capture keys often used for image bytes
            elif k.lower() in ('image', 'imagebytes', 'bytesbase64encoded', 'content', 'data') and isinstance(v, (bytes, bytearray)):
                try:
                    b64 = base64.b64encode(v).decode('ascii')
                    found.append((None, b64))
                except Exception:
                    pass
    elif isinstance(obj, list):
        for item in obj:
            found.extend(find_base64_strings(item))
    return found


def download_uri(uri: str, out_path: str, token: str = None) -> bool:
    cmd = ['curl', '-sS', '-L', uri, '-o', out_path]
    if token:
        cmd[1:1] = ['-H', f'Authorization: Bearer {token}']
    proc = subprocess.run(cmd, capture_output=True)
    return proc.returncode == 0


def main():
    p = argparse.ArgumentParser(description="Vertex AI Image Generation Harness")
    p.add_argument('--prompt-file', required=True, help="Path to prompt text file")
    p.add_argument('--out', required=True, help="Path to write the output image")
    p.add_argument('--auth-mode', choices=['adc', 'user-token'], default='adc', help="gcloud auth mode")
    p.add_argument('--project', default=os.environ.get('GOOGLE_CLOUD_PROJECT'), help="Google Cloud Project ID (defaults to GOOGLE_CLOUD_PROJECT environment variable)")
    p.add_argument('--location', default=os.environ.get('GOOGLE_CLOUD_LOCATION', 'global'), help="Google Cloud Location (defaults to GOOGLE_CLOUD_LOCATION environment variable, default: global)")
    p.add_argument('--model', default=os.environ.get('GOOGLE_CLOUD_MODEL', 'gemini-3.1-flash-image-preview'), help="Vertex Model (defaults to GOOGLE_CLOUD_MODEL environment variable, default: gemini-3.1-flash-image-preview)")
    args = p.parse_args()

    if not args.project:
        print(json.dumps({
            "ok": False,
            "error": "Google Cloud Project ID is required. Please set --project or specify the GOOGLE_CLOUD_PROJECT environment variable."
        }))
        sys.exit(1)

    if not os.path.exists(args.prompt_file):
        print(json.dumps({
            "ok": False,
            "error": f"Prompt file not found: {args.prompt_file}"
        }))
        sys.exit(1)

    with open(args.prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read().strip()

    token = get_token(args.auth_mode)

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # Cross-platform secure temp file
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
        payload_path = f.name

    # Build curl command securely using safe executor
    cmd_args = ['-X', 'POST', '-H', f'Authorization: Bearer {token}', '-H', 'Content-Type: application/json; charset=utf-8', '--data-binary', f'@{payload_path}', url]
    proc = run_safe_cmd('curl', *cmd_args)
    
    # Cleanup payload tempfile
    try:
        os.remove(payload_path)
    except Exception:
        pass

    if proc.returncode != 0:
        print(json.dumps({"ok": False, "error": "curl POST request failed", "debug": proc.stderr}))
        sys.exit(3)

    resp_raw = proc.stdout
    
    # Save response for debugging to a unique random file
    # This prevents predictable path injection and ensures isolation
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8', delete=False) as tmp_debug:
            tmp_debug.write(resp_raw)
            # Log the path if needed, or omit to avoid info leakage
    except Exception:
        pass

    try:
        j = json.loads(resp_raw) if resp_raw else {}
    except Exception:
        print(json.dumps({"ok": False, "error": "Invalid response format (not valid JSON)", "debug": resp_raw[:1000]}))
        sys.exit(4)

    # Check for API error
    if 'error' in j:
        print(json.dumps({"ok": False, "error": "API returned an error", "debug": j['error']}))
        sys.exit(5)

    # 1) look for base64/image bytes in the response
    b64_candidates = find_base64_strings(j)

    out_path = args.out

    if b64_candidates:
        hdr, b64 = b64_candidates[0]
        try:
            data = base64.b64decode(b64)
            # Ensure output parent directory exists
            out_parent = os.path.dirname(os.path.abspath(out_path))
            if out_parent:
                os.makedirs(out_parent, exist_ok=True)
            with open(out_path, 'wb') as f:
                f.write(data)

            print(json.dumps({"ok": True, "path": out_path}))
            return
        except Exception as e:
            print(json.dumps({"ok": False, "error": "Failed to decode/write image content", "debug": str(e)}))
            sys.exit(6)

    # 2) look for image URIs
    def find_uris(obj):
        uris = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and (k.lower().endswith('uri') or v.startswith('http')):
                    uris.append(v)
                elif isinstance(v, (dict, list)):
                    uris.extend(find_uris(v))
        elif isinstance(obj, list):
            for item in obj:
                uris.extend(find_uris(item))
        return uris

    uris = find_uris(j)
    if uris:
        tmp_out = out_path + '.tmp'
        ok = download_uri(uris[0], tmp_out, token=token)
        if ok:
            try:
                out_parent = os.path.dirname(os.path.abspath(out_path))
                if out_parent:
                    os.makedirs(out_parent, exist_ok=True)
                os.replace(tmp_out, out_path)
                print(json.dumps({"ok": True, "path": out_path}))
                return
            except Exception as e:
                print(json.dumps({"ok": False, "error": "Failed to replace temporary download path with target output path", "debug": str(e)}))
                sys.exit(6)

    # No usable image found
    print(json.dumps({"ok": False, "error": "No image content or URL found in response", "debug": j}))
    sys.exit(5)


if __name__ == '__main__':
    main()
