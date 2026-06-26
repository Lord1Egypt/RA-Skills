#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebUnlocker Tool for OpenClaw

Bypass website blocks and scrape web content using Scrapeless Universal Scraping API.
"""

import os
import sys
import time
import json
import argparse
import logging
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

try:
    import requests
except ImportError:
    print(json.dumps({
        'error': 'Missing dependency',
        'message': 'requests library not found. Please install it: pip install requests'
    }), file=sys.stderr)
    sys.exit(1)


class WebUnlocker:
    """WebUnlocker for Scrapeless Universal Scraping API"""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv('X_API_TOKEN')
        if not self.api_token:
            raise ValueError(
                "API token not found. Please set X_API_TOKEN in .env file or environment variable."
            )
        
        self.api_base_url = 'https://api.scrapeless.com'
        self.endpoint = '/api/v2/unlocker/request'
        
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-token': self.api_token
        }
        
        logger.info(f"WebUnlocker initialized with API base URL: {self.api_base_url}")
    
    def _build_request_payload(
        self,
        actor: str,
        url: str,
        method: str = 'GET',
        redirect: bool = False,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        response_type: Optional[str] = None,
        content_types: Optional[List[str]] = None,
        country: str = 'ANY',
        proxy_url: Optional[str] = None,
        js_render: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        input_params = {
            'url': url,
            'method': method,
            'redirect': redirect
        }
        
        if headers:
            input_params['headers'] = headers
        
        if data:
            input_params['data'] = data
        
        # Set response_type in top-level for non-jsRender requests
        if response_type and not js_render:
            input_params['response_type'] = response_type
        
        # content_types is only used with response_type='content'
        if content_types and response_type == 'content':
            input_params['content_types'] = content_types
        
        if js_render:
            input_params['jsRender'] = js_render
        
        payload = {
            'actor': actor,
            'input': input_params
        }
        
        # Build proxy configuration
        proxy_config = {}
        if country:
            proxy_config['country'] = country
        if proxy_url:
            proxy_config['url'] = proxy_url
        
        if proxy_config:
            payload['proxy'] = proxy_config
        
        return payload
    
    def execute(
        self,
        actor: str,
        url: str,
        method: str = 'GET',
        redirect: bool = False,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        response_type: Optional[str] = None,
        content_types: Optional[List[str]] = None,
        country: str = 'ANY',
        proxy_url: Optional[str] = None,
        js_render: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            logger.info(f"Sending request to {actor} for URL: {url}")
            
            payload = self._build_request_payload(
                actor=actor,
                url=url,
                method=method,
                redirect=redirect,
                headers=headers,
                data=data,
                response_type=response_type,
                content_types=content_types,
                country=country,
                proxy_url=proxy_url,
                js_render=js_render
            )
            
            response = requests.post(
                f"{self.api_base_url}{self.endpoint}",
                headers=self.headers,
                json=payload,
                timeout=180  # Global execution timeout as per documentation
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Request completed successfully")
                return {
                    'success': True,
                    'data': result,
                    'status': 'success'
                }
            elif response.status_code == 400:
                raise ValueError(f"Invalid request: {response.json()}")
            elif response.status_code == 429:
                raise RuntimeError("Rate limit exceeded")
            else:
                raise RuntimeError(f"Unexpected status code {response.status_code}: {response.text}")
            
        except Exception as e:
            return {
                'success': False,
                'error': type(e).__name__,
                'message': str(e)
            }


def main():
    parser = argparse.ArgumentParser(
        description='WebUnlocker Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 webunlocker.py --url "https://httpbin.io/get"
  python3 webunlocker.py --url "https://example.com" --response-type plaintext
  python3 webunlocker.py --url "https://example.com" --response-type png
  python3 webunlocker.py --url "https://httpbin.org/post" --method POST --data '{"key": "value"}'
  python3 webunlocker.py --url "https://example.com" --headers '{"User-Agent": "Mozilla/5.0"}'
        """
    )
    
    parser.add_argument('--url', required=True, help='Target URL')
    parser.add_argument('--method', default='GET', choices=['GET', 'POST', 'PUT', 'DELETE'], help='HTTP method (default: GET)')
    parser.add_argument('--redirect', action='store_true', help='Allow redirects')
    parser.add_argument('--headers', type=str, help='Custom headers as JSON string')
    parser.add_argument('--data', type=str, help='Request data as JSON string')
    parser.add_argument('--response-type', default='html', choices=['html', 'plaintext', 'markdown', 'png', 'jpeg', 'network', 'content'], help='Response type (default: html)')
    parser.add_argument('--content-types', type=str, help='Content types to extract (comma-separated)')
    parser.add_argument('--country', default='ANY', help='Country code for proxy (default: ANY)')
    parser.add_argument('--proxy-url', type=str, help='Custom proxy URL')
    parser.add_argument('--js-render', action='store_true', help='Enable JavaScript rendering')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--wait-selector', type=str, help='Wait for element with this selector to appear')
    
    args = parser.parse_args()
    
    try:
        unlocker = WebUnlocker()
        
        # Parse headers and data if provided
        headers = None
        if args.headers:
            headers = json.loads(args.headers)
        
        data = None
        if args.data:
            data = json.loads(args.data)
        
        # Parse content types if provided
        content_types = None
        if args.content_types:
            content_types = args.content_types.split(',')
        
        # Build jsRender configuration
        js_render = None
        if args.js_render:
            js_render = {
                'enabled': True,
                'headless': args.headless,
                'waitUntil': 'load',
                'instructions': [
                    {
                        'wait': 5000,  # Wait 5 seconds for page to load
                        'waitFor': {
                            '0': args.wait_selector if args.wait_selector else 'body',
                            '1': 30000  # 30 seconds timeout for selector
                        }
                    }
                ],
                'response': {
                    'type': args.response_type
                }
            }
            
            # Add response options if needed
            if args.wait_selector:
                js_render['response']['options'] = {
                    'selector': args.wait_selector
                }
            
            # Add content_types if response type is 'content'
            if args.content_types and args.response_type == 'content':
                if 'options' not in js_render['response']:
                    js_render['response']['options'] = {}
                js_render['response']['options']['outputs'] = args.content_types
        
        result = unlocker.execute(
            actor='unlocker.webunlocker',
            url=args.url,
            method=args.method,
            redirect=args.redirect,
            headers=headers,
            data=data,
            response_type=args.response_type,
            content_types=content_types,
            country=args.country,
            proxy_url=args.proxy_url,
            js_render=js_render
        )
        
        # Output result as JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Exit with error code if failed
        if not result.get('success'):
            sys.exit(1)
            
    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': type(e).__name__,
            'message': str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


