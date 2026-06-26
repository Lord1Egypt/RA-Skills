#!/usr/bin/env python3
"""Object analysis: bounding box, volume, area, properties."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def get_object_info(object_id: str) -> dict:
    """Get basic info about an object.
    
    Args:
        object_id: Object GUID
    
    Returns:
        Object type, name, layer, bounding box
    """
    params = {"object_id": object_id}
    
    with RhinoClient() as client:
        return client.send_command("get_object_info", params)


def get_object_properties(object_id: str) -> dict:
    """Get detailed properties including area/volume.
    
    Args:
        object_id: Object GUID
    
    Returns:
        Full properties: type, bounds, area, volume, centroid, etc.
    """
    params = {"object_id": object_id}
    
    with RhinoClient() as client:
        return client.send_command("get_object_properties", params)


def get_selected_info() -> dict:
    """Get info about all selected objects."""
    with RhinoClient() as client:
        return client.send_command("get_selected_objects_info", {})


def get_document_info() -> dict:
    """Get document info including object counts by type."""
    with RhinoClient() as client:
        return client.send_command("get_document_info", {})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Object analysis')
    subparsers = parser.add_subparsers(dest='action', help='Analysis action')
    
    # Object info
    info_p = subparsers.add_parser('info', help='Get basic object info')
    info_p.add_argument('object_id', help='Object GUID')
    
    # Object properties (detailed)
    props_p = subparsers.add_parser('properties', help='Get detailed properties')
    props_p.add_argument('object_id', help='Object GUID')
    
    # Selected objects info
    subparsers.add_parser('selected', help='Get info about selected objects')
    
    # Document info
    subparsers.add_parser('document', help='Get document summary')
    
    args = parser.parse_args()
    
    if args.action == 'info':
        result = get_object_info(args.object_id)
    elif args.action == 'properties':
        result = get_object_properties(args.object_id)
    elif args.action == 'selected':
        result = get_selected_info()
    elif args.action == 'document':
        result = get_document_info()
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
