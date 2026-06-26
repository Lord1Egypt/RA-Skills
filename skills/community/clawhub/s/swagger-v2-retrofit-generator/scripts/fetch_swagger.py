#!/usr/bin/env python3
"""
Fetch Swagger v2 API documentation from a given URL.
Supports no auth, Basic Auth, Bearer token, and API Key auth.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse
import base64


def fetch_swagger(
    url: str,
    auth_type: str = 'none',
    username: str = None,
    password: str = None,
    token: str = None,
    api_key: str = None,
    api_key_name: str = 'X-API-Key',
    api_key_in: str = 'header'
) -> dict:
    """
    Fetch Swagger v2 API documentation from the given URL.
    
    Args:
        url: The URL to the Swagger v2 API docs (e.g., http://host/v2/api-docs)
        auth_type: Auth type: none/basic/bearer/api-key
        username: Optional username for Basic Auth
        password: Optional password for Basic Auth
        token: Optional token for Bearer auth
        api_key: Optional key for API Key auth
        api_key_name: API Key name for header/query
        api_key_in: Where API Key is passed: header/query
    
    Returns:
        The parsed JSON as a dictionary
    """
    request_url = url
    request = urllib.request.Request(request_url, method='GET')
    request.add_header('Accept', 'application/json')

    if auth_type == 'basic':
        if not username or not password:
            print('Basic auth requires both --username and --password', file=sys.stderr)
            sys.exit(2)
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        request.add_header('Authorization', f'Basic {credentials}')
    elif auth_type == 'bearer':
        if not token:
            print('Bearer auth requires --token', file=sys.stderr)
            sys.exit(2)
        request.add_header('Authorization', f'Bearer {token}')
    elif auth_type == 'api-key':
        if not api_key:
            print('API Key auth requires --api-key', file=sys.stderr)
            sys.exit(2)
        if api_key_in == 'header':
            request.add_header(api_key_name, api_key)
        else:
            parsed = urllib.parse.urlsplit(url)
            query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
            query.append((api_key_name, api_key))
            new_query = urllib.parse.urlencode(query)
            request_url = urllib.parse.urlunsplit(
                (parsed.scheme, parsed.netloc, parsed.path, new_query, parsed.fragment)
            )
            request = urllib.request.Request(request_url, method='GET')
            request.add_header('Accept', 'application/json')
    elif auth_type != 'none':
        print(f'Unsupported auth type: {auth_type}', file=sys.stderr)
        sys.exit(2)
    
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        if e.code == 401:
            print("Authentication failed. Please check your username and password.", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Fetch Swagger v2 API documentation'
    )
    parser.add_argument(
        'url',
        help='URL to Swagger v2 API docs (e.g., http://host/v2/api-docs)'
    )
    parser.add_argument(
        '--auth-type',
        choices=['none', 'basic', 'bearer', 'api-key'],
        default='none',
        help='Authentication type (default: none)'
    )
    parser.add_argument(
        '-u', '--username',
        help='Username for Basic Authentication'
    )
    parser.add_argument(
        '-p', '--password',
        help='Password for Basic Authentication'
    )
    parser.add_argument(
        '--token',
        help='Token for Bearer Authentication'
    )
    parser.add_argument(
        '--api-key',
        help='Value for API Key Authentication'
    )
    parser.add_argument(
        '--api-key-name',
        default='X-API-Key',
        help='API Key name in header/query (default: X-API-Key)'
    )
    parser.add_argument(
        '--api-key-in',
        choices=['header', 'query'],
        default='header',
        help='Pass API key via header or query (default: header)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Fetch Swagger docs
    # Backward compatible: auto switch to basic when -u/-p is provided
    auth_type = args.auth_type
    if auth_type == 'none' and (args.username or args.password):
        auth_type = 'basic'

    swagger_data = fetch_swagger(
        args.url,
        auth_type=auth_type,
        username=args.username,
        password=args.password,
        token=args.token,
        api_key=args.api_key,
        api_key_name=args.api_key_name,
        api_key_in=args.api_key_in
    )
    
    # Output as formatted JSON
    output = json.dumps(swagger_data, indent=2, ensure_ascii=False)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Swagger docs saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
