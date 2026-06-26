#!/usr/bin/env python3
"""Object operations: get info, modify, delete, select."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def get_object_info(object_id: str) -> dict:
    """Get detailed information about an object."""
    with RhinoClient() as client:
        return client.send_command("get_object_info", {"id": object_id})


def modify_object(object_id: str, name: str = None, layer: str = None,
                  color: list = None, translation: list = None,
                  rotation: list = None, scale: list = None,
                  visible: bool = None) -> dict:
    """Modify object properties or transform.
    
    Args:
        object_id: Object GUID
        name: New object name
        layer: Move to layer
        color: New color [r, g, b]
        translation: Move by [x, y, z]
        rotation: Rotate by [rx, ry, rz] radians
        scale: Scale by [sx, sy, sz]
        visible: Set visibility
    """
    params = {"id": object_id}
    
    if name is not None:
        params["name"] = name
    if layer is not None:
        params["layer"] = layer
    if color is not None:
        params["color"] = color
    if translation is not None:
        params["translation"] = translation
    if rotation is not None:
        params["rotation"] = rotation
    if scale is not None:
        params["scale"] = scale
    if visible is not None:
        params["visible"] = visible
    
    with RhinoClient() as client:
        return client.send_command("modify_object", params)


def delete_object(object_id: str) -> dict:
    """Delete an object by ID."""
    with RhinoClient() as client:
        return client.send_command("delete_object", {"id": object_id})


def select_objects(object_ids: list = None, filters: dict = None, 
                   filter_mode: str = "and", deselect: bool = False) -> dict:
    """Select objects by IDs or filters.
    
    Args:
        object_ids: List of GUIDs to select
        filters: Filter dict (e.g., {"layer": "MyLayer", "name": "Box*"})
        filter_mode: "and" or "or" for multiple filters
        deselect: If True, deselect instead of select
    """
    params = {}
    
    if object_ids:
        params["ids"] = object_ids
    if filters:
        params["filters"] = filters
        params["filter_mode"] = filter_mode
    if deselect:
        params["deselect"] = deselect
    
    with RhinoClient() as client:
        return client.send_command("select_objects", params)


def get_selected_objects() -> dict:
    """Get info about currently selected objects."""
    with RhinoClient() as client:
        return client.send_command("get_selected_objects_info")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Object operations')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Get info
    info_p = subparsers.add_parser('info', help='Get object info')
    info_p.add_argument('object_id', help='Object GUID')
    
    # Modify
    modify_p = subparsers.add_parser('modify', help='Modify object')
    modify_p.add_argument('object_id', help='Object GUID')
    modify_p.add_argument('--name', help='New name')
    modify_p.add_argument('--layer', help='Move to layer')
    modify_p.add_argument('--color', type=str, help='Color as r,g,b')
    modify_p.add_argument('--translate', type=str, help='Move by x,y,z')
    modify_p.add_argument('--rotate', type=str, help='Rotate by rx,ry,rz (radians)')
    modify_p.add_argument('--scale', type=str, help='Scale by sx,sy,sz')
    modify_p.add_argument('--visible', type=str, choices=['true', 'false'], help='Set visibility')
    
    # Delete
    delete_p = subparsers.add_parser('delete', help='Delete object')
    delete_p.add_argument('object_id', help='Object GUID')
    
    # Select
    select_p = subparsers.add_parser('select', help='Select objects')
    select_p.add_argument('--ids', nargs='+', help='Object GUIDs')
    select_p.add_argument('--layer', help='Filter by layer')
    select_p.add_argument('--name', help='Filter by name pattern')
    select_p.add_argument('--mode', choices=['and', 'or'], default='and', help='Filter mode')
    select_p.add_argument('--deselect', action='store_true', help='Deselect instead')
    
    # Get selected
    subparsers.add_parser('selected', help='Get selected objects info')
    
    args = parser.parse_args()
    
    def parse_list(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    def parse_color(s: str) -> list:
        return [int(x) for x in s.split(',')]
    
    if args.action == 'info':
        result = get_object_info(args.object_id)
    elif args.action == 'modify':
        color = parse_color(args.color) if args.color else None
        translation = parse_list(args.translate) if args.translate else None
        rotation = parse_list(args.rotate) if args.rotate else None
        scale = parse_list(args.scale) if args.scale else None
        visible = args.visible == 'true' if args.visible else None
        result = modify_object(
            args.object_id,
            name=args.name,
            layer=args.layer,
            color=color,
            translation=translation,
            rotation=rotation,
            scale=scale,
            visible=visible
        )
    elif args.action == 'delete':
        result = delete_object(args.object_id)
    elif args.action == 'select':
        filters = {}
        if args.layer:
            filters['layer'] = args.layer
        if args.name:
            filters['name'] = args.name
        result = select_objects(
            object_ids=args.ids,
            filters=filters if filters else None,
            filter_mode=args.mode,
            deselect=args.deselect
        )
    elif args.action == 'selected':
        result = get_selected_objects()
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
