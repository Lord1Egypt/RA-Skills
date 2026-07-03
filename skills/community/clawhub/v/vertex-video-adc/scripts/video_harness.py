#!/usr/bin/env python3
"""
Robust test harness for Vertex predictLongRunning (Veo) using ADC or user token.
Supports text-to-video and image-to-video.
"""
import argparse
import subprocess
import json
import base64
import sys
import time
import os
import tempfile
from typing import Any


def get_token(auth_mode):
    if auth_mode == 'adc':
        cmd = ['gcloud', 'auth', 'application-default', 'print-access-token']
    else:
        cmd = ['gcloud', 'auth', 'print-access-token']
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(json.dumps({
            "ok": False,
            "error": "Failed to get auth token via gcloud. Ensure gcloud is installed and authenticated.",
            "debug": proc.stderr.strip()
        }))
        sys.exit(2)
    return proc.stdout.strip()


def curl_json_post(url, token, json_path=None, json_body=None):
    cmd = ['curl', '-sS', '-X', 'POST', '-H', f'Authorization: Bearer {token}', '-H', 'Content-Type: application/json; charset=utf-8']
    if json_path:
        cmd += ['--data-binary', f'@{json_path}', url]
    else:
        cmd += ['-d', json.dumps(json_body), url]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def find_base64_strings(obj, max_samples=100):
    samples = []
    def _walk(o):
        if isinstance(o, dict):
            for k,v in o.items():
                if isinstance(v, str) and len(v) > 100 and all(ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n' for ch in v[:100]):
                    samples.append(v)
                else:
                    _walk(v)
        elif isinstance(o, list):
            for it in o:
                _walk(it)
    _walk(obj)
    return samples[:max_samples]


def extract_and_write_videos(final_json, out_path=None):
    b64s = []
    try:
        vids = final_json.get('response', {}).get('videos', [])
        for v in vids:
            b = v.get('bytesBase64Encoded') or v.get('bytes') or v.get('data')
            if isinstance(b, str) and len(b) > 100:
                b64s.append(b)
    except Exception:
        pass
        
    if not b64s:
        b64s = find_base64_strings(final_json)
        
    if not b64s:
        return []

    saved_paths = []
    if out_path:
        base, ext = os.path.splitext(out_path)
        if not ext:
            ext = '.mp4'
    else:
        temp_dir = tempfile.gettempdir()
        base = os.path.join(temp_dir, 'vertex_video')
        ext = '.mp4'

    for i, b in enumerate(b64s):
        try:
            data = base64.b64decode(b)
            if len(b64s) == 1 and out_path:
                current_out = out_path
            else:
                current_out = f"{base}_{i}{ext}"
                
            out_parent = os.path.dirname(os.path.abspath(current_out))
            if out_parent:
                os.makedirs(out_parent, exist_ok=True)
                
            with open(current_out, 'wb') as f:
                f.write(data)
            saved_paths.append(current_out)
        except Exception:
            pass
            
    return saved_paths


def main():
    p = argparse.ArgumentParser(description="Vertex AI Veo Video Generation")
    p.add_argument('--image', required=False, help='Path to reference image (optional)')
    p.add_argument('--prompt-file', required=False, help='File containing prompt text')
    p.add_argument('--prompt', required=False, help='Prompt string (alternative to --prompt-file)')
    p.add_argument('--out', required=False, help='Output MP4 path')
    p.add_argument('--project', default=os.environ.get('GOOGLE_CLOUD_PROJECT'), help="GCP Project ID")
    p.add_argument('--location', default=os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1'), help="GCP Location")
    p.add_argument('--model', default=os.environ.get('GOOGLE_CLOUD_MODEL', 'veo-3.1-generate-001'), help="Veo Model ID")
    p.add_argument('--auth-mode', choices=['adc','user-token'], default='adc')
    p.add_argument('--poll-interval', type=float, default=5.0)
    p.add_argument('--timeout', type=float, default=240.0, help='Total seconds to wait')
    p.add_argument('--aspect-ratio', default='16:9', help="Video aspect ratio (e.g. 16:9, 9:16)")
    p.add_argument('--duration', type=int, default=5, help="Video duration in seconds")
    p.add_argument('--resolution', default='720p', help="Video resolution (720p, 1080p)")
    
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')
            
    p.add_argument('--generate-audio', type=str2bool, default=True, help="Whether to generate audio (default: True)")
    args = p.parse_args()

    if not args.project:
        print(json.dumps({
            "ok": False,
            "error": "Google Cloud Project ID is required. Please set --project or specify the GOOGLE_CLOUD_PROJECT environment variable."
        }))
        sys.exit(1)

    if not args.prompt and not args.prompt_file:
        print(json.dumps({
            "ok": False,
            "error": "Either --prompt or --prompt-file must be provided."
        }))
        sys.exit(1)

    if args.prompt_file:
        if not os.path.exists(args.prompt_file):
            print(json.dumps({
                "ok": False,
                "error": f"Prompt file not found: {args.prompt_file}"
            }))
            sys.exit(1)
        with open(args.prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
    else:
        prompt = args.prompt

    # Build the instance dictionary
    instance = {
        'prompt': prompt
    }

    if args.image:
        if not os.path.exists(args.image):
            print(json.dumps({
                "ok": False,
                "error": f"Image file not found: {args.image}"
            }))
            sys.exit(1)
        with open(args.image, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode('ascii')
        instance['image'] = {
            'bytesBase64Encoded': img_b64,
            'mimeType': 'image/jpeg'
        }

    payload = {
        'instances': [instance],
        'parameters': {
            'aspectRatio': args.aspect_ratio,
            'sampleCount': 1,
            'durationSeconds': args.duration,
            'personGeneration': 'allow_all',
            'generateAudio': args.generate_audio,
            'resolution': args.resolution
        }
    }

    # Use cross-platform secure temporary file
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json', encoding='utf-8') as f:
        json.dump(payload, f)
        payload_path = f.name

    token = get_token(args.auth_mode)

    if args.location == 'global':
        endpoint_host = 'aiplatform.googleapis.com'
    else:
        endpoint_host = f'{args.location}-aiplatform.googleapis.com'

    url = f"https://{endpoint_host}/v1/projects/{args.project}/locations/{args.location}/publishers/google/models/{args.model}:predictLongRunning"

    rc, out, err = curl_json_post(url, token, json_path=payload_path)
    
    # Cleanup payload tempfile
    try:
        os.remove(payload_path)
    except Exception:
        pass

    if rc != 0:
        print(json.dumps({"ok": False, "error": "curl predictLongRunning failed", "debug": err}))
        sys.exit(3)

    # Save response for debugging under system temp dir
    temp_dir = tempfile.gettempdir()
    resp_path = os.path.join(temp_dir, 'vertex_video_response.json')
    try:
        with open(resp_path, 'w', encoding='utf-8') as f:
            f.write(out)
    except Exception:
        pass

    try:
        j = json.loads(out)
    except Exception:
        print(json.dumps({"ok": False, "error": "Failed to parse predictLongRunning response as JSON", "debug": out[:1000]}))
        sys.exit(4)

    if 'error' in j:
        print(json.dumps({"ok": False, "error": "API predictLongRunning returned an error", "debug": j['error']}))
        sys.exit(5)

    op_name = j.get('name') or j.get('operation')
    if not op_name:
        print(json.dumps({"ok": False, "error": "No operation name found in predictLongRunning response", "debug": j}))
        sys.exit(5)

    # Poll fetchPredictOperation
    fetch_url = f"https://{endpoint_host}/v1/projects/{args.project}/locations/{args.location}/publishers/google/models/{args.model}:fetchPredictOperation"
    start = time.time()
    interval = args.poll_interval
    attempt = 0
    final_json = None
    while True:
        attempt += 1
        body = { 'operationName': op_name }
        rc, out, err = curl_json_post(fetch_url, token, json_body=body)
        now = time.time()
        
        # Save intermediate poll log to system temp dir
        poll_path = os.path.join(temp_dir, 'vertex_video_operation_poll.json')
        try:
            with open(poll_path, 'w', encoding='utf-8') as f:
                f.write(out)
        except Exception:
            pass

        try:
            pj = json.loads(out)
        except Exception:
            pj = None
            
        if pj and pj.get('done'):
            final_json = pj
            final_path = os.path.join(temp_dir, 'vertex_video_operation_final.json')
            try:
                with open(final_path, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(pj))
            except Exception:
                pass
            break
            
        if now - start > args.timeout:
            print(json.dumps({"ok": False, "error": f"Polling timeout exceeded ({args.timeout}s)."}))
            sys.exit(6)
            
        time.sleep(min(interval * (1 + attempt * 0.1), 10.0))

    if not final_json:
        print(json.dumps({"ok": False, "error": "Polling completed but no final JSON operation structure was obtained."}))
        sys.exit(7)

    # Check error in final response
    if 'error' in final_json:
        print(json.dumps({"ok": False, "error": "LRO completed with error", "debug": final_json['error']}))
        sys.exit(8)

    # Extract video bytes
    try:
        saved_paths = extract_and_write_videos(final_json, args.out)
        if saved_paths:
            print(json.dumps({"ok": True, "paths": saved_paths}))
        else:
            print(json.dumps({"ok": False, "error": "No base64 video artifacts found in final operation response."}))
    except Exception as e:
        print(json.dumps({"ok": False, "error": "Error during video extraction", "debug": str(e)}))


if __name__ == '__main__':
    main()
