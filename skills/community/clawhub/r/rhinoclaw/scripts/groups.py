#!/usr/bin/env python3
"""Group and block operations."""

import argparse
import json
import sys
from rhino_client import RhinoClient


# ============ GROUPS ============

def create_group(object_ids: list, name: str = None) -> dict:
    """Create a group from objects.
    
    Args:
        object_ids: List of object GUIDs to group
        name: Optional group name
    """
    params = {"object_ids": object_ids}
    if name:
        params["name"] = name
    
    with RhinoClient() as client:
        return client.send_command("create_group", params)


def ungroup(group_name: str = None, object_ids: list = None) -> dict:
    """Ungroup objects.
    
    Args:
        group_name: Name of group to ungroup
        object_ids: Or specific object GUIDs to ungroup
    """
    params = {}
    if group_name:
        params["group_name"] = group_name
    if object_ids:
        params["object_ids"] = object_ids
    
    with RhinoClient() as client:
        return client.send_command("ungroup", params)


# ============ BLOCKS ============

def create_block(object_ids: list, name: str, base_point: list = None, 
                 delete_objects: bool = True) -> dict:
    """Create a block definition from objects.
    
    Args:
        object_ids: List of object GUIDs
        name: Block definition name
        base_point: Insertion base point [x, y, z] (default: origin)
        delete_objects: Delete original objects after creating block
    """
    params = {
        "object_ids": object_ids,
        "name": name,
        "delete_objects": delete_objects
    }
    if base_point:
        params["base_point"] = base_point
    
    with RhinoClient() as client:
        return client.send_command("create_block", params)


def insert_block(name: str, position: list = None, scale: float = 1.0, 
                 rotation: float = 0.0) -> dict:
    """Insert a block instance.
    
    Args:
        name: Block definition name
        position: Insertion point [x, y, z] (default: origin)
        scale: Uniform scale factor
        rotation: Rotation angle in degrees (around Z axis)
    """
    params = {
        "name": name,
        "scale": scale,
        "rotation": rotation
    }
    if position:
        params["position"] = position
    
    with RhinoClient() as client:
        return client.send_command("insert_block", params)


def explode_block(object_id: str, delete_input: bool = True) -> dict:
    """Explode a block instance into individual objects.
    
    Args:
        object_id: Block instance GUID
        delete_input: Delete block instance after exploding
    """
    params = {
        "object_id": object_id,
        "delete_input": delete_input
    }
    
    with RhinoClient() as client:
        return client.send_command("explode_block", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Group and block operations')
    subparsers = parser.add_subparsers(dest='action', help='Operation')
    
    # Create group
    group_p = subparsers.add_parser('group', help='Create group')
    group_p.add_argument('ids', nargs='+', help='Object GUIDs')
    group_p.add_argument('--name', '-n', help='Group name')
    
    # Ungroup
    ungroup_p = subparsers.add_parser('ungroup', help='Ungroup objects')
    ungroup_p.add_argument('--name', '-n', help='Group name')
    ungroup_p.add_argument('--ids', nargs='+', help='Object GUIDs')
    
    # Create block
    block_p = subparsers.add_parser('block-create', help='Create block definition')
    block_p.add_argument('name', help='Block name')
    block_p.add_argument('ids', nargs='+', help='Object GUIDs')
    block_p.add_argument('--base', type=str, help='Base point as x,y,z')
    block_p.add_argument('--keep', '-k', action='store_true', help='Keep original objects')
    
    # Insert block
    insert_p = subparsers.add_parser('block-insert', help='Insert block instance')
    insert_p.add_argument('name', help='Block definition name')
    insert_p.add_argument('--position', '-p', type=str, help='Position as x,y,z')
    insert_p.add_argument('--scale', '-s', type=float, default=1.0, help='Scale factor')
    insert_p.add_argument('--rotation', '-r', type=float, default=0.0, help='Rotation (degrees)')
    
    # Explode block
    explode_p = subparsers.add_parser('block-explode', help='Explode block instance')
    explode_p.add_argument('object_id', help='Block instance GUID')
    explode_p.add_argument('--keep', '-k', action='store_true', help='Keep block instance')
    
    args = parser.parse_args()
    
    def parse_point(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    if args.action == 'group':
        result = create_group(args.ids, args.name)
    elif args.action == 'ungroup':
        result = ungroup(args.name, args.ids)
    elif args.action == 'block-create':
        base = parse_point(args.base) if args.base else None
        result = create_block(args.ids, args.name, base, delete_objects=not args.keep)
    elif args.action == 'block-insert':
        pos = parse_point(args.position) if args.position else None
        result = insert_block(args.name, pos, args.scale, args.rotation)
    elif args.action == 'block-explode':
        result = explode_block(args.object_id, delete_input=not args.keep)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
