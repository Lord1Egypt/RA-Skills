#!/usr/bin/env python3
"""Selection operations: select by layer, type, name, IDs."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def select_all() -> dict:
    """Select all objects in the document."""
    params = {"all": True}
    
    with RhinoClient() as client:
        return client.send_command("select_objects", params)


def select_none() -> dict:
    """Clear selection."""
    params = {"clear": True}
    
    with RhinoClient() as client:
        return client.send_command("select_objects", params)


def select_by_layer(layer_name: str) -> dict:
    """Select all objects on a layer.
    
    Args:
        layer_name: Name of the layer
    """
    params = {"layer": layer_name}
    
    with RhinoClient() as client:
        return client.send_command("select_objects", params)


def select_by_type(object_type: str) -> dict:
    """Select all objects of a specific type.
    
    Args:
        object_type: One of: curve, surface, solid, mesh, point, line, 
                     circle, arc, polyline, extrusion, text, block
    """
    params = {"type": object_type}
    
    with RhinoClient() as client:
        return client.send_command("select_objects", params)


def select_by_name(name: str) -> dict:
    """Select objects by name (partial match).
    
    Args:
        name: Object name to search for (case-insensitive)
    """
    params = {"name": name}
    
    with RhinoClient() as client:
        return client.send_command("select_objects", params)


def select_by_ids(object_ids: list) -> dict:
    """Select specific objects by their IDs.
    
    Args:
        object_ids: List of object GUIDs
    """
    params = {"ids": object_ids}
    
    with RhinoClient() as client:
        return client.send_command("select_objects", params)


def select_combined(layer: str = None, object_type: str = None, name: str = None) -> dict:
    """Select with combined filters (AND logic).
    
    Args:
        layer: Filter by layer name
        object_type: Filter by object type
        name: Filter by object name
    """
    params = {}
    if layer:
        params["layer"] = layer
    if object_type:
        params["type"] = object_type
    if name:
        params["name"] = name
    
    with RhinoClient() as client:
        return client.send_command("select_objects", params)


def get_selected() -> dict:
    """Get information about currently selected objects."""
    with RhinoClient() as client:
        return client.send_command("get_selected_objects_info", {})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Selection operations')
    subparsers = parser.add_subparsers(dest='action', help='Selection action')
    
    # Select all
    subparsers.add_parser('all', help='Select all objects')
    
    # Clear selection
    subparsers.add_parser('none', help='Clear selection')
    
    # Get selected
    subparsers.add_parser('get', help='Get selected objects info')
    
    # By layer
    layer_p = subparsers.add_parser('layer', help='Select by layer')
    layer_p.add_argument('name', help='Layer name')
    
    # By type
    type_p = subparsers.add_parser('type', help='Select by object type')
    type_p.add_argument('object_type', 
                        choices=['curve', 'surface', 'solid', 'mesh', 'point', 
                                 'line', 'circle', 'arc', 'polyline', 'extrusion', 
                                 'text', 'block'],
                        help='Object type')
    
    # By name
    name_p = subparsers.add_parser('name', help='Select by name (partial match)')
    name_p.add_argument('pattern', help='Name pattern to search')
    
    # By IDs
    ids_p = subparsers.add_parser('ids', help='Select by object IDs')
    ids_p.add_argument('object_ids', nargs='+', help='Object GUIDs')
    
    # Combined
    combined_p = subparsers.add_parser('filter', help='Select with combined filters')
    combined_p.add_argument('--layer', '-l', help='Layer name')
    combined_p.add_argument('--type', '-t', dest='object_type', help='Object type')
    combined_p.add_argument('--name', '-n', help='Object name pattern')
    
    args = parser.parse_args()
    
    if args.action == 'all':
        result = select_all()
    elif args.action == 'none':
        result = select_none()
    elif args.action == 'get':
        result = get_selected()
    elif args.action == 'layer':
        result = select_by_layer(args.name)
    elif args.action == 'type':
        result = select_by_type(args.object_type)
    elif args.action == 'name':
        result = select_by_name(args.pattern)
    elif args.action == 'ids':
        result = select_by_ids(args.object_ids)
    elif args.action == 'filter':
        result = select_combined(args.layer, args.object_type, args.name)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
