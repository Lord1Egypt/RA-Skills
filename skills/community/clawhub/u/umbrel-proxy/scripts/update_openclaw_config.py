#!/usr/bin/env python3
"""
Update OpenClaw config with discovered Umbrel proxy service URLs.
"""

import subprocess
import json
import os
import sys
from typing import Dict, List

def run_command(cmd: str) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        return ""

def load_mappings(filename: str = "umbrel_services.json") -> List[Dict]:
    """Load service mappings from JSON file."""
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run discover_umbrel_services.py first.")
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)

def get_openclaw_plugin_config(plugin_name: str) -> Dict:
    """Get current OpenClaw config for a plugin."""
    cmd = f"openclaw config get plugins.entries.{plugin_name}"
    output = run_command(cmd)
    
    if "not found" in output or "undefined" in output:
        return {}
    
    # Parse the output (it's not pure JSON, need to extract)
    lines = output.split('\n')
    for line in lines:
        if plugin_name in line and 'config' in line:
            # Try to extract URL
            if 'http://' in line:
                url_start = line.find('http://')
                url = line[url_start:].strip()
                return {'baseUrl': url}
    
    return {}

def update_plugin_config(plugin_name: str, base_url: str) -> bool:
    """Update OpenClaw config for a plugin."""
    config_path = f"plugins.entries.{plugin_name}.config.baseUrl"
    cmd = f"openclaw config set {config_path} {base_url}"
    
    print(f"Updating {plugin_name}: {base_url}")
    output = run_command(cmd)
    
    if "Updated" in output or "Config overwrite" in output:
        print(f"  ✓ Success")
        return True
    else:
        print(f"  ✗ Failed: {output[:100]}...")
        return False

def map_app_to_plugin(app_name: str) -> str:
    """Map Umbrel app name to OpenClaw plugin name."""
    plugin_map = {
        'perplexica': 'perplexica',
        'searxng': 'searxng',
        'jellyfin': 'jellyfin',
        'openwebui': 'openwebui',
        'ollama': 'ollama',
        'synapse': 'matrix',
        'element': 'matrix-web'
    }
    
    return plugin_map.get(app_name, app_name)

def update_openclaw_config(mappings: List[Dict]) -> int:
    """Main update function."""
    print("=== Updating OpenClaw Config ===\n")
    
    if not mappings:
        print("No mappings to update.")
        return 1
    
    updates_applied = 0
    updates_failed = 0
    
    for mapping in mappings:
        app_name = mapping['app_name']
        proxy_port = mapping['proxy_port']
        plugin_name = map_app_to_plugin(app_name)
        
        base_url = f"http://localhost:{proxy_port}"
        
        # Check current config
        current_config = get_openclaw_plugin_config(plugin_name)
        current_url = current_config.get('baseUrl', '')
        
        if current_url == base_url:
            print(f"{plugin_name}: Already configured correctly ✓")
            continue
        
        # Update config
        if update_plugin_config(plugin_name, base_url):
            updates_applied += 1
        else:
            updates_failed += 1
    
    print(f"\n=== Summary ===")
    print(f"Updates applied: {updates_applied}")
    print(f"Updates failed: {updates_failed}")
    
    if updates_applied > 0:
        print("\n⚠️  Restart OpenClaw gateway to apply changes:")
        print("  openclaw gateway restart")
    
    return 0 if updates_failed == 0 else 1

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Update OpenClaw config with Umbrel proxy URLs")
    parser.add_argument("--mappings-file", default="umbrel_services.json",
                       help="JSON file with service mappings")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be updated without making changes")
    
    args = parser.parse_args()
    
    mappings = load_mappings(args.mappings_file)
    if not mappings:
        return 1
    
    if args.dry_run:
        print("=== Dry Run: Would Update ===")
        for mapping in mappings:
            app_name = mapping['app_name']
            proxy_port = mapping['proxy_port']
            plugin_name = map_app_to_plugin(app_name)
            print(f"{plugin_name}: http://localhost:{proxy_port}")
        return 0
    
    return update_openclaw_config(mappings)

if __name__ == "__main__":
    sys.exit(main())