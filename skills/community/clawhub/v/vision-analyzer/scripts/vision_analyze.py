#!/usr/bin/env python3
"""
Vision Analyzer - Analyze images using Ollama Kimi K2.5
Part of vision-analyzer skill for OpenClaw
"""

import sys
import base64
import json
import urllib.request
import urllib.error
import os

OLLAMA_URL = "https://ollama.com/api/generate"
MODEL = "kimi-k2.5:cloud"
API_KEY = os.environ.get("OLLAMA_API_KEY", "")

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def analyze_image(image_path, prompt="Describe this image in detail"):
    """Send image to Ollama API for analysis"""
    
    if not API_KEY:
        return "Error: OLLAMA_API_KEY environment variable not set"
    
    if not os.path.exists(image_path):
        return f"Error: File not found: {image_path}"
    
    # Encode image
    try:
        base64_image = encode_image(image_path)
    except Exception as e:
        return f"Error encoding image: {e}"
    
    # Build request payload (Ollama format)
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [base64_image],
        "stream": False
    }
    
    # Prepare request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data, headers=headers, method='POST')
    
    # Send request
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "No response field found")
    except urllib.error.HTTPError as e:
        return f"HTTP Error: {e.code} - {e.reason}"
    except urllib.error.URLError as e:
        return f"URL Error: {e.reason}"
    except Exception as e:
        return f"Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python vision_analyze.py <image_path> [prompt]")
        print("Example: python vision_analyze.py photo.jpg 'What do you see?'")
        sys.exit(1)
    
    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Describe this image in detail"
    
    result = analyze_image(image_path, prompt)
    print(result)

if __name__ == "__main__":
    main()
