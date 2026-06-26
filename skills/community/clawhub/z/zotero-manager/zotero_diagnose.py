#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero 本地 API 诊断工具

检查 Zotero 7 本地 API 是否正确配置和运行
"""

import requests
import sys

# 可能的 API 端点
ENDPOINTS = [
    'http://localhost:23119',
    'http://127.0.0.1:23119',
    'http://localhost:23119/api',
    'http://localhost:23119/api/2',
    'http://localhost:23119/api/2/items',
    'http://localhost:23119/api/2/collections',
]

def check_endpoint(url):
    """检查端点是否可用"""
    try:
        response = requests.get(url, timeout=3)
        return {
            'url': url,
            'status': response.status_code,
            'available': True,
            'content_type': response.headers.get('Content-Type', '')
        }
    except requests.exceptions.ConnectionError:
        return {'url': url, 'status': 0, 'available': False, 'error': 'Connection refused'}
    except requests.exceptions.Timeout:
        return {'url': url, 'status': 0, 'available': False, 'error': 'Timeout'}
    except Exception as e:
        return {'url': url, 'status': 0, 'available': False, 'error': str(e)}


def main():
    print("=" * 60)
    print("Zotero Local API Diagnostic Tool")
    print("=" * 60)
    print()
    
    print("Checking Zotero 7 local API endpoints...")
    print("-" * 60)
    
    available_endpoints = []
    
    for endpoint in ENDPOINTS:
        result = check_endpoint(endpoint)
        status = "[OK]" if result['available'] else "[FAIL]"
        print(f"{status}: {endpoint}")
        if result['available']:
            print(f"   Status: {result['status']}")
            print(f"   Content-Type: {result['content_type']}")
            available_endpoints.append(result)
        elif 'error' in result:
            print(f"   Error: {result['error']}")
    
    print()
    print("-" * 60)
    
    if available_endpoints:
        print(f"\n[OK] Found {len(available_endpoints)} available endpoint(s)")
        print("\nSuggested API base URL:")
        for ep in available_endpoints:
            base_url = ep['url'].replace('/items', '').replace('/collections', '')
            print(f"  --api-url {base_url}")
    else:
        print("\n[FAIL] No available Zotero local API endpoint found")
        print("\nPlease check:")
        print("1. Is Zotero 7 running?")
        print("2. Is local API service enabled?")
        print("3. Is the port correct? (default: 23119)")
        print("\nHow to enable in Zotero 7:")
        print("  Edit -> Preferences -> Advanced -> Local API service")
        print("  Check 'Allow other applications to access Zotero data via HTTP'")
    
    print()


if __name__ == '__main__':
    main()
