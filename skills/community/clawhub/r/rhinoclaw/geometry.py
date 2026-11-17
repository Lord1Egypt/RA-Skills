#!/usr/bin/env python3
"""
Create geometry objects in Rhino via RhinoClaw.
"""

import argparse
import json
import sys
from rhino_client import RhinoClient
from utils import parse_coords as _parse_coords, parse_color as _parse_color

GEOMETRY_TYPES = [
    'POINT', 'LINE', 'POLYLINE', 'CIRCLE', 'ARC', 'ELLIPSE', 
    'CURVE', 'BOX', 'SPHERE', 'CONE', 'CYLINDER', 'SURFACE', 'MESH'
]


def create_object(obj_type: str, params: dict, name: str = None, 
                  color: list = None, layer: str = None, 
                  translation: list = None) -> dict:
    """Create a single geometry object."""
    cmd_params = {
        "type": obj_type.upper(),
        "params": params
    }
    if name:
        cmd_params["name"] = name
    if color:
        cmd_params["color"] = color
    if layer:
        cmd_params["layer"] = layer
    if translation:
        cmd_params["translation"] = translation
    
    with RhinoClient() as client:
        return client.send_command("create_object", cmd_params)


def create_objects(objects: list) -> dict:
    """Create multiple geometry objects (batch)."""
    with RhinoClient() as client:
        return client.send_command("create_objects", {"objects": objects})


def main():
    parser = argparse.ArgumentParser(description='Create Rhino geometry')
    subparsers = parser.add_subparsers(dest='geometry', required=True)
    
    # Sphere
    sp = subparsers.add_parser('sphere', help='Create a sphere')
    sp.add_argument('--radius', '-r', type=float, default=1.0)
    sp.add_argument('--name', '-n', type=str)
    sp.add_argument('--position', '-pos', type=str, default='0,0,0', help='x,y,z')
    sp.add_argument('--color', '-c', type=str, help='r,g,b')
    sp.add_argument('--layer', '-l', type=str)
    
    # Box
    bp = subparsers.add_parser('box', help='Create a box')
    bp.add_argument('--width', '-w', type=float, default=1.0)
    bp.add_argument('--length', '-len', type=float, default=1.0)
    bp.add_argument('--height', '-ht', type=float, default=1.0)
    bp.add_argument('--name', '-n', type=str)
    bp.add_argument('--position', '-pos', type=str, default='0,0,0')
    bp.add_argument('--color', '-c', type=str)
    bp.add_argument('--layer', '-l', type=str)
    
    # Cylinder
    cp = subparsers.add_parser('cylinder', help='Create a cylinder')
    cp.add_argument('--radius', '-r', type=float, default=1.0)
    cp.add_argument('--height', '-ht', type=float, default=2.0)
    cp.add_argument('--no-cap', action='store_true', help='Create open cylinder (default: capped)')
    cp.add_argument('--name', '-n', type=str)
    cp.add_argument('--position', '-pos', type=str, default='0,0,0')
    cp.add_argument('--color', '-c', type=str)
    cp.add_argument('--layer', '-l', type=str)
    
    # Cone
    conep = subparsers.add_parser('cone', help='Create a cone')
    conep.add_argument('--radius', '-r', type=float, default=1.0)
    conep.add_argument('--height', '-ht', type=float, default=2.0)
    conep.add_argument('--no-cap', action='store_true', help='Create open cone (default: capped)')
    conep.add_argument('--name', '-n', type=str)
    conep.add_argument('--position', '-pos', type=str, default='0,0,0')
    conep.add_argument('--color', '-c', type=str)
    conep.add_argument('--layer', '-l', type=str)
    
    # Point
    pp = subparsers.add_parser('point', help='Create a point')
    pp.add_argument('--position', '-pos', type=str, default='0,0,0')
    pp.add_argument('--name', '-n', type=str)
    pp.add_argument('--layer', '-l', type=str)
    
    # Line
    lp = subparsers.add_parser('line', help='Create a line')
    lp.add_argument('--start', '-s', type=str, required=True, help='x,y,z')
    lp.add_argument('--end', '-e', type=str, required=True, help='x,y,z')
    lp.add_argument('--name', '-n', type=str)
    lp.add_argument('--color', '-c', type=str)
    lp.add_argument('--layer', '-l', type=str)
    
    # Circle
    circp = subparsers.add_parser('circle', help='Create a circle')
    circp.add_argument('--radius', '-r', type=float, default=1.0)
    circp.add_argument('--name', '-n', type=str)
    circp.add_argument('--position', '-pos', type=str, default='0,0,0')
    circp.add_argument('--color', '-c', type=str)
    circp.add_argument('--layer', '-l', type=str)
    
    # Raw JSON
    rawp = subparsers.add_parser('raw', help='Create from raw JSON')
    rawp.add_argument('--type', '-t', type=str, required=True, choices=GEOMETRY_TYPES)
    rawp.add_argument('--params', '-p', type=str, required=True, help='JSON params')
    rawp.add_argument('--name', '-n', type=str)
    rawp.add_argument('--position', '-pos', type=str)
    rawp.add_argument('--color', '-c', type=str)
    rawp.add_argument('--layer', '-l', type=str)
    
    args = parser.parse_args()
    
    # Parse common arguments
    def parse_coords(s):
        return [float(x) for x in s.split(',')] if s else None
    
    position = parse_coords(getattr(args, 'position', None))
    color = parse_coords(getattr(args, 'color', None))
    name = getattr(args, 'name', None)
    layer = getattr(args, 'layer', None)
    
    # Build params based on geometry type
    if args.geometry == 'sphere':
        params = {"radius": args.radius}
        obj_type = "SPHERE"
    elif args.geometry == 'box':
        params = {"width": args.width, "length": args.length, "height": args.height}
        obj_type = "BOX"
    elif args.geometry == 'cylinder':
        params = {"radius": args.radius, "height": args.height, "cap": not getattr(args, 'no_cap', False)}
        obj_type = "CYLINDER"
    elif args.geometry == 'cone':
        params = {"radius": args.radius, "height": args.height, "cap": not getattr(args, 'no_cap', False)}
        obj_type = "CONE"
    elif args.geometry == 'point':
        params = {"location": position or [0, 0, 0]}
        obj_type = "POINT"
        position = None  # Already in params
    elif args.geometry == 'line':
        params = {
            "start": parse_coords(args.start),
            "end": parse_coords(args.end)
        }
        obj_type = "LINE"
    elif args.geometry == 'circle':
        params = {"radius": args.radius}
        obj_type = "CIRCLE"
    elif args.geometry == 'raw':
        params = json.loads(args.params)
        obj_type = args.type
    else:
        print(f"Unknown geometry type: {args.geometry}", file=sys.stderr)
        sys.exit(1)
    
    # Create the object
    result = create_object(
        obj_type=obj_type,
        params=params,
        name=name,
        color=[int(c) for c in color] if color else None,
        layer=layer,
        translation=position
    )
    
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
