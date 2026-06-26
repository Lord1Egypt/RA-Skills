#!/usr/bin/env python3
"""
Fetch free models from OpenRouter API.
Part of the updating-openrouter-free-models skill.
"""

import json
import subprocess
import sys
from pathlib import Path

def is_free_model(model_data):
    """
    Determine if a model is free based on:
    1. ID contains ':free' suffix, OR
    2. All pricing fields (prompt, completion, request) are 0 or "0"
    """
    model_id = model_data.get('id', '')
    pricing = model_data.get('pricing', {})

    # Check for :free suffix
    if ':free' in model_id:
        return True

    # Check if all pricing fields are zero (handle both string and numeric)
    prompt_price = pricing.get('prompt')
    completion_price = pricing.get('completion')
    request_price = pricing.get('request')

    # Convert to numeric for comparison
    def is_zero(val):
        if val is None:
            return False
        try:
            return float(val) == 0.0
        except (ValueError, TypeError):
            return False

    return is_zero(prompt_price) and is_zero(completion_price) and is_zero(request_price)

def fetch_free_models():
    """Query OpenRouter API and extract free model IDs."""
    cmd = ["curl", "-s", "https://openrouter.ai/api/v1/models"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        print(f"Error fetching models: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON response: {e}", file=sys.stderr)
        sys.exit(1)

    if 'data' not in data:
        print("Unexpected API response structure", file=sys.stderr)
        sys.exit(1)

    # Filter free models using comprehensive check
    free_models = [
        m['id'] for m in data['data']
        if is_free_model(m)
    ]

    return sorted(set(free_models))  # Deduplicate and sort

def main():
    output_file = Path('/tmp/free_models.txt')
    models = fetch_free_models()

    output_file.write_text('\n'.join(models))
    print(f"✓ Fetched {len(models)} free models")
    print(f"  Saved to: {output_file}")
    print("\nTop 10 models:")
    for m in models[:10]:
        print(f"  - {m}")

if __name__ == "__main__":
    main()
