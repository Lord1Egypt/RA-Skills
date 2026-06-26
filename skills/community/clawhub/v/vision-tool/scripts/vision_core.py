#!/usr/bin/env python3
"""
Vision analyzer for image recognition using Ollama
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
import requests


class VisionAnalyzer:
    """
    Analyzes images using local model via Ollama.
    
    Uses /api/chat endpoint which provides content directly in response.
    """
    
    DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
    DEFAULT_MODEL = "qwen3.5:4b"

    def __init__(self, ollama_url=DEFAULT_OLLAMA_URL, model=None):
        self.ollama_url = ollama_url
        self.model = model or self.DEFAULT_MODEL

    def clean_thinking_content(self, thinking_text):
        """
        Clean thinking field content by removing empty lines and trimming.
        Used as fallback when content field is not available.
        """
        if not thinking_text:
            return ""
        
        lines = []
        for line in thinking_text.split('\n'):
            stripped = line.strip()
            if stripped:  # Keep non-empty lines
                lines.append(stripped)
        
        return '\n'.join(lines)

    def analyze_image(self, image_path, prompt="Describe this image"):
        """
        Analyze image and return structured result.
        
        Uses /api/chat endpoint which provides content directly.
        Returns dict with success status, analysis, and metadata.
        """
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"Image not found: {image_path}",
                "source": "file_not_found"
            }

        # Read and encode image
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            image_b64 = base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read image: {e}",
                "source": "read_error"
            }

        # Prepare request for /api/chat endpoint
        url = f"{self.ollama_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_b64]
                }
            ],
            "stream": False,
            "think": False,  # Disable thinking field, ensure content has analysis
            "options": {
                "temperature": 0.1,
                "num_predict": 400,
            }
        }

        start_time = time.time()

        try:
            response = requests.post(url, json=payload, timeout=120)
            elapsed = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                message = result.get('message', {})
                
                # Get content directly from message (primary)
                raw_content = message.get('content', '').strip()
                raw_thinking = message.get('thinking', '').strip()
                
                # Determine actual source and content
                final_content = ""
                source = "no_content"
                
                if raw_content:
                    # Direct content available (with think=False)
                    final_content = raw_content
                    source = "content_direct"
                elif raw_thinking:
                    # Fallback: thinking field has content (should not happen with think=False)
                    final_content = self.clean_thinking_content(raw_thinking)
                    source = "thinking_cleaned"
                    print(f"⚠️  Warning: thinking field used despite think=False")
                
                # Build result
                return {
                    "success": True,
                    "analysis": final_content if final_content else "No analysis returned",
                    "image": os.path.basename(image_path),
                    "prompt": prompt,
                    "time_elapsed": f"{elapsed:.2f}s",
                    "source": source,
                    "stats": {
                        "total_duration": result.get('total_duration', 0) / 1e9 
                        if result.get('total_duration') else 0,
                        "prompt_tokens": result.get('prompt_eval_count', 0),
                        "output_tokens": result.get('eval_count', 0),
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "response_text": response.text[:200],
                    "source": "error"
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout (120 seconds)",
                "suggestion": "Try smaller image or check Ollama",
                "source": "timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {e}",
                "source": "exception"
            }


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description="Image recognition using Ollama")
    parser.add_argument("image", help="Image path")
    parser.add_argument("--prompt", default="Describe this image", 
                       help="Analysis prompt")
    parser.add_argument("--debug", action="store_true", 
                       help="Show debug information")

    args = parser.parse_args()

    analyzer = VisionAnalyzer()
    result = analyzer.analyze_image(args.image, args.prompt)

    if args.debug:
        sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    else:
        if result.get("success"):
            sys.stdout.write(f'\nAnalysis ({result.get("time_elapsed", "?")}):\n')
            sys.stdout.write('-' * 60 + '\n')
            sys.stdout.write(result.get("analysis", "No analysis") + '\n')
            sys.stdout.write('-' * 60 + '\n')
        else:
            sys.stdout.write(f'\nError: {result.get("error", "Unknown error")}\n')


if __name__ == "__main__":
    main()