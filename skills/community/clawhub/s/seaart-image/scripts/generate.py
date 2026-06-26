# SECURITY MANIFEST:
# Environment variables accessed: SEAART_TOKEN
# External endpoints called:
#   - https://www.seaart.ai/api/v1/task/v2/text-to-img (POST)
#   - https://www.seaart.ai/api/v1/task/batch-progress (POST)
# Local files read: none
# Local files written: none

import argparse
import math
import requests
import time
import sys
import json
import os
from urllib.parse import urlparse, parse_qs

# hd=True means the model requires >= 3,686,400 pixels (e.g. 1920x1920)
# hd=False means the model works best at ~1MP (e.g. 1024x1024, SD/Pony class)
MODELS = {
    # --- SeaArt Official ---
    "seaart-infinity": {
        "model_no": "f8172af6747ec762bcf847bd60fdf7cd",
        "model_ver_no": "2c39fe1f-f5d6-4b50-a273-499677f2f7a9",
        "name": "SeaArt Infinity",
        "hd": True
    },
    "seaart-film": {
        "model_no": "26058e019e3a0c026e1ad2bfa69e2b75",
        "model_ver_no": "91b19145-a436-4bbc-ace4-62399e71336b",
        "name": "SeaArt Film",
        "hd": True
    },
    "seaart-film-edit": {
        "model_no": "a70a84e9d2db46c78661de9bfbbf5bd5",
        "model_ver_no": "1cd2354ece4e4308a1b0896eb35b37bc",
        "name": "SeaArt Film Edit",
        "hd": True
    },
    "seaart-film-edit-2": {
        "model_no": "d4ont25e878c7390gip0",
        "model_ver_no": "d39166c9-4d77-4fa3-a81f-d69f144929f0",
        "name": "SeaArt Film Edit 2.0",
        "hd": True
    },
    "seaart-film-edit-3": {
        "model_no": "d6eqg15e878c73dilcv0",
        "model_ver_no": "a8b3e33e-02b5-4a27-bca8-c331c87b267f",
        "name": "SeaArt Film Edit 3.0",
        "hd": True
    },
    # --- Seedream Series ---
    "seedream-5": {
        "model_no": "d6eqbble878c73dhco9g",
        "model_ver_no": "1ad9c231-1945-4e50-a24d-d2c7570338ad",
        "name": "Seedream 5.0",
        "hd": True
    },
    "seedream-4.5": {
        "model_no": "d4pbgg5e878c73fengf0",
        "model_ver_no": "53c0eaf0-7de3-4e9c-a906-9499df061661",
        "name": "Seedream 4.5",
        "hd": True
    },
    "seedream-4": {
        "model_no": "d534afde878c73drik20",
        "model_ver_no": "60099fa2-8f31-4f42-8e7f-5ea4c2784220",
        "name": "Seedream 4.0",
        "hd": True
    },
    # --- Nano Banana Series ---
    "nano-banana": {
        "model_no": "0e21cbf906b5b39c2f9863f4b9ff059edbd0b399",
        "model_ver_no": "e651aa45c8ed746bcd2546d46a3cdf3bf83feb67",
        "name": "Nano Banana",
        "hd": True
    },
    "nano-banana-2": {
        "model_no": "d6ggttle878c739bpf50",
        "model_ver_no": "547ebf19-577f-4614-9ef7-f9ece0aebf80",
        "name": "Nano Banana 2",
        "hd": True
    },
    "nano-banana-pro": {
        "model_no": "d49btu5e878c73avuqfg",
        "model_ver_no": "49a838b1-0ef7-4442-999d-71e10cb2feab",
        "name": "Nano Banana Pro Image",
        "hd": True
    },
    # --- Other ---
    "z-image-turbo": {
        "model_no": "d4kssode878c7387fae0",
        "model_ver_no": "ef24b47a8d618127c9342fd0635aedb9",
        "name": "Z Image Turbo",
        "hd": True
    },
    "wai-ani-ponyxl": {
        "model_no": "24231feb2db47b663ff5b3123f01fab6",
        "model_ver_no": "6e2e976db9a8e83312a0c91b852f876c",
        "name": "WAI-ANI-PONYXL",
        "hd": False
    },
    "grok-imagine": {
        "model_no": "d6sih8le878c73a7cbtg",
        "model_ver_no": "0e7eaf79-5702-4387-bcaa-ce3b79a36889",
        "name": "Grok Imagine Image",
        "hd": True
    },
}

