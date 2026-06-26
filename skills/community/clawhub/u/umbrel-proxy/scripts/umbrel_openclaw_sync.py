#!/usr/bin/env python3
"""
Sync Umbrel proxy services with OpenClaw config (focused on OpenClaw-relevant services).
"""

import subprocess
import json
import os
import sys
import time
import requests
from typing import Dict, List, Optional

def run_command(cmd: str) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr.strip()}"

# OpenClaw-relevant Umbrel services
OPENCLAW_SERVICES = {
    'perplexica': {
        'proxy_port': 3444,
        'openclaw_plugin': 'perplexica',
        'test_path': '/'
    },
    'searxng': {
        'proxy_port': 8182,
        'openclaw_plugin': 'searxng',
        'test_path': '/'
    },
    'synapse': {
        'proxy_port': 8008,
        'openclaw_plugin': 'matrix',
        'test_path': '/_matrix/client/versions'
    },
    'openwebui': {
        'proxy_port': 10123,
        'openclaw_plugin': 'openwebui',
        'test_path': '/'
    },
    'jellyfin': {
        'proxy_port': 8096,
        'openclaw_plugin': 'jellyfin',
        'test_path': '/'
    },
    'ntfy': {
        'proxy_port': 13119,
        'openclaw_plugin': 'ntfy',
        'test_path': '/'
    }
}

def check_service_health(service_name: str, proxy_port: int, test_path: str = '/') -> Dict:
    """Check if a service is accessible via its proxy."""
    url = f"http://localhost:{proxy_port}{test_path}"
    
    result = {
        'service': service_name,
        'url': url,
        'accessible': False,
        'status_code': None,
        'response_time': None,
        'error': None
    }
    
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = (time.time() - start) * 1000
        
        result['accessible'] = True
        result['status_code'] = response.status_code
        result['response_time'] = f"{elapsed:.1f}ms"
        
        # Check if it's a valid response
        if response.status_code >= 400:
            result['accessible'] = False
            result['error'] = f"HTTP {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        result['accessible'] = False
        result['error'] = str(e)
    
    return result

def update_openclaw_config(service_name: str, proxy_port: int, openclaw_plugin: str) -> bool:
    """Update OpenClaw config for a service."""
    config_path = f"plugins.entries.{openclaw_plugin}.config.baseUrl"
    base_url = f"http://localhost:{proxy_port}"
    
    cmd = f"openclaw config set {config_path} {base_url}"
    output = run_command(cmd)
    
    if "Updated" in output or "Config overwrite" in output:
        return True
    else:
        # Check if plugin exists
        check_cmd = f"openclaw config get plugins.entries.{openclaw_plugin}"
        check_output = run_command(check_cmd)
        
        if "not found" in check_output or "undefined" in check_output:
            print(f"  ⚠️  Plugin '{openclaw_plugin}' not configured in OpenClaw")
            return False
        else:
            print(f"  ✗ Failed to update: {output[:100]}...")
            return False

def sync_openclaw_services():
    """Main sync function for OpenClaw-relevant services."""
    print("🦦 Umbrel → OpenClaw Proxy Sync")
    print("=" * 50)
    print()
    
    # Check Docker is running
    docker_status = run_command("docker ps 2>&1 | head -5")
    if "Cannot connect" in docker_status:
        print("❌ Docker is not running or not accessible")
        return 1
    
    print("Checking OpenClaw-relevant Umbrel services...")
    print()
    
    results = []
    updates_needed = []
    
    for service_name, service_info in OPENCLAW_SERVICES.items():
        proxy_port = service_info['proxy_port']
        openclaw_plugin = service_info['openclaw_plugin']
        test_path = service_info['test_path']
        
        print(f"🔍 {service_name} (localhost:{proxy_port})")
        
        # Check health
        health = check_service_health(service_name, proxy_port, test_path)
        
        if health['accessible']:
            status_icon = "✓"
            status_color = "\033[92m"  # Green
            status_text = f"Accessible ({health['status_code']}, {health['response_time']})"
        else:
            status_icon = "✗"
            status_color = "\033[91m"  # Red
            status_text = f"Not accessible: {health['error']}"
        
        print(f"  {status_color}{status_icon} {status_text}\033[0m")
        
        # Check current OpenClaw config
        config_cmd = f"openclaw config get plugins.entries.{openclaw_plugin}.config.baseUrl 2>/dev/null || echo 'NOT_CONFIGURED'"
        current_config = run_command(config_cmd)
        
        expected_url = f"http://localhost:{proxy_port}"
        
        if expected_url in current_config:
            print(f"  ✓ OpenClaw config is correct")
        elif "NOT_CONFIGURED" in current_config or "undefined" in current_config:
            print(f"  ⚠️  OpenClaw plugin '{openclaw_plugin}' not configured")
            if health['accessible']:
                updates_needed.append((service_name, proxy_port, openclaw_plugin))
        else:
            print(f"  🔄 Config mismatch: {current_config[:50]}...")
            if health['accessible']:
                updates_needed.append((service_name, proxy_port, openclaw_plugin))
        
        results.append({
            'service': service_name,
            'health': health,
            'config_status': 'correct' if expected_url in current_config else 'needs_update'
        })
        print()
    
    # Apply updates if needed
    if updates_needed:
        print("=== Applying OpenClaw Config Updates ===")
        
        for service_name, proxy_port, openclaw_plugin in updates_needed:
            print(f"Updating {service_name} → {openclaw_plugin}...")
            
            if update_openclaw_config(service_name, proxy_port, openclaw_plugin):
                print(f"  ✓ Updated successfully")
            else:
                print(f"  ✗ Update failed")
            print()
    
    # Summary
    print("=== Summary ===")
    
    accessible_count = sum(1 for r in results if r['health']['accessible'])
    config_correct_count = sum(1 for r in results if r['config_status'] == 'correct')
    
    print(f"Services accessible: {accessible_count}/{len(results)}")
    print(f"Configs correct: {config_correct_count}/{len(results)}")
    print(f"Updates applied: {len(updates_needed)}")
    print()
    
    # Check if gateway needs restart
    gateway_status = run_command("openclaw gateway status 2>&1")
    if "active (running)" in gateway_status:
        print("⚠️  OpenClaw gateway is running and needs restart to apply changes:")
        print("  openclaw gateway restart")
    else:
        print("✓ OpenClaw gateway is not running (config will apply on next start)")
    
    print()
    
    # Quick reference
    print("Quick Reference:")
    print("----------------")
    for service_name, service_info in OPENCLAW_SERVICES.items():
        proxy_port = service_info['proxy_port']
        openclaw_plugin = service_info['openclaw_plugin']
        print(f"{service_name}: http://localhost:{proxy_port} → {openclaw_plugin}")
    
    print()
    print("✅ Sync complete!")
    
    return 0

if __name__ == "__main__":
    sys.exit(sync_openclaw_services())