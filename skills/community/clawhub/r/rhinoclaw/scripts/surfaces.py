#!/usr/bin/env python3
"""Surface operations: loft, extrude, revolve."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def loft_curves(curve_ids: list, loft_type: str = "normal", closed: bool = False) -> dict:
    """Create a surface by lofting through curves.
    
    Args:
        curve_ids: List of curve GUIDs to loft through
        loft_type: 'normal', 'loose', 'tight', 'straight', 'developable'
        closed: Whether to create a closed loft
    """
    params = {
        "curve_ids": curve_ids,
        "loft_type": loft_type,
        "closed": closed
    }
    
    with RhinoClient() as client:
        return client.send_command("loft_curves", params)


def extrude_curve(curve_id: str, direction: list, cap: bool = True) -> dict:
    """Extrude a curve along a direction vector.
    
    Args:
        curve_id: Curve GUID to extrude
        direction: Extrusion direction as [x, y, z] (length = extrusion distance)
        cap: Whether to cap the ends (creates solid if curve is closed)
    """
    params = {
        "curve_id": curve_id,
        "direction": direction,
        "cap": cap
    }
    
    with RhinoClient() as client:
        return client.send_command("extrude_curve", params)


def revolve_curve(curve_id: str, axis_start: list, axis_end: list, 
                  angle: float = 360.0) -> dict:
    """Revolve a curve around an axis.
    
    Args:
        curve_id: Curve GUID to revolve
        axis_start: Start point of rotation axis
        axis_end: End point of rotation axis
        angle: Rotation angle in degrees (default: 360 = full revolution)
    """
    params = {
        "curve_id": curve_id,
        "axis_start": axis_start,
        "axis_end": axis_end,
        "angle": angle
    }
    
    with RhinoClient() as client:
        return client.send_command("revolve_curve", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Surface operations')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Loft
    loft_p = subparsers.add_parser('loft', help='Loft through curves')
    loft_p.add_argument('curves', nargs='+', help='Curve GUIDs to loft through')
    loft_p.add_argument('--type', '-t', default='normal', 
                        choices=['normal', 'loose', 'tight', 'straight', 'developable'],
                        help='Loft type')
    loft_p.add_argument('--closed', action='store_true', help='Create closed loft')
    
    # Extrude
    extrude_p = subparsers.add_parser('extrude', help='Extrude a curve')
    extrude_p.add_argument('curve_id', help='Curve GUID')
    extrude_p.add_argument('--direction', '-d', type=str, required=True, 
                           help='Direction as x,y,z (length = distance)')
    extrude_p.add_argument('--no-cap', action='store_true', help='Do not cap the ends')
    
    # Revolve
    revolve_p = subparsers.add_parser('revolve', help='Revolve a curve')
    revolve_p.add_argument('curve_id', help='Curve GUID')
    revolve_p.add_argument('--axis-start', type=str, required=True, help='Axis start as x,y,z')
    revolve_p.add_argument('--axis-end', type=str, required=True, help='Axis end as x,y,z')
    revolve_p.add_argument('--angle', '-a', type=float, default=360.0, help='Angle in degrees')
    
    args = parser.parse_args()
    
    def parse_point(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    if args.action == 'loft':
        result = loft_curves(args.curves, args.type, args.closed)
    elif args.action == 'extrude':
        result = extrude_curve(args.curve_id, parse_point(args.direction), cap=not args.no_cap)
    elif args.action == 'revolve':
        result = revolve_curve(
            args.curve_id, 
            parse_point(args.axis_start),
            parse_point(args.axis_end),
            args.angle
        )
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