# Standard resolution (~1MP, for SD/Pony models)
ASPECT_RATIOS_SD = {
    "1:1":   {"width": 1024, "height": 1024},
    "2:3":   {"width": 832,  "height": 1216},
    "3:2":   {"width": 1216, "height": 832},
    "3:4":   {"width": 896,  "height": 1152},
    "4:3":   {"width": 1152, "height": 896},
    "9:16":  {"width": 768,  "height": 1344},
    "16:9":  {"width": 1344, "height": 768},
}

# HD resolution (~4MP, for SeaArt/Seedream/new-gen models, all >= 3,686,400 px)
ASPECT_RATIOS_HD = {
    "1:1":   {"width": 2048, "height": 2048},
    "2:3":   {"width": 1664, "height": 2432},
    "3:2":   {"width": 2432, "height": 1664},
    "3:4":   {"width": 1792, "height": 2304},
    "4:3":   {"width": 2304, "height": 1792},
    "9:16":  {"width": 1536, "height": 2688},
    "16:9":  {"width": 2688, "height": 1536},
}

HD_MIN_PIXELS = 3_686_400


def ensure_min_pixels(width, height, min_pixels):
    """Scale up dimensions proportionally if below minimum pixel count."""
    current = width * height
    if current >= min_pixels:
        return width, height
    scale = math.sqrt(min_pixels / current)
    new_w = int(math.ceil(width * scale / 64) * 64)
    new_h = int(math.ceil(height * scale / 64) * 64)
    return new_w, new_h


def is_hd_model(model_key=None, model_no=None):
    """Check if a model requires HD resolution."""
    if model_key and model_key in MODELS:
        return MODELS[model_key].get("hd", True)
    # For custom models (via --model-no or --model-url), assume HD by default
    return True


class SeaArtAPI:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()

        self.session.headers.update({
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en',
            'content-type': 'application/json',
            'origin': 'https://www.seaart.ai',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-app-id': 'web_global_seaart',
            'x-platform': 'web',
            'x-project-id': 'seaart'
        })

        self.session.cookies.set('T', self.token, domain='.seaart.ai')
        self.session.cookies.set('lang', 'en', domain='.seaart.ai')

    def generate_image(self, prompt, model_no, model_ver_no, width, height,
                       n_iter=4, negative="", steps=None, loras=None):
        url = 'https://www.seaart.ai/api/v1/task/v2/text-to-img'

        lora_models = []
        if loras:
            for lora in loras:
                entry = {"id": lora["id"], "strength": lora["strength"]}
                if lora.get("model_ver_no"):
                    entry["model_no"] = lora["id"]
                    entry["model_ver_no"] = lora["model_ver_no"]
                lora_models.append(entry)

        meta = {
            "prompt": prompt,
            "network_remix_local_prompt": prompt,
            "cfa_scale": 7,
            "clip_skip": 2,
            "embeddings": [],
            "generate": {
                "anime_enhance": 0,
                "mode": 0,
                "gen_mode": 1,
                "prompt_magic_mode": 2
            },
            "height": height,
            "width": width,
            "lab_base": {"conds": []},
            "lora_models": lora_models,
            "n_iter": n_iter,
            "negative_prompt": negative,
            "restore_faces": False,
            "sampler_name": "DPM++ 2M Karras",
            "vae": "None"
        }

        if steps is not None:
            meta["steps"] = steps

        payload = {
            "model_no": model_no,
            "model_ver_no": model_ver_no,
            "meta": meta,
            "speed_type": 2
        }

        print(f"Submitting image generation task...", file=sys.stderr)
        print(f"  Prompt: {prompt}", file=sys.stderr)
        print(f"  Size: {width}x{height} ({width*height:,} px), Count: {n_iter}", file=sys.stderr)

        response = self.session.post(url, json=payload, timeout=30)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
            raise Exception("Failed to submit task")

        data = response.json()
        status_code = data.get('status', {}).get('code') or data.get('code')
        if status_code != 10000:
            msg = data.get('status', {}).get('msg', 'Unknown error')
            print(f"API Error ({status_code}): {msg}", file=sys.stderr)
            print(f"Full response: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
            raise Exception(f"API returned error code {status_code}: {msg}")

        task_id = data.get('data', {}).get('id')
        if not task_id:
            raise Exception("Task ID not found in response")

        print(f"Task submitted! ID: {task_id}", file=sys.stderr)
        return task_id

    def poll_progress(self, task_id, max_wait_seconds=300):
        url = 'https://www.seaart.ai/api/v1/task/batch-progress'
        payload = {"task_ids": [task_id]}

        start_time = time.time()
        print(f"Polling for completion (timeout: {max_wait_seconds}s)...", file=sys.stderr)

        while True:
            if time.time() - start_time > max_wait_seconds:
                raise TimeoutError(f"Task timed out after {max_wait_seconds}s. Task ID: {task_id}")

            try:
                response = self.session.post(url, json=payload, timeout=10)
            except requests.exceptions.RequestException as e:
                print(f"Network error during polling: {e}", file=sys.stderr)
                time.sleep(5)
                continue

            if response.status_code == 200:
                data = response.json()
                status_code = data.get('status', {}).get('code') or data.get('code')
                if status_code == 10000:
                    items = data.get('data', {}).get('items', [])
                    task_info = next((i for i in items if i.get('task_id') == task_id), None)
                    if task_info:
                        status = task_info.get('status')
                        progress = task_info.get('process', 0)
                        rest_time = task_info.get('rest_estimate_time', 0)

                        filled = int(progress / 5)
                        bar = '█' * filled + '░' * (20 - filled)
                        print(f"\r[{bar}] {progress}% (est. {rest_time}s remaining)", end='', file=sys.stderr)

                        if status == 3:  # complete
                            print('', file=sys.stderr)
                            return self._extract_results(task_info)

                        if status == 4:  # failed
                            print('', file=sys.stderr)
                            reason = task_info.get('fail_reason', 'Unknown')
                            raise Exception(f"Generation failed: {reason}")

                        if status == 5:  # cancelled
                            print('', file=sys.stderr)
                            reason = task_info.get('fail_reason', 'Unknown')
                            raise Exception(f"Task cancelled: {reason}")

            time.sleep(5)

    def _extract_results(self, task_info):
        results = {
            "urls": [],
            "coin_cost": task_info.get('coin_cost', 0),
            "stamina_cost": task_info.get('stamina_cost', 0),
            "n_iter": task_info.get('n_iter', 0),
        }

        img_uris = task_info.get('img_uris') or []
        for item in img_uris:
            if isinstance(item, dict):
                url = item.get('url', '')
            else:
                url = str(item)
            if url and not url.startswith('http'):
                url = f"https://image.cdn2.seaart.me/{url}"
            if url:
                results["urls"].append(url)

        return results


def parse_loras(lora_str):
    """Parse LoRA string: 'id:strength:ver,id2:strength2:ver2'"""
    if not lora_str:
        return []
    loras = []
    for part in lora_str.split(','):
        fields = part.strip().split(':')
        if len(fields) < 2:
            raise ValueError(f"Invalid LoRA format: {part}. Expected id:strength[:version]")
        entry = {
            "id": fields[0],
            "strength": float(fields[1]),
        }
        if len(fields) >= 3 and fields[2]:
            entry["model_ver_no"] = fields[2]
        loras.append(entry)
    return loras


def parse_model_url(url_str):
    """Extract model_no and model_ver_no from a SeaArt model page URL."""
    parsed = urlparse(url_str)
    params = parse_qs(parsed.query)
    model_no = params.get('id', [''])[0]
    model_ver = params.get('model_ver_no', [''])[0]
    if not model_no or not model_ver:
        raise ValueError(f"Cannot extract model params from URL: {url_str}")
    return model_no, model_ver


def main():
    all_ratios = list(ASPECT_RATIOS_SD.keys())

    parser = argparse.ArgumentParser(description="Generate SeaArt Images")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--model", default=None, choices=list(MODELS.keys()),
                        help="Predefined model name")
    parser.add_argument("--model-no", default=None, help="Custom model number")
    parser.add_argument("--model-ver", default=None, help="Custom model version")
    parser.add_argument("--model-url", default=None, help="SeaArt model page URL")
    parser.add_argument("--aspect-ratio", default=None, choices=all_ratios,
                        help="Aspect ratio (overrides width/height)")
    parser.add_argument("--width", type=int, default=None, help="Image width")
    parser.add_argument("--height", type=int, default=None, help="Image height")
    parser.add_argument("--n", type=int, default=4, help="Number of images (1-8)")
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--steps", type=int, default=None, help="Generation steps (model-dependent)")
    parser.add_argument("--lora", default=None, help="LoRA models (format: id:strength:ver,id2:strength2:ver2)")

    args = parser.parse_args()

    token = os.environ.get("SEAART_TOKEN")
    if not token:
        print("Error: SEAART_TOKEN environment variable not set.", file=sys.stderr)
        print('Run: /update-config set SEAART_TOKEN="your_t_cookie_value"', file=sys.stderr)
        sys.exit(1)

    # Resolve model
    model_key = None
    model_no = None
    model_ver = None

    if args.model_url:
        model_no, model_ver = parse_model_url(args.model_url)
    elif args.model_no and args.model_ver:
        model_no = args.model_no
        model_ver = args.model_ver
    elif args.model:
        model_key = args.model
        info = MODELS[model_key]
        model_no = info["model_no"]
        model_ver = info["model_ver_no"]
    else:
        env_no = os.environ.get("SEAART_DEFAULT_MODEL_NO")
        env_ver = os.environ.get("SEAART_DEFAULT_MODEL_VER")
        if env_no and env_ver:
            model_no = env_no
            model_ver = env_ver
        else:
            model_key = "seaart-infinity"
            default = MODELS[model_key]
            model_no = default["model_no"]
            model_ver = default["model_ver_no"]
            print(f"Using default model: {default['name']}", file=sys.stderr)

    hd = is_hd_model(model_key=model_key, model_no=model_no)
    ratio_table = ASPECT_RATIOS_HD if hd else ASPECT_RATIOS_SD

    # Resolve dimensions
    if args.aspect_ratio:
        ar = ratio_table[args.aspect_ratio]
        width = ar["width"]
        height = ar["height"]
    elif args.width and args.height:
        width = args.width
        height = args.height
    else:
        default_ar = ratio_table["1:1"]
        width = default_ar["width"]
        height = default_ar["height"]

    # Safety: ensure HD models meet minimum pixel requirement
    if hd:
        old_w, old_h = width, height
        width, height = ensure_min_pixels(width, height, HD_MIN_PIXELS)
        if (old_w, old_h) != (width, height):
            print(f"  Auto-scaled {old_w}x{old_h} -> {width}x{height} (HD model requires >= {HD_MIN_PIXELS:,} px)", file=sys.stderr)

    # Clamp n_iter
    n_iter = max(1, min(8, args.n))

    # Parse LoRAs
    loras = parse_loras(args.lora) if args.lora else None

    api = SeaArtAPI(token)

    try:
        task_id = api.generate_image(
            prompt=args.prompt,
            model_no=model_no,
            model_ver_no=model_ver,
            width=width,
            height=height,
            n_iter=n_iter,
            negative=args.negative,
            steps=args.steps,
            loras=loras
        )

        print("Waiting for generation...", file=sys.stderr)
        results = api.poll_progress(task_id)

        # Output structured result to stdout
        print("\n=== Generation Complete ===")

        if results["stamina_cost"]:
            print(f"Stamina cost: {results['stamina_cost']}")
        if results["coin_cost"]:
            print(f"Coin cost: {results['coin_cost']}")

        total = results["n_iter"]
        actual = len(results["urls"])

        if actual < total and actual > 0:
            print(f"Warning: {total - actual} of {total} images filtered by content review")

        if not results["urls"]:
            print("All images were filtered by content review.")
            print("Suggestion: adjust prompt to avoid sensitive content, or add negative prompt.")
            sys.exit(1)

        print(f"Images ({actual}):")
        for url in results["urls"]:
            print(f"  {url}")

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
