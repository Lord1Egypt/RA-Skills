#!/usr/bin/env python3
"""Generate images using OpenAI's gpt-image-1 model.

Usage:
    python3 gen_image.py "your prompt here" output.png
    python3 gen_image.py "your prompt here" output.png 1024x1536

Sizes: 1024x1024 (square), 1024x1536 (portrait/IG), 1536x1024 (landscape/Twitter)

Requires OPENAI_API_KEY environment variable.
"""
import sys, os, json, base64, urllib.request

if len(sys.argv) < 3:
    print("Usage: gen_image.py \"prompt\" output.png [size]")
    print("Sizes: 1024x1024, 1024x1536 (portrait), 1536x1024 (landscape)")
    sys.exit(1)

prompt = sys.argv[1]
output = sys.argv[2]
size = sys.argv[3] if len(sys.argv) > 3 else "1024x1536"

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not set")
    print("Set it: export OPENAI_API_KEY='your-key-here'")
    sys.exit(1)

valid_sizes = ["1024x1024", "1024x1536", "1536x1024"]
if size not in valid_sizes:
    print(f"Error: Invalid size '{size}'. Use: {', '.join(valid_sizes)}")
    sys.exit(1)

data = json.dumps({
    "model": "gpt-image-1",
    "prompt": prompt,
    "n": 1,
    "size": size,
    "quality": "high"
}).encode()

req = urllib.request.Request(
    "https://api.openai.com/v1/images/generations",
    data=data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
)

print(f"Generating image ({size})...")
try:
    resp = urllib.request.urlopen(req, timeout=120)
    result = json.loads(resp.read())
    b64 = result["data"][0]["b64_json"]
    with open(output, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"MEDIA:{output}")
    print(f"Saved to {output}")
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    print(f"Error: {e.code} - {error_body}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
