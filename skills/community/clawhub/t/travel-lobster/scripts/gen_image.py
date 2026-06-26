#!/usr/bin/env python3
"""Generate an image using Gemini Flash via OpenRouter API."""
import requests, base64, json, sys, os

def generate_image(prompt: str, output_path: str) -> bool:
    """Generate image from prompt and save to output_path. Returns True on success."""
    # API key: only from environment variable, never auto-scan config files
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set", file=sys.stderr)
        print("Set it with: export OPENROUTER_API_KEY=your_key", file=sys.stderr)
        return False

    model = os.environ.get("TRAVEL_IMAGE_MODEL", "google/gemini-3.1-flash-image-preview")
    
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "modalities": ["text", "image"]
            },
            timeout=120
        )
        resp.raise_for_status()
        data = resp.json()
        
        img_url = data["choices"][0]["message"]["images"][0]["image_url"]["url"]
        img_b64 = img_url.split(",", 1)[1]
        
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(img_b64))
        
        print(f"Saved to {output_path}")
        return True
        
    except requests.exceptions.HTTPError as e:
        # Only print status code, never the full response (may contain auth info in headers)
        print(f"Error: HTTP {e.response.status_code if e.response else 'unknown'}", file=sys.stderr)
        return False
    except requests.exceptions.RequestException as e:
        # Generic network error — print type only, not full message (may leak URL/headers)
        print(f"Error: Network request failed ({type(e).__name__})", file=sys.stderr)
        return False
    except (KeyError, IndexError) as e:
        print(f"Error: Unexpected API response format", file=sys.stderr)
        return False
    except Exception as e:
        # Catch-all — only print error type, never the message
        print(f"Error: {type(e).__name__}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <prompt> <output_path>", file=sys.stderr)
        sys.exit(1)
    
    success = generate_image(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
