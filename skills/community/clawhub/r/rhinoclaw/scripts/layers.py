#!/usr/bin/env python3
"""
Layer management for Rhino via RhinoClaw.
"""

import argparse
import json
import sys
from rhino_client import RhinoClient


def create_layer(name: str, color: list = None, parent: str = None) -> dict:
    """Create a new layer."""
    params = {"name": name}
    if color:
        params["color"] = color
    if parent:
        params["parent"] = parent
    
    with RhinoClient() as client:
        return client.send_command("create_layer", params)


def delete_layer(name: str) -> dict:
    """Delete a layer."""
    with RhinoClient() as client:
        return client.send_command("delete_layer", {"name": name})


def set_current_layer(name: str) -> dict:
    """Set the current active layer."""
    with RhinoClient() as client:
        return client.send_command("get_or_set_current_layer", {"name": name})


def get_current_layer() -> dict:
    """Get the current active layer."""
    with RhinoClient() as client:
        return client.send_command("get_or_set_current_layer", {})


def list_layers() -> dict:
    """List all layers via document info."""
    with RhinoClient() as client:
        info = client.send_command("get_document_info")
        if info.get("status") == "success":
            result = info.get("result", {})
            layers = result.get("layers", [])
            return {"status": "success", "layers": layers, "count": len(layers)}
        return info


def main():
    parser = argparse.ArgumentParser(description='Rhino layer management')
    subparsers = parser.add_subparsers(dest='action', required=True)
    
    # Create
    cp = subparsers.add_parser('create', help='Create a layer')
    cp.add_argument('name', type=str)
    cp.add_argument('--color', '-c', type=str, help='r,g,b')
    cp.add_argument('--parent', '-p', type=str)
    
    # Delete
    dp = subparsers.add_parser('delete', help='Delete a layer')
    dp.add_argument('name', type=str)
    
    # Set current
    sp = subparsers.add_parser('set', help='Set current layer')
    sp.add_argument('name', type=str)
    
    # Get current
    subparsers.add_parser('current', help='Get current layer')
    
    # List
    subparsers.add_parser('list', help='List all layers')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        color = [int(x) for x in args.color.split(',')] if args.color else None
        result = create_layer(args.name, color, args.parent)
    elif args.action == 'delete':
        result = delete_layer(args.name)
    elif args.action == 'set':
        result = set_current_layer(args.name)
    elif args.action == 'current':
        result = get_current_layer()
    elif args.action == 'list':
        result = list_layers()
    else:
        print(f"Unknown action: {args.action}", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