def webunlocker_scrape(
    url: str,
    method: str = 'GET',
    redirect: bool = False,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    response_type: str = 'html',
    content_types: Optional[List[str]] = None,
    country: str = 'ANY',
    proxy_url: Optional[str] = None,
    js_render: Optional[Dict[str, Any]] = None,
    api_token: Optional[str] = None
) -> Dict[str, Any]:
    """Scrape web content using WebUnlocker
    
    Args:
        url: Target URL
        method: HTTP method (default: GET)
        redirect: Whether to allow redirects (default: False)
        headers: Custom headers
        data: Request data
        response_type: Response type (html, plaintext, markdown, png, jpeg, network, content)
        content_types: Content types to extract (e.g., emails,links,images)
        country: Country code for proxy (default: ANY)
        proxy_url: Custom proxy URL
        js_render: JavaScript rendering configuration
        api_token: API token for Scrapeless API
    
    Returns:
        Dict with success status and result data
    """
    unlocker = WebUnlocker(api_token=api_token)
    return unlocker.execute(
        actor='unlocker.webunlocker',
        url=url,
        method=method,
        redirect=redirect,
        headers=headers,
        data=data,
        response_type=response_type,
        content_types=content_types,
        country=country,
        proxy_url=proxy_url,
        js_render=js_render
    )


def cloudflare_bypass(
    url: str,
    country: str = 'ANY',
    proxy_url: Optional[str] = None,
    js_render: Optional[Dict[str, Any]] = None,
    api_token: Optional[str] = None
) -> Dict[str, Any]:
    """Bypass Cloudflare protection
    
    Args:
        url: Target URL
        country: Country code for proxy (default: ANY)
        proxy_url: Custom proxy URL
        js_render: JavaScript rendering configuration
        api_token: API token for Scrapeless API
    
    Returns:
        Dict with success status and result data
    """
    unlocker = WebUnlocker(api_token=api_token)
    return unlocker.execute(
        actor='unlocker.webunlocker',
        url=url,
        country=country,
        proxy_url=proxy_url,
        js_render=js_render
    )


if __name__ == '__main__':
    main()