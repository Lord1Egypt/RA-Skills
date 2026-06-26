#!/usr/bin/env python3
"""
Apply verified models to configuration files.
Part of the updating-openrouter-free-models skill.
"""

import json
import subprocess
import sys
from pathlib import Path

def validate_json(filepath):
    """Check if file is valid JSON."""
    try:
        with open(filepath) as f:
            json.load(f)
        return True, None
    except Exception as e:
        return False, str(e)

def update_claude_settings(verified_models):
    """Update ~/.claude/settings.json with verified models."""
    settings_path = Path.home() / '.claude' / 'settings.json'

    if not settings_path.exists():
        print(f"Warning: {settings_path} not found, skipping")
        return

    with open(settings_path) as f:
        config = json.load(f)

    # Keep primary model as first, add rest as availableModels
    primary = "stepfun/step-3.5-flash:free"
    fallbacks = [m for m in verified_models if m != primary]

    config['model'] = primary
    config['availableModels'] = verified_models

    # Write with proper formatting
    with open(settings_path, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')

    valid, err = validate_json(settings_path)
    if valid:
        print(f"✓ Updated Claude settings with {len(verified_models)} models")
    else:
        print(f"✗ Claude settings JSON error: {err}")
        sys.exit(1)

def update_openclaw_config(verified_models):
    """Update ~/.openclaw/openclaw.json with verified models."""
    config_path = Path.home() / '.openclaw' / 'openclaw.json'

    if not config_path.exists():
        print(f"Warning: {config_path} not found, skipping")
        return

    with open(config_path) as f:
        config = json.load(f)

    primary = "stepfun/step-3.5-flash:free"

    # Update provider.models
    provider_models = []
    for model_id in verified_models:
        provider_models.append({
            "id": model_id,
            "name": model_id.split('/')[-1],
            "api": "openai-completions"
        })
    config['models']['providers']['openrouter']['models'] = provider_models

    # Update fallbacks (excluding primary)
    fallbacks = [f"openrouter/{m}" for m in verified_models if m != primary]
    config['agents']['defaults']['model']['fallbacks'] = fallbacks

    # Update agents.defaults.models
    for model_id in verified_models:
        key = f"openrouter/{model_id}"
        if key not in config['agents']['defaults']['models']:
            config['agents']['defaults']['models'][key] = {}

    # Write
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')

    valid, err = validate_json(config_path)
    if valid:
        print(f"✓ Updated OpenClaw config with {len(verified_models)} models")
    else:
        print(f"✗ OpenClaw JSON error: {err}")
        sys.exit(1)

def main():
    verified_file = Path('/tmp/verified_models.txt')
    if not verified_file.exists():
        print("Error: /tmp/verified_models.txt not found. Run test_models.py first.", file=sys.stderr)
        sys.exit(1)

    verified_models = verified_file.read_text().strip().split('\n')
    print(f"Applying {len(verified_models)} verified models...\n")

    update_claude_settings(verified_models)
    update_openclaw_config(verified_models)

    print("\n✅ All configurations updated successfully!")
    print("\nNext steps:")
    print("1. Test with: claude code --model stepfun/step-3.5-flash:free")
    print("2. Test with: openclaw (verify fallbacks work)")

if __name__ == "__main__":
    main()
