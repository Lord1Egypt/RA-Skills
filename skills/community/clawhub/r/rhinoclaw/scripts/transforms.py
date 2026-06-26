#!/usr/bin/env python3
"""Transform operations: copy, mirror, array."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def copy_object(object_id: str, offset: list = None) -> dict:
    """Copy an object with optional offset."""
    params = {"object_id": object_id}
    if offset:
        params["offset"] = offset
    
    with RhinoClient() as client:
        return client.send_command("copy_object", params)


def mirror_object(object_id: str, plane_origin: list, plane_normal: list, copy: bool = True) -> dict:
    """Mirror an object across a plane."""
    params = {
        "object_id": object_id,
        "plane_origin": plane_origin,
        "plane_normal": plane_normal,
        "copy": copy
    }
    
    with RhinoClient() as client:
        return client.send_command("mirror_object", params)


def array_linear(object_id: str, direction: list, count: int, distance: float = None) -> dict:
    """Create a linear array of objects."""
    params = {
        "object_id": object_id,
        "direction": direction,
        "count": count
    }
    if distance is not None:
        params["distance"] = distance
    
    with RhinoClient() as client:
        return client.send_command("array_linear", params)


def array_polar(object_id: str, center: list, axis: list, count: int, angle: float = 360.0) -> dict:
    """Create a polar/radial array of objects."""
    params = {
        "object_id": object_id,
        "center": center,
        "axis": axis,
        "count": count,
        "angle": angle
    }
    
    with RhinoClient() as client:
        return client.send_command("array_polar", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform operations')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Copy
    copy_p = subparsers.add_parser('copy', help='Copy an object')
    copy_p.add_argument('object_id', help='Object GUID')
    copy_p.add_argument('--offset', type=str, help='Offset as x,y,z')
    
    # Mirror
    mirror_p = subparsers.add_parser('mirror', help='Mirror an object')
    mirror_p.add_argument('object_id', help='Object GUID')
    mirror_p.add_argument('--origin', type=str, required=True, help='Plane origin as x,y,z')
    mirror_p.add_argument('--normal', type=str, required=True, help='Plane normal as x,y,z')
    mirror_p.add_argument('--no-copy', action='store_true', help='Move instead of copy')
    
    # Linear array
    linear_p = subparsers.add_parser('linear', help='Linear array')
    linear_p.add_argument('object_id', help='Object GUID')
    linear_p.add_argument('--direction', type=str, required=True, help='Direction as x,y,z')
    linear_p.add_argument('--count', type=int, required=True, help='Number of copies')
    linear_p.add_argument('--distance', type=float, help='Distance between copies')
    
    # Polar array
    polar_p = subparsers.add_parser('polar', help='Polar array')
    polar_p.add_argument('object_id', help='Object GUID')
    polar_p.add_argument('--center', type=str, required=True, help='Center point as x,y,z')
    polar_p.add_argument('--axis', type=str, default='0,0,1', help='Rotation axis as x,y,z')
    polar_p.add_argument('--count', type=int, required=True, help='Number of copies')
    polar_p.add_argument('--angle', type=float, default=360.0, help='Total angle in degrees')
    
    args = parser.parse_args()
    
    def parse_point(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    if args.action == 'copy':
        offset = parse_point(args.offset) if args.offset else None
        result = copy_object(args.object_id, offset)
    elif args.action == 'mirror':
        result = mirror_object(
            args.object_id,
            parse_point(args.origin),
            parse_point(args.normal),
            copy=not args.no_copy
        )
    elif args.action == 'linear':
        result = array_linear(
            args.object_id,
            parse_point(args.direction),
            args.count,
            args.distance
        )
    elif args.action == 'polar':
        result = array_polar(
            args.object_id,
            parse_point(args.center),
            parse_point(args.axis),
            args.count,
            args.angle
        )
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
