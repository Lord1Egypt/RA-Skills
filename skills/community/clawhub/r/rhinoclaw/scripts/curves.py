#!/usr/bin/env python3
"""Curve operations: offset, fillet, chamfer."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def offset_curve(curve_id: str, distance: float, direction: list = None) -> dict:
    """Offset a curve by a distance.
    
    Args:
        curve_id: Curve GUID
        distance: Offset distance (positive = right, negative = left)
        direction: Optional direction point to determine offset side
    """
    params = {
        "curve_id": curve_id,
        "distance": distance
    }
    if direction:
        params["direction"] = direction
    
    with RhinoClient() as client:
        return client.send_command("offset_curve", params)


def fillet_curves(curve_id1: str, curve_id2: str, radius: float, 
                  point1: list = None, point2: list = None) -> dict:
    """Create a fillet arc between two curves.
    
    Args:
        curve_id1: First curve GUID
        curve_id2: Second curve GUID
        radius: Fillet radius
        point1: Optional point on first curve near fillet
        point2: Optional point on second curve near fillet
    """
    params = {
        "curve_id_1": curve_id1,
        "curve_id_2": curve_id2,
        "radius": radius
    }
    if point1:
        params["point_1"] = point1
    if point2:
        params["point_2"] = point2
    
    with RhinoClient() as client:
        return client.send_command("fillet_curves", params)


def chamfer_curves(curve_id1: str, curve_id2: str, distance1: float, 
                   distance2: float = None, point1: list = None, point2: list = None) -> dict:
    """Create a chamfer between two curves.
    
    Args:
        curve_id1: First curve GUID
        curve_id2: Second curve GUID
        distance1: Chamfer distance on first curve
        distance2: Chamfer distance on second curve (defaults to distance1)
        point1: Optional point on first curve near chamfer
        point2: Optional point on second curve near chamfer
    """
    params = {
        "curve_id_1": curve_id1,
        "curve_id_2": curve_id2,
        "distance_1": distance1,
        "distance_2": distance2 if distance2 is not None else distance1
    }
    if point1:
        params["point_1"] = point1
    if point2:
        params["point_2"] = point2
    
    with RhinoClient() as client:
        return client.send_command("chamfer_curves", params)


def join_curves(curve_ids: list, delete_input: bool = True) -> dict:
    """Join multiple curves into polycurves.
    
    Args:
        curve_ids: List of curve GUIDs to join
        delete_input: Delete original curves after joining
    
    Returns:
        Result with joined curve IDs
    """
    params = {
        "curve_ids": curve_ids,
        "delete_input": delete_input
    }
    
    with RhinoClient() as client:
        return client.send_command("join_curves", params)


def explode_curve(curve_id: str, delete_input: bool = True) -> dict:
    """Explode a polycurve into segments.
    
    Args:
        curve_id: Polycurve GUID to explode
        delete_input: Delete original curve after exploding
    
    Returns:
        Result with segment curve IDs
    """
    params = {
        "curve_id": curve_id,
        "delete_input": delete_input
    }
    
    with RhinoClient() as client:
        return client.send_command("explode_curve", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Curve operations')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Offset
    offset_p = subparsers.add_parser('offset', help='Offset a curve')
    offset_p.add_argument('curve_id', help='Curve GUID')
    offset_p.add_argument('--distance', '-d', type=float, required=True, help='Offset distance')
    offset_p.add_argument('--direction', type=str, help='Direction point as x,y,z')
    
    # Fillet
    fillet_p = subparsers.add_parser('fillet', help='Fillet two curves')
    fillet_p.add_argument('curve1', help='First curve GUID')
    fillet_p.add_argument('curve2', help='Second curve GUID')
    fillet_p.add_argument('--radius', '-r', type=float, required=True, help='Fillet radius')
    fillet_p.add_argument('--point1', type=str, help='Point on curve 1 as x,y,z')
    fillet_p.add_argument('--point2', type=str, help='Point on curve 2 as x,y,z')
    
    # Chamfer
    chamfer_p = subparsers.add_parser('chamfer', help='Chamfer two curves')
    chamfer_p.add_argument('curve1', help='First curve GUID')
    chamfer_p.add_argument('curve2', help='Second curve GUID')
    chamfer_p.add_argument('--distance', '-d', type=float, required=True, help='Chamfer distance')
    chamfer_p.add_argument('--distance2', type=float, help='Distance on second curve')
    chamfer_p.add_argument('--point1', type=str, help='Point on curve 1 as x,y,z')
    chamfer_p.add_argument('--point2', type=str, help='Point on curve 2 as x,y,z')
    
    # Join
    join_p = subparsers.add_parser('join', help='Join curves into polycurves')
    join_p.add_argument('curve_ids', nargs='+', help='Curve GUIDs to join')
    join_p.add_argument('--keep', '-k', action='store_true', help='Keep input curves')
    
    # Explode
    explode_p = subparsers.add_parser('explode', help='Explode polycurve into segments')
    explode_p.add_argument('curve_id', help='Polycurve GUID')
    explode_p.add_argument('--keep', '-k', action='store_true', help='Keep input curve')
    
    args = parser.parse_args()
    
    def parse_point(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    if args.action == 'offset':
        direction = parse_point(args.direction) if args.direction else None
        result = offset_curve(args.curve_id, args.distance, direction)
    elif args.action == 'fillet':
        point1 = parse_point(args.point1) if args.point1 else None
        point2 = parse_point(args.point2) if args.point2 else None
        result = fillet_curves(args.curve1, args.curve2, args.radius, point1, point2)
    elif args.action == 'chamfer':
        point1 = parse_point(args.point1) if args.point1 else None
        point2 = parse_point(args.point2) if args.point2 else None
        result = chamfer_curves(args.curve1, args.curve2, args.distance, args.distance2, point1, point2)
    elif args.action == 'join':
        result = join_curves(args.curve_ids, delete_input=not args.keep)
    elif args.action == 'explode':
        result = explode_curve(args.curve_id, delete_input=not args.keep)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
