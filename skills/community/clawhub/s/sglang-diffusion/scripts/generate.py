#!/usr/bin/env python3
"""
Generate images using a local SGLang-Diffusion server (OpenAI-compatible API).


Usage:
   python3 generate.py --prompt "a futuristic cityscape at sunset"
   python3 generate.py --prompt "portrait" --size 512x512 --steps 30 --seed 42
   python3 generate.py --prompt "abstract art" --negative-prompt "blurry" --server http://host:30000
"""


from __future__ import annotations


import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path




def get_api_key(provided_key: str | None) -> str | None:
   """Get API key from argument first, then environment."""
   if provided_key:
       return provided_key
   return os.environ.get("SGLANG_DIFFUSION_API_KEY")




def generate_output_path(out_arg: str | None, prompt: str) -> Path:
   """Build an output file path: explicit --out wins, otherwise timestamped tmp."""
   if out_arg:
       p = Path(out_arg).expanduser()
       p.parent.mkdir(parents=True, exist_ok=True)
       return p


   now = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
   slug = prompt[:40].lower().strip()
   slug = "".join(c if c.isalnum() or c in ("-", "_") else "-" for c in slug)
   slug = slug.strip("-") or "image"
   tmp = Path("/tmp")
   return tmp / f"sglang-{now}-{slug}.png"




def request_image(
   server: str,
   api_key: str,
   prompt: str,
   *,
   negative_prompt: str = "",
   size: str = "1024x1024",
   steps: int | None = None,
   guidance_scale: float | None = None,
   seed: int | None = None,
) -> dict:
   """POST to /v1/images/generations and return the parsed JSON response."""
   url = f"{server.rstrip('/')}/v1/images/generations"


   body: dict = {
       "prompt": prompt,
       "size": size,
       "n": 1,
       "response_format": "b64_json",
   }
   if negative_prompt:
       body["negative_prompt"] = negative_prompt
   if steps is not None:
       body["num_inference_steps"] = steps
   if guidance_scale is not None:
       body["guidance_scale"] = guidance_scale
   if seed is not None:
       body["seed"] = seed


   data = json.dumps(body).encode("utf-8")
   headers = {"Content-Type": "application/json"}
   if api_key:
       headers["Authorization"] = f"Bearer {api_key}"


   req = urllib.request.Request(url, method="POST", headers=headers, data=data)
   try:
       with urllib.request.urlopen(req, timeout=300) as resp:
           return json.loads(resp.read().decode("utf-8"))
   except urllib.error.HTTPError as e:
       payload = e.read().decode("utf-8", errors="replace")
       raise RuntimeError(
           f"SGLang-Diffusion API failed ({e.code}): {payload}"
       ) from e
   except urllib.error.URLError as e:
       raise RuntimeError(
           f"Cannot reach SGLang-Diffusion server at {server}: {e}"
       ) from e




def main() -> int:
   ap = argparse.ArgumentParser(
       description="Generate images via a local SGLang-Diffusion server."
   )
   ap.add_argument("--prompt", "-p", required=True, help="Image description/prompt.")
   ap.add_argument(
       "--negative-prompt",
       default="",
       help="What to avoid in the image.",
   )
   ap.add_argument("--size", default="1024x1024", help="Image size (default: 1024x1024).")
   ap.add_argument("--steps", type=int, default=None, help="Number of denoising steps.")
   ap.add_argument(
       "--guidance-scale",
       type=float,
       default=None,
       help="Prompt adherence (higher = closer to prompt).",
   )
   ap.add_argument("--seed", type=int, default=None, help="Seed for reproducible generation.")
   ap.add_argument(
       "--server",
       default="http://127.0.0.1:30000",
       help="SGLang-Diffusion server URL (default: http://127.0.0.1:30000).",
   )
   ap.add_argument("--out", "-o", default=None, help="Output file path (default: timestamped /tmp/).")
   ap.add_argument("--api-key", "-k", default=None, help="API key (optional; only needed if server uses --api-key).")
   args = ap.parse_args()


   api_key = get_api_key(args.api_key) or ""


   output_path = generate_output_path(args.out, args.prompt)


   print(f"Generating image: {args.prompt}")
   print(f"Server: {args.server}")
   print(f"Size: {args.size}")


   res = request_image(
       args.server,
       api_key,
       args.prompt,
       negative_prompt=args.negative_prompt,
       size=args.size,
       steps=args.steps,
       guidance_scale=args.guidance_scale,
       seed=args.seed,
   )


   data_list = res.get("data", [])
   if not data_list:
       print("Error: No image data in response.", file=sys.stderr)
       print(f"Response: {json.dumps(res)[:400]}", file=sys.stderr)
       return 1


   b64 = data_list[0].get("b64_json")
   if not b64:
       print("Error: Response missing b64_json field.", file=sys.stderr)
       print(f"Response keys: {list(data_list[0].keys())}", file=sys.stderr)
       return 1


   output_path.write_bytes(base64.b64decode(b64))
   full_path = output_path.resolve()
   print(f"\nImage saved: {full_path}")
   print(f"MEDIA:{full_path}")
   return 0




if __name__ == "__main__":
   raise SystemExit(main())