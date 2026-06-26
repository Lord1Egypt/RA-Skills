import requests
import os
import sys
import argparse
from typing import Union

API_URL = "https://api.trunkate.ai"

def optimize_prompt(prompt: str, budget: Union[int, str] = 1000, model: str = "gpt-4o") -> str:
    """Optimizes a prompt using the private Trunkate AI API."""
    api_url = os.environ.get("TRUNKATE_API_URL", API_URL).rstrip("/")
    api_key = os.environ.get("TRUNKATE_API_KEY")
    
    if not api_key:
        print("Error: TRUNKATE_API_KEY required.", file=sys.stderr)
        return prompt
    
    payload = {"text": prompt, "budget": budget, "model": model}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(f"{api_url}/optimize", json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("optimized_text", prompt)
    except Exception as e:
        print(f"Error optimizing prompt: {e}", file=sys.stderr)
        return prompt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trunkate AI CLI")
    parser.add_argument("--text", required=True, help="The text to optimize")
    parser.add_argument("--budget", default="1000", help="Max token budget (int or '20%')")
    parser.add_argument("--model", default="gpt-4o", help="Target model")
    
    args = parser.parse_args()
    print(optimize_prompt(args.text, budget=args.budget, model=args.model))