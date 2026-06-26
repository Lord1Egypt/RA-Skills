#!/usr/bin/env python3
"""
Discover Umbrel proxy services and map internal Docker IPs to accessible host ports.
"""

import subprocess
import json
import re
from typing import Dict, List, Tuple, Optional
import sys

def run_command(cmd: str) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        return ""

def get_docker_containers() -> List[Dict]:
    """Get all Docker containers with their details."""
    cmd = "docker ps --format '{{.Names}}|{{.Image}}|{{.Ports}}'"
    output = run_command(cmd)
    containers = []
    
    for line in output.split('\n'):
        if not line:
            continue
        parts = line.split('|', 2)
        if len(parts) == 3:
            name, image, ports = parts
            containers.append({
                'name': name,
                'image': image,
                'ports': ports
            })
    
    return containers

def get_container_network_info(container_name: str) -> Dict:
    """Get network information for a container."""
    cmd = f"docker inspect {container_name} --format '{{{{json .NetworkSettings.Networks}}}}'"
    output = run_command(cmd)
    
    if output:
        try:
            networks = json.loads(output)
            # Umbrel uses umbrel_main_network or custom bridge networks
            for network_name, network_info in networks.items():
                if 'umbrel' in network_name or 'br-' in network_name:
                    return {
                        'ip': network_info.get('IPAddress', ''),
                        'network': network_name
                    }
        except json.JSONDecodeError:
            pass
    
    return {'ip': '', 'network': ''}

def find_proxy_containers(containers: List[Dict]) -> List[Dict]:
    """Find Umbrel app proxy containers."""
    proxies = []
    proxy_pattern = re.compile(r'app-proxy')
    
    for container in containers:
        if proxy_pattern.search(container['image']):
            # Extract port mapping from ports string
            ports_str = container['ports']
            port_match = re.search(r'(\d+\.\d+\.\d+\.\d+:)?(\d+)->\d+/tcp', ports_str)
            if port_match:
                host_port = port_match.group(2)
                proxies.append({
                    'name': container['name'],
                    'host_port': host_port,
                    'app_name': container['name'].replace('_app_proxy_1', '').replace('_', '-')
                })
    
    return proxies

def find_service_containers(containers: List[Dict]) -> List[Dict]:
    """Find service containers (not proxies)."""
    services = []
    proxy_pattern = re.compile(r'app-proxy')
    
    for container in containers:
        if not proxy_pattern.search(container['image']):
            network_info = get_container_network_info(container['name'])
            if network_info.get('ip'):
                # Extract exposed ports
                ports = []
                ports_str = container['ports']
                port_matches = re.findall(r'(\d+)/tcp', ports_str)
                for port in port_matches:
                    ports.append(port)
                
                services.append({
                    'name': container['name'],
                    'ip': network_info['ip'],
                    'ports': ports,
                    'image': container['image']
                })
    
    return services

def map_services_to_proxies(services: List[Dict], proxies: List[Dict]) -> List[Dict]:
    """Map services to their proxy containers based on naming patterns."""
    mappings = []
    
    # Create a lookup of proxy containers by base name
    proxy_lookup = {}
    for proxy in proxies:
        # Extract base name from proxy container name
        # Pattern: {app}_app_proxy_1
        if proxy['name'].endswith('_app_proxy_1'):
            base_name = proxy['name'][:-len('_app_proxy_1')]
            proxy_lookup[base_name] = proxy
    
    # Special mapping for complex container names
    special_mappings = {
        'big-bear-umbrel-open-webui_big-bear-open-webui': 'big-bear-umbrel-open-webui',
        'searxng_web': 'searxng',
        'perplexica_web': 'perplexica',
        'synapse_server': 'synapse',
        'element_web': 'element',
        'jellyfin_server': 'jellyfin',
        'openwebui': 'openwebui'  # Simplified name
    }
    
    for service in services:
        service_name = service['name']
        
        # Try to find matching proxy
        matched_proxy = None
        matched_base = None
        
        # Check each possible base name in proxy lookup
        for base_name, proxy in proxy_lookup.items():
            # Check if service name starts with base name
            if service_name.startswith(base_name):
                matched_proxy = proxy
                matched_base = base_name
                break
        
        if not matched_proxy:
            continue
        
        # Get app name (clean for display)
        app_name = special_mappings.get(matched_base, matched_base.replace('_', '-'))
        
        # Special handling for openwebui
        if 'big-bear-umbrel-open-webui' in app_name:
            app_name = 'openwebui'
        
        for port in service['ports']:
            mappings.append({
                'service_name': service_name,
                'service_ip': service['ip'],
                'service_port': port,
                'proxy_name': matched_proxy['name'],
                'proxy_port': matched_proxy['host_port'],
                'app_name': app_name
            })
    
    return mappings

def discover_umbrel_services() -> List[Dict]:
    """Main discovery function."""
    print("=== Discovering Umbrel Proxy Services ===\n")
    
    containers = get_docker_containers()
    if not containers:
        print("No Docker containers found. Is Docker running?")
        return []
    
    proxies = find_proxy_containers(containers)
    services = find_service_containers(containers)
    mappings = map_services_to_proxies(services, proxies)
    
    # Print results
    if mappings:
        print(f"Found {len(mappings)} service mappings:")
        for i, mapping in enumerate(mappings, 1):
            print(f"{i}. {mapping['app_name']}:")
            print(f"   Service: {mapping['service_ip']}:{mapping['service_port']}")
            print(f"   Proxy: localhost:{mapping['proxy_port']}")
            print(f"   Container: {mapping['service_name']}")
            print()
    else:
        print("No Umbrel proxy service mappings found.")
        print("\nAvailable containers:")
        for container in containers:
            print(f"  - {container['name']} ({container['image']})")
    
    return mappings

def save_mappings_to_file(mappings: List[Dict], filename: str = "umbrel_services.json"):
    """Save discovered mappings to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(mappings, f, indent=2)
    print(f"Mappings saved to {filename}")

if __name__ == "__main__":
    mappings = discover_umbrel_services()
    
    if mappings:
        save_mappings_to_file(mappings)
        
        # Generate OpenClaw config update commands
        print("=== OpenClaw Config Update Commands ===")
        for mapping in mappings:
            app_name = mapping['app_name']
            proxy_port = mapping['proxy_port']
            
            # Map common app names to OpenClaw plugin names
            plugin_map = {
                'perplexica': 'perplexica',
                'searxng': 'searxng',
                'jellyfin': 'jellyfin',
                'openwebui': 'openwebui'
            }
            
            plugin_name = plugin_map.get(app_name, app_name)
            print(f"openclaw config set plugins.entries.{plugin_name}.config.baseUrl http://localhost:{proxy_port}")
    
    sys.exit(0 if mappings else 1)