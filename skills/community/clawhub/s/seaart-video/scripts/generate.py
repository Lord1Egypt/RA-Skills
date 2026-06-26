# SECURITY MANIFEST:
# Environment variables accessed: SEAART_TOKEN
# External endpoints called:
#   - https://www.seaart.ai/api/v1/task/v2/video/text-to-video (POST)
#   - https://www.seaart.ai/api/v1/task/v2/video/img-to-video (POST)
#   - https://www.seaart.ai/api/v1/task/batch-progress (POST)
# Local files read: none
# Local files written: none

import argparse
import requests
import time
import sys
import json
import os

MODELS = {
    "seaart-sono-cast": {
        "model_no": "d4t763te878c73csvcf0",
        "model_ver_no": "21a5fc20-68dd-4d4b-9afd-7bfe2e8f5166",
        "name": "SeaArt Sono Cast"
    },
    "vidu-q3-turbo": {
        "model_no": "d6l3adte878c73dr6a3g",
        "model_ver_no": "26ca53e1-e6f2-44e4-8227-13e38bb73945",
        "name": "Vidu Q3 Turbo"
    },
    "kling3.0": {
        "model_no": "d62lo1te878c73f8eua0",
        "model_ver_no": "93636e78-3d55-4416-92e3-d7d3b89f023d",
        "name": "Kling 3.0"
    },
    "wan2.6": {
        "model_no": "d4t6pkle878c73cpsif0",
        "model_ver_no": "5856d251-5b8f-4704-970e-e301982eb532",
        "name": "Wan 2.6"
    }
}

ASPECT_RATIOS = {
    "16:9": {"width": 1280, "height": 720},
    "9:16": {"width": 720, "height": 1280},
    "1:1": {"width": 1024, "height": 1024},
    "4:3": {"width": 1024, "height": 768},
    "3:4": {"width": 768, "height": 1024}
}

class SeaArtAPI:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()

        # Base headers derived from curl examples
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

        # We only really need the T cookie for auth based on the curl
        self.session.cookies.set('T', self.token, domain='.seaart.ai')
        self.session.cookies.set('lang', 'en', domain='.seaart.ai')

    def generate_text_to_video(self, prompt, model_key, aspect_ratio):
        url = 'https://www.seaart.ai/api/v1/task/v2/video/text-to-video'

        model_info = MODELS.get(model_key.lower())
        if not model_info:
            raise ValueError(f"Unknown model: {model_key}")

        ar_info = ASPECT_RATIOS.get(aspect_ratio)
        if not ar_info:
            raise ValueError(f"Unknown aspect ratio: {aspect_ratio}")

        payload = {
            "model_no": model_info["model_no"],
            "model_ver_no": model_info["model_ver_no"],
            "meta": {
                "generate": {
                    "gen_mode": 0,
                    "prompt_magic_mode": 2
                },
                "generate_video": {
                    "prompt_magic_mode": 2,
                    "generate_video_duration": 5,
                    "with_audio_to_video": {
                        "audio_uri": "",
                        "audio_name": "",
                        "audio_duration": 0
                    }
                },
                "prompt": prompt,
                "n_iter": 1,
                "task_from": "web",
                "aspect_ratio": aspect_ratio,
                "width": ar_info["width"],
                "height": ar_info["height"],
                "negative_prompt": ""
            },
            "task_domain_type": 11,
            "ss": 52,
            "source": 82001
        }

        print(f"Submitting Text-to-Video task to {model_info['name']}...", file=sys.stderr)
        response = self.session.post(url, json=payload)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
            raise Exception("Failed to submit task")

        data = response.json()
        status_code = data.get('status', {}).get('code') or data.get('code')
        if status_code != 10000:
            print(f"API Error: {json.dumps(data)}", file=sys.stderr)
            raise Exception(f"API returned error code {status_code}")

        task_id = data.get('data', {}).get('id')
        if not task_id:
             raise Exception("Task ID not found in response")

        print(f"Task submitted successfully! Task ID: {task_id}", file=sys.stderr)
        return task_id

    def generate_image_to_video(self, prompt, image_url, model_key):
        url = 'https://www.seaart.ai/api/v1/task/v2/video/img-to-video'

        model_info = MODELS.get(model_key.lower())
        if not model_info:
            raise ValueError(f"Unknown model: {model_key}")

        payload = {
            "model_no": model_info["model_no"],
            "model_ver_no": model_info["model_ver_no"],
            "meta": {
                "generate": {
                    "gen_mode": 0,
                    "prompt_magic_mode": 2
                },
                "generate_video": {
                    "prompt_magic_mode": 2,
                    "generate_video_duration": 5,
                    "with_audio_to_video": {
                        "audio_uri": "",
                        "audio_name": "",
                        "audio_duration": 0
                    },
                    "image_opts": [
                        {
                            "mode": "first_frame",
                            "url": image_url
                        }
                    ]
                },
                "prompt": prompt,
                "n_iter": 1,
                "task_from": "web",
                "negative_prompt": ""
            },
            "task_domain_type": 12,
            "ss": 52
        }

        print(f"Submitting Image-to-Video task to {model_info['name']}...", file=sys.stderr)
        response = self.session.post(url, json=payload)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
            raise Exception("Failed to submit task")

        data = response.json()
        status_code = data.get('status', {}).get('code') or data.get('code')
        if status_code != 10000:
            print(f"API Error: {json.dumps(data)}", file=sys.stderr)
            raise Exception(f"API returned error code {status_code}")

        task_id = data.get('data', {}).get('id')
        if not task_id:
             raise Exception("Task ID not found in response")

        print(f"Task submitted successfully! Task ID: {task_id}", file=sys.stderr)
        return task_id

    def poll_progress(self, task_id, max_wait_seconds=600):
        url = 'https://www.seaart.ai/api/v1/task/batch-progress'
        payload = {
            "task_ids": [task_id],
            "ss": 52
        }

        start_time = time.time()
        print(f"Polling for completion (timeout in {max_wait_seconds}s)...", file=sys.stderr)

        while True:
            if time.time() - start_time > max_wait_seconds:
                raise TimeoutError("Task timed out while waiting for completion")

            response = self.session.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                status_code = data.get('status', {}).get('code') or data.get('code')
                if status_code == 10000:
                    items = data.get('data', {}).get('items', [])
                    task_info = next((i for i in items if i.get('task_id') == task_id), None)
                    if task_info:
                        status = task_info.get('status')
                        progress = task_info.get('process', 0)

                        filled = int(progress / 5)
                        bar = '█' * filled + '░' * (20 - filled)
                        print(f"\r[{bar}] {progress}% ({task_info.get('status_desc', '')})", end='', file=sys.stderr)

                        if status == 3:  # complete
                            print('', file=sys.stderr)  # newline after progress bar
                            img_uris = task_info.get('img_uris') or []
                            if img_uris:
                                uri = img_uris[0].get('url', '') if isinstance(img_uris[0], dict) else img_uris[0]
                                return uri if uri.startswith('http') else f"https://image.cdn2.seaart.me/{uri}"
                            img_url = task_info.get('img_url', '')
                            if img_url:
                                return img_url
                            return "Complete, but couldn't parse video URL from response."

                        if status in (4, 5):  # error states
                            raise Exception(f"Task failed with status: {status}")

            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="Generate SeaArt Videos")
    parser.add_argument("--type", choices=["t2v", "i2v"], required=True, help="Task type")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--image-url", help="Image URL (required for i2v)")
    parser.add_argument("--model", default="seaart-sono-cast", choices=MODELS.keys(), help="Model to use")
    parser.add_argument("--aspect-ratio", default="9:16", choices=ASPECT_RATIOS.keys(), help="Aspect ratio for t2v")

    args = parser.parse_args()

    token = os.environ.get("SEAART_TOKEN")
    if not token:
        print("Error: SEAART_TOKEN environment variable not set.", file=sys.stderr)
        print("Run: /update-config set SEAART_TOKEN=\"your_t_cookie_value\"", file=sys.stderr)
        sys.exit(1)

    api = SeaArtAPI(token)

    try:
        if args.type == "t2v":
            task_id = api.generate_text_to_video(args.prompt, args.model, args.aspect_ratio)
        else:
            if not args.image_url:
                print("Error: --image-url is required for i2v", file=sys.stderr)
                sys.exit(1)
            task_id = api.generate_image_to_video(args.prompt, args.image_url, args.model)

        print("Waiting for generation to finish...", file=sys.stderr)
        video_url = api.poll_progress(task_id)

        print("\n=== Generation Complete ===")
        print(f"Video URL: {video_url}")

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
