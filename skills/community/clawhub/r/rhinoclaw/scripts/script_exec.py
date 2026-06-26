#!/usr/bin/env python3
"""
Execute RhinoScript Python code in Rhino via RhinoClaw.
"""

import argparse
import json
import sys
from rhino_client import RhinoClient


def execute_script(code: str) -> dict:
    """Execute RhinoScript Python code."""
    with RhinoClient() as client:
        return client.send_command("execute_rhinoscript_python_code", {"code": code})


def execute_file(filepath: str) -> dict:
    """Execute a Python script file."""
    with open(filepath, 'r') as f:
        code = f.read()
    return execute_script(code)


def main():
    parser = argparse.ArgumentParser(description='Execute RhinoScript in Rhino')
    parser.add_argument('--code', '-c', type=str, help='Python code to execute')
    parser.add_argument('--file', '-f', type=str, help='Python file to execute')
    parser.add_argument('--stdin', '-s', action='store_true', help='Read code from stdin')
    
    args = parser.parse_args()
    
    if args.code:
        code = args.code
    elif args.file:
        with open(args.file, 'r') as f:
            code = f.read()
    elif args.stdin:
        code = sys.stdin.read()
    else:
        parser.print_help()
        print("\nError: Must provide --code, --file, or --stdin", file=sys.stderr)
        sys.exit(1)
    
    result = execute_script(code)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
