#!/usr/bin/env python3
"""Vultr Inference API helper for image generation."""

import argparse
import json
import os
import sys
import urllib.request

API_BASE = "https://api.vultrinference.com/v1"

def get_api_key():
    key_path = os.path.expanduser("~/.config/vultr/api_key")
    if not os.path.exists(key_path):
        print(f"Error: API key not found at {key_path}")
        sys.exit(1)
    return open(key_path).read().strip()

def generate_image(prompt, model="flux", size="1024x1024", n=1, output=None):
    """Generate an image using Vultr Inference API."""
    api_key = get_api_key()
    
    url = f"{API_BASE}/images/generations"
    data = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": size
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    print(f"Generating image with {model}...")
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode())
    
    images = result.get("data", [])
    if not images:
        print("Error: No images generated")
        sys.exit(1)
    
    for i, img in enumerate(images):
        img_url = img.get("url")
        if img_url:
            if output and n == 1:
                filename = output
            else:
                filename = f"generated_{i}.png"
            
            print(f"Downloading to {filename}...")
            urllib.request.urlretrieve(img_url, filename)
            print(f"Saved: {filename}")
    
    return images

def list_models():
    """List available models."""
    api_key = get_api_key()
    
    url = f"{API_BASE}/models"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}"}
    )
    
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    
    print("Available Models:")
    print("=" * 50)
    for model in result.get("data", []):
        model_id = model.get("id", "unknown")
        model_type = model.get("type", "unknown")
        print(f"  {model_id} ({model_type})")

def main():
    parser = argparse.ArgumentParser(description="Vultr Inference API")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Image generation
    img_parser = subparsers.add_parser("image", help="Generate an image")
    img_parser.add_argument("prompt", help="Image description")
    img_parser.add_argument("--model", "-m", default="flux", 
                           help="Model: flux, flux-pro, flux-dev (default: flux)")
    img_parser.add_argument("--size", "-s", default="1024x1024",
                           help="Size: 256x256, 512x512, 1024x1024 (default: 1024x1024)")
    img_parser.add_argument("--number", "-n", type=int, default=1,
                           help="Number of images (default: 1)")
    img_parser.add_argument("--output", "-o", help="Output filename")
    
    # List models
    subparsers.add_parser("models", help="List available models")
    
    args = parser.parse_args()
    
    if args.command == "image":
        generate_image(args.prompt, args.model, args.size, args.number, args.output)
    elif args.command == "models":
        list_models()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
