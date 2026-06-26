#!/usr/bin/env python3
"""
Test connectivity to Umbrel proxy services.
"""

import subprocess
import json
import os
import sys
import time
from typing import Dict, List
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_command(cmd: str) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr.strip()}"

def load_mappings(filename: str = "umbrel_services.json") -> List[Dict]:
    """Load service mappings from JSON file."""
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run discover_umbrel_services.py first.")
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)

def test_service_connectivity(service: Dict) -> Dict:
    """Test connectivity to a single service."""
    app_name = service['app_name']
    proxy_port = service['proxy_port']
    service_ip = service['service_ip']
    service_port = service['service_port']
    
    url = f"http://localhost:{proxy_port}"
    internal_url = f"http://{service_ip}:{service_port}"
    
    result = {
        'app_name': app_name,
        'proxy_url': url,
        'internal_url': internal_url,
        'proxy_status': 'unknown',
        'internal_status': 'unknown',
        'proxy_response_time': None,
        'internal_response_time': None,
        'proxy_error': None,
        'internal_error': None
    }
    
    # Test proxy endpoint
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = (time.time() - start) * 1000
        
        result['proxy_status'] = f"{response.status_code}"
        result['proxy_response_time'] = f"{elapsed:.1f}ms"
        
        if response.status_code == 200:
            result['proxy_status'] = "✓ 200 OK"
        elif 300 <= response.status_code < 400:
            result['proxy_status'] = f"↪ {response.status_code} Redirect"
        else:
            result['proxy_status'] = f"✗ {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        result['proxy_status'] = "✗ Failed"
        result['proxy_error'] = str(e)
    
    # Test internal endpoint (may not be accessible from host)
    try:
        start = time.time()
        response = requests.get(internal_url, timeout=3)
        elapsed = (time.time() - start) * 1000
        
        result['internal_status'] = f"{response.status_code}"
        result['internal_response_time'] = f"{elapsed:.1f}ms"
        
        if response.status_code == 200:
            result['internal_status'] = "✓ 200 OK"
        else:
            result['internal_status'] = f"✗ {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        result['internal_status'] = "✗ Not accessible"
        result['internal_error'] = str(e)
    
    return result

def test_all_connectivity(mappings: List[Dict]) -> List[Dict]:
    """Test connectivity to all services in parallel."""
    print("=== Testing Service Connectivity ===\n")
    
    if not mappings:
        print("No services to test.")
        return []
    
    results = []
    
    # Test in parallel for speed
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_service = {
            executor.submit(test_service_connectivity, service): service 
            for service in mappings
        }
        
        for future in as_completed(future_to_service):
            service = future_to_service[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error testing {service['app_name']}: {e}")
    
    # Sort by app name
    results.sort(key=lambda x: x['app_name'])
    
    return results

def print_results(results: List[Dict]):
    """Print connectivity test results in a readable format."""
    if not results:
        return
    
    print(f"{'App':<15} {'Proxy URL':<25} {'Status':<20} {'Response Time':<15}")
    print("=" * 80)
    
    all_healthy = True
    
    for result in results:
        app_name = result['app_name']
        proxy_url = result['proxy_url']
        status = result['proxy_status']
        response_time = result['proxy_response_time'] or "N/A"
        
        # Color coding for status
        if status.startswith("✓"):
            status_display = f"\033[92m{status}\033[0m"  # Green
        elif status.startswith("↪"):
            status_display = f"\033[93m{status}\033[0m"  # Yellow
        elif status.startswith("✗"):
            status_display = f"\033[91m{status}\033[0m"  # Red
            all_healthy = False
        else:
            status_display = status
        
        print(f"{app_name:<15} {proxy_url:<25} {status_display:<20} {response_time:<15}")
        
        # Show internal status if different
        if result['internal_status'] and not result['internal_status'].startswith("✗ Not accessible"):
            internal_status = result['internal_status']
            if "✓" in internal_status:
                internal_status = f"\033[92m{internal_status}\033[0m"
            print(f"  Internal: {result['internal_url']} - {internal_status}")
        
        # Show error if any
        if result['proxy_error']:
            print(f"  Error: {result['proxy_error'][:100]}...")
    
    print("\n" + "=" * 80)
    
    if all_healthy:
        print("\033[92m✓ All services are accessible via proxy\033[0m")
    else:
        print("\033[91m✗ Some services have issues\033[0m")
    
    return all_healthy

def save_results_to_file(results: List[Dict], filename: str = "connectivity_results.json"):
    """Save connectivity results to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {filename}")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test connectivity to Umbrel proxy services")
    parser.add_argument("--mappings-file", default="umbrel_services.json",
                       help="JSON file with service mappings")
    parser.add_argument("--save-results", action="store_true",
                       help="Save results to JSON file")
    
    args = parser.parse_args()
    
    mappings = load_mappings(args.mappings_file)
    if not mappings:
        return 1
    
    results = test_all_connectivity(mappings)
    
    all_healthy = print_results(results)
    
    if args.save_results:
        save_results_to_file(results)
    
    return 0 if all_healthy else 1

if __name__ == "__main__":
    sys.exit(main())