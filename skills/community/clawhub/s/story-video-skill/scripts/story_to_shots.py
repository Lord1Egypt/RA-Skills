#!/usr/bin/env python3
"""
story_to_shots.py
Breaks a story outline into individual shot descriptions using MiniMax LLM API.
Outputs JSON list of shots with detailed visual descriptions.
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional

# Configuration
API_ENDPOINT = "https://api.minimaxi.com/v1/text/chatcompletion_v2"
MODEL = "MiniMax-M2.7"  # MiniMax-M2.7, MiniMax-M2.5-highspeed also available

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def get_api_key() -> str:
    """Get API key from environment."""
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY environment variable not set")
    return api_key


def load_story(story_path: str) -> str:
    """Load story text from file or return as-is if it's direct text."""
    path = Path(story_path)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    # Assume it's direct text content
    return story_path


def build_prompt(story_text: str) -> str:
    """Build the prompt for shot breakdown."""
    return f"""You are a professional film director and storyboard artist. 
Break down the following story into individual shots for video production.

For each shot, provide:
1. shot_number: Sequential number
2. description: Brief narrative description of what happens in this shot
3. visual_description: Detailed visual description for image generation (describe scene, characters, camera angle, lighting, mood, colors, composition)
4. duration_suggestion: Estimated duration in seconds (2-8 seconds typical)
5. camera_movement: e.g., "static", "pan left", "zoom in", "tracking shot", "tilt up"

Story:
---
{story_text}
---

Output ONLY a valid JSON array of shots. No markdown, no explanation.
Example format:
[
  {{
    "shot_number": 1,
    "description": "Wide establishing shot of a mountain village at sunrise",
    "visual_description": "Aerial view of ancient stone houses clustered on a hillside, golden hour lighting, mist rising from valleys below, warm orange and purple sky, cinematic wide lens, photorealistic",
    "duration_suggestion": 5,
    "camera_movement": "static"
  }}
]
"""


def call_llm_with_retry(prompt: str, api_key: str, timeout: int = 120) -> Dict[str, Any]:
    """Call MiniMax LLM API with retry logic."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4000,
        "temperature": 0.7
    }
    
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            print(f"  [Attempt {attempt + 1}/{MAX_RETRIES}] Calling LLM API...")
            response = requests.post(
                API_ENDPOINT,
                headers=headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract content from MiniMax response format
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not content:
                # Try alternative format
                content = result.get("content", "")
            
            return {"success": True, "content": content, "raw": result}
            
        except requests.exceptions.Timeout:
            last_error = f"Request timeout after {timeout}s"
            print(f"  Timeout: {last_error}")
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            print(f"  Request error: {last_error}")
        except json.JSONDecodeError as e:
            last_error = f"JSON decode error: {e}"
            print(f"  Response parse error: {last_error}")
        
        if attempt < MAX_RETRIES - 1:
            print(f"  Retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
    
    return {"success": False, "error": last_error}


def parse_shots(content: str) -> List[Dict[str, Any]]:
    """Parse JSON shots from LLM response content."""
    # Try to extract JSON from markdown code blocks first
    import re
    
    # Remove markdown code blocks if present
    content = re.sub(r'^```json\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^```\s*', '', content, flags=re.MULTILINE)
    
    # Find JSON array
    json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
    else:
        # Try the whole content
        json_str = content.strip()
    
    try:
        shots = json.loads(json_str)
        # Validate structure
        for shot in shots:
            if "shot_number" not in shot:
                shot["shot_number"] = shots.index(shot) + 1
        return shots
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse shots JSON: {e}\nContent: {content[:500]}")


def generate_shots(story_input: str, output_path: str = "./output/shots.json") -> List[Dict[str, Any]]:
    """
    Main function to convert story to shots.
    
    Args:
        story_input: Path to story file or direct story text
        output_path: Path to save the JSON output
        
    Returns:
        List of shot dictionaries
    """
    print("=" * 60)
    print("STORY TO SHOTS")
    print("=" * 60)
    
    # Get API key
    api_key = get_api_key()
    print(f"[OK] API key loaded")
    
    # Load story
    story_text = load_story(story_input)
    print(f"[OK] Story loaded ({len(story_text)} characters)")
    print(f"  Preview: {story_text[:100]}...")
    
    # Build prompt
    prompt = build_prompt(story_text)
    
    # Call LLM
    print("[...] Calling LLM API to generate shots...")
    result = call_llm_with_retry(prompt, api_key)
    
    if not result["success"]:
        raise RuntimeError(f"LLM API call failed: {result['error']}")
    
    content = result["content"]
    print(f"[OK] Received response ({len(content)} characters)")
    
    # Parse shots
    print("[...] Parsing shot descriptions...")
    shots = parse_shots(content)
    print(f"[OK] Parsed {len(shots)} shots")
    
    # Save output
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(shots, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Saved to {output_path}")
    
    # Print summary
    print("\nSHOT SUMMARY:")
    print("-" * 40)
    for shot in shots:
        print(f"  Shot {shot['shot_number']}: {shot['description'][:50]}...")
        print(f"    Duration: {shot.get('duration_suggestion', 'N/A')}s | Camera: {shot.get('camera_movement', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
    
    return shots


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert story to shot list")
    parser.add_argument("story", nargs="?", default=None, help="Story text or path to story file")
    parser.add_argument("-o", "--output", default="./output/shots.json", help="Output JSON path")
    
    args = parser.parse_args()
    
    if not args.story:
        # Interactive mode
        print("Enter your story (Ctrl+D to finish):")
        story_text = ""
        try:
            while True:
                story_text += input() + "\n"
        except EOFError:
            pass
        args.story = story_text
    
    try:
        shots = generate_shots(args.story, args.output)
        print(f"\nSuccessfully generated {len(shots)} shots!")
    except Exception as e:
        print(f"\nERROR: {e}")
        exit(1)
