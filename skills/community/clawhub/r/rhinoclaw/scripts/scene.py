#!/usr/bin/env python3
"""High-level scene operations: clear, query, batch create."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def get_info() -> dict:
    """Get document info including objects, layers, materials."""
    with RhinoClient() as client:
        return client.send_command("get_document_info")


def clear_all() -> dict:
    """Delete all objects in the document."""
    info = get_info()
    result = info.get("result", info)
    objects = result.get("objects", [])
    
    deleted = []
    with RhinoClient() as client:
        for obj in objects:
            obj_id = obj.get("id")
            if obj_id:
                try:
                    client.send_command("delete_object", {"id": obj_id})
                    deleted.append(obj_id)
                except:
                    pass
    
    return {"status": "success", "deleted_count": len(deleted), "deleted_ids": deleted}


def select_all() -> dict:
    """Select all objects."""
    info = get_info()
    result = info.get("result", info)
    objects = result.get("objects", [])
    
    ids = [obj.get("id") for obj in objects if obj.get("id")]
    
    with RhinoClient() as client:
        return client.send_command("select_objects", {"ids": ids})


def select_by_layer(layer_name: str) -> dict:
    """Select all objects on a layer."""
    with RhinoClient() as client:
        return client.send_command("select_objects", {
            "filters": {"layer": layer_name},
            "filter_mode": "and"
        })


def select_by_name(name_pattern: str) -> dict:
    """Select objects by name pattern."""
    with RhinoClient() as client:
        return client.send_command("select_objects", {
            "filters": {"name": name_pattern},
            "filter_mode": "and"
        })


def get_selected() -> dict:
    """Get info about selected objects."""
    with RhinoClient() as client:
        return client.send_command("get_selected_objects_info")


def batch_create(objects: list) -> dict:
    """Create multiple objects in a single call.
    
    Args:
        objects: List of object definitions, each with:
            - type: Object type (BOX, SPHERE, etc.)
            - params: Type-specific parameters
            - name: Optional object name
            - layer: Optional layer name
            - color: Optional [r, g, b] color
            - translation: Optional [x, y, z] offset
    """
    with RhinoClient() as client:
        return client.send_command("create_objects", {"objects": objects})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scene operations')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Info
    subparsers.add_parser('info', help='Get document info')
    
    # Clear
    subparsers.add_parser('clear', help='Delete all objects')
    
    # Select all
    subparsers.add_parser('select-all', help='Select all objects')
    
    # Select by layer
    layer_p = subparsers.add_parser('select-layer', help='Select by layer')
    layer_p.add_argument('layer', help='Layer name')
    
    # Select by name
    name_p = subparsers.add_parser('select-name', help='Select by name')
    name_p.add_argument('pattern', help='Name pattern')
    
    # Get selected
    subparsers.add_parser('selected', help='Get selected objects info')
    
    # Batch create
    batch_p = subparsers.add_parser('batch', help='Batch create objects')
    batch_p.add_argument('--json', '-j', type=str, required=True, 
                         help='JSON file or string with objects array')
    
    args = parser.parse_args()
    
    if args.action == 'info':
        result = get_info()
    elif args.action == 'clear':
        result = clear_all()
    elif args.action == 'select-all':
        result = select_all()
    elif args.action == 'select-layer':
        result = select_by_layer(args.layer)
    elif args.action == 'select-name':
        result = select_by_name(args.pattern)
    elif args.action == 'selected':
        result = get_selected()
    elif args.action == 'batch':
        # Try to parse as JSON string first, then as file
        try:
            objects = json.loads(args.json)
        except json.JSONDecodeError:
            with open(args.json) as f:
                objects = json.load(f)
        result = batch_create(objects)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
