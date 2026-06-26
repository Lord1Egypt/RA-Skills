#!/usr/bin/env python3
"""
Generate image using Gemini API.
Usage: python3 generate_image.py "<PROMPT>" "<GEMINI_API_KEY>" <OUTPUT_PATH>
"""

import sys
import json
import base64
import requests

PROMPT = sys.argv[1] if len(sys.argv) > 1 else None
API_KEY = sys.argv[2] if len(sys.argv) > 2 else None
OUTPUT_PATH = sys.argv[3] if len(sys.argv) > 3 else "/tmp/gemini_image.png"

if not PROMPT or not API_KEY:
    print(json.dumps({"error": "Missing required arguments: PROMPT and GEMINI_API_KEY"}))
    sys.exit(1)

# Try Imagen 3 first, fallback to Gemini Flash
def generate_with_imagen():
    """Generate image using Imagen 3.0"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "instances": [{"prompt": PROMPT}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9"
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        # Extract base64 image
        if "predictions" in data and len(data["predictions"]) > 0:
            img_b64 = data["predictions"][0].get("bytesBase64Encoded", "")
            if img_b64:
                img_bytes = base64.b64decode(img_b64)
                with open(OUTPUT_PATH, "wb") as f:
                    f.write(img_bytes)
                return {"success": True, "path": OUTPUT_PATH, "model": "imagen-3.0"}
        
        return {"error": "No image generated", "response": data}
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return {"error": "rate_limited", "message": "Rate limit exceeded, retry after 10s"}
        return {"error": f"HTTP error: {e.response.status_code}", "message": str(e)}
    except Exception as e:
        return {"error": str(e)}

def generate_with_gemini_flash():
    """Fallback to Gemini Flash image generation"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": f"Generate an image: {PROMPT}"}]
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"]
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        # Look for inline image data
        candidates = data.get("candidates", [])
        for candidate in candidates:
            content = candidate.get("content", {})
            parts = content.get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    img_b64 = part["inlineData"].get("data", "")
                    if img_b64:
                        img_bytes = base64.b64decode(img_b64)
                        with open(OUTPUT_PATH, "wb") as f:
                            f.write(img_bytes)
                        return {"success": True, "path": OUTPUT_PATH, "model": "gemini-flash"}
        
        return {"error": "No image in response", "response": data}
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Try Imagen first
    result = generate_with_imagen()
    
    # If Imagen fails or rate limited, try Gemini Flash
    if "error" in result:
        if result.get("error") == "rate_limited":
            print(json.dumps(result))
            sys.exit(1)
        # Try fallback
        result = generate_with_gemini_flash()
    
    print(json.dumps(result, ensure_ascii=False))
