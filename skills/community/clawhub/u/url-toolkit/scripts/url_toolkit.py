#!/usr/bin/env python3
"""
URL Toolkit - URL encoding, decoding, parsing, and building
"""

import argparse
import json
import sys
from urllib.parse import urlparse, parse_qs, urlencode, quote, unquote


def cmd_encode(args):
    """URL encode a string"""
    try:
        if args.full:
            # Full encoding (encode all special chars)
            result = quote(args.input, safe='')
        else:
            # Safe encoding (preserve /:?&= etc)
            result = quote(args.input)
        
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def cmd_decode(args):
    """URL decode a string"""
    try:
        result = unquote(args.input)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def cmd_parse(args):
    """Parse URL into components"""
    try:
        parsed = urlparse(args.input)
        
        result = {
            "scheme": parsed.scheme or None,
            "netloc": parsed.netloc or None,
            "host": None,
            "port": None,
            "path": parsed.path or None,
            "query": parsed.query or None,
            "fragment": parsed.fragment or None,
            "params": parsed.params or None
        }
        
        # Extract host and port from netloc
        if parsed.netloc:
            if ':' in parsed.netloc:
                host_part, port_part = parsed.netloc.rsplit(':', 1)
                result["host"] = host_part
                result["port"] = int(port_part) if port_part.isdigit() else None
            else:
                result["host"] = parsed.netloc
        
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def cmd_query_parse(args):
    """Parse query string into key-value pairs"""
    try:
        parsed = parse_qs(args.input)
        
        # Convert lists to single values if only one item
        result = {}
        for key, value in parsed.items():
            if len(value) == 1:
                result[key] = value[0]
            else:
                result[key] = value
        
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def cmd_query_build(args):
    """Build query string from JSON object"""
    try:
        data = json.loads(args.input)
        
        if not isinstance(data, dict):
            return {"success": False, "error": "Input must be a JSON object"}
        
        result = urlencode(data)
        return {"success": True, "result": result}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description='URL Toolkit - URL encoding, decoding, parsing, and building'
    )
    parser.add_argument('action', choices=['encode', 'decode', 'parse', 'query-parse', 'query-build'],
                       help='Action to perform')
    parser.add_argument('--input', required=True, help='Input string or URL')
    parser.add_argument('--full', action='store_true', 
                       help='Full encoding (encode all special chars)')
    
    args = parser.parse_args()
    
    # Execute command
    commands = {
        'encode': cmd_encode,
        'decode': cmd_decode,
        'parse': cmd_parse,
        'query-parse': cmd_query_parse,
        'query-build': cmd_query_build,
    }
    
    result = commands[args.action](args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
