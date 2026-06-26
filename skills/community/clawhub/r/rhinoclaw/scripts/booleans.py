#!/usr/bin/env python3
"""Boolean operations: union, difference, intersection."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def boolean_union(object_ids: list, delete_input: bool = True) -> dict:
    """Create boolean union of multiple solids.
    
    Args:
        object_ids: List of object GUIDs (at least 2)
        delete_input: Delete input objects after operation
    
    Returns:
        Result with new object IDs
    """
    params = {
        "operation": "union",
        "object_ids": object_ids,
        "delete_input": delete_input
    }
    
    with RhinoClient() as client:
        return client.send_command("boolean_operation", params)


def boolean_difference(object_ids: list, delete_input: bool = True) -> dict:
    """Subtract objects from the first object.
    
    Args:
        object_ids: List of object GUIDs - first is the base, rest are subtracted
        delete_input: Delete input objects after operation
    
    Returns:
        Result with new object IDs
    """
    params = {
        "operation": "difference",
        "object_ids": object_ids,
        "delete_input": delete_input
    }
    
    with RhinoClient() as client:
        return client.send_command("boolean_operation", params)


def boolean_intersection(object_ids: list, delete_input: bool = True) -> dict:
    """Create boolean intersection of multiple solids.
    
    Args:
        object_ids: List of object GUIDs (at least 2)
        delete_input: Delete input objects after operation
    
    Returns:
        Result with new object IDs
    """
    params = {
        "operation": "intersection",
        "object_ids": object_ids,
        "delete_input": delete_input
    }
    
    with RhinoClient() as client:
        return client.send_command("boolean_operation", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Boolean operations on solids')
    subparsers = parser.add_subparsers(dest='action', help='Boolean operation')
    
    # Union
    union_p = subparsers.add_parser('union', help='Boolean union')
    union_p.add_argument('ids', nargs='+', help='Object GUIDs to union')
    union_p.add_argument('--keep', '-k', action='store_true', help='Keep input objects')
    
    # Difference
    diff_p = subparsers.add_parser('difference', help='Boolean difference')
    diff_p.add_argument('ids', nargs='+', help='Object GUIDs (first - rest)')
    diff_p.add_argument('--keep', '-k', action='store_true', help='Keep input objects')
    
    # Intersection
    inter_p = subparsers.add_parser('intersection', help='Boolean intersection')
    inter_p.add_argument('ids', nargs='+', help='Object GUIDs to intersect')
    inter_p.add_argument('--keep', '-k', action='store_true', help='Keep input objects')
    
    args = parser.parse_args()
    
    if args.action == 'union':
        result = boolean_union(args.ids, delete_input=not args.keep)
    elif args.action == 'difference':
        result = boolean_difference(args.ids, delete_input=not args.keep)
    elif args.action == 'intersection':
        result = boolean_intersection(args.ids, delete_input=not args.keep)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
