#!/usr/bin/env python3
"""
Batch test models from fetched list.
Part of the updating-openrouter-free-models skill.
"""

import json
import subprocess
import time
import sys
import os
from pathlib import Path

def test_model(model_id, token, timeout=30):
    """Test if a model is available. Returns (success, error_msg)."""
    cmd = [
        "curl", "-s", "-m", str(timeout), "-X", "POST",
        "https://openrouter.ai/api/v1/chat/completions",
        "-H", f"Authorization: Bearer {token}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "model": model_id,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 5
        })
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    try:
        resp = json.loads(result.stdout)
        if "error" in resp:
            error = resp['error']
            return False, f"{error.get('code', 'ERR')}: {error.get('message', 'Unknown')}"
        elif "choices" in resp:
            return True, None
        return False, "No choices in response"
    except json.JSONDecodeError:
        output = result.stdout[:80] if result.stdout else "(empty)"
        return False, f"JSON parse error: {output}"

def main():
    # Try ANTHROPIC_AUTH_TOKEN first (for Claude Code compatibility)
    token = os.environ.get('ANTHROPIC_AUTH_TOKEN', '').strip()

    # If not set, try OPENROUTER_API_KEY (for OpenRouter)
    if not token:
        token = os.environ.get('OPENROUTER_API_KEY', '').strip()

    # If still not set, try reading from OpenClaw config
    if not token:
        try:
            with open(Path.home() / '.openclaw' / 'openclaw.json') as f:
                cfg = json.load(f)
                token = cfg.get('models', {}).get('providers', {}).get('openrouter', {}).get('apiKey', '').strip()
        except Exception:
            pass

    if not token:
        print("Error: No API token found. Set ANTHROPIC_AUTH_TOKEN or OPENROUTER_API_KEY environment variable,", file=sys.stderr)
        print("       or configure openrouter.apiKey in ~/.openclaw/openclaw.json", file=sys.stderr)
        sys.exit(1)

    models_file = Path('/tmp/free_models.txt')
    if not models_file.exists():
        print(f"Error: {models_file} not found. Run fetch_models.py first.", file=sys.stderr)
        sys.exit(1)

    models = models_file.read_text().strip().split('\n')
    print(f"Testing {len(models)} models...\n")

    verified = []
    failed = []

    for i, model in enumerate(models, 1):
        success, error = test_model(model, token)

        if success:
            verified.append(model)
            print(f"[{i:3d}/{len(models)}] ✓ {model}")
        else:
            failed.append((model, error))
            print(f"[{i:3d}/{len(models)}] ✗ {model}: {error[:60]}")

        time.sleep(0.5)  # Rate limiting to avoid 429

    # Save results
    Path('/tmp/verified_models.txt').write_text('\n'.join(verified))
    Path('/tmp/failed_models.txt').write_text(
        '\n'.join(f"{m}:{e}" for m, e in failed)
    )

    print(f"\n{'='*60}")
    print(f"✅ Verified: {len(verified)} models")
    print(f"❌ Failed: {len(failed)} models")
    print(f"   Results saved to /tmp/verified_models.txt and /tmp/failed_models.txt")

if __name__ == "__main__":
    main()
