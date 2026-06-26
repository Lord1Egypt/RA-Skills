#!/usr/bin/env python3
"""Text and annotation operations."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def create_text(text: str, position: list = None, height: float = 1.0,
                font: str = "Arial", bold: bool = False, italic: bool = False,
                normal: list = None, name: str = None, color: list = None) -> dict:
    """Create annotation text.
    
    Args:
        text: Text content
        position: Position [x, y, z]
        height: Text height
        font: Font name
        bold: Bold text
        italic: Italic text
        normal: Plane normal [x, y, z] (default: Z-up)
        name: Object name
        color: Color [r, g, b]
    """
    params = {
        "text": text,
        "height": height,
        "font": font,
        "bold": bold,
        "italic": italic
    }
    if position:
        params["position"] = position
    if normal:
        params["normal"] = normal
    if name:
        params["name"] = name
    if color:
        params["color"] = color
    
    with RhinoClient() as client:
        return client.send_command("create_text", params)


def create_3d_text(text: str, position: list = None, height: float = 1.0,
                   depth: float = None, font: str = "Arial", bold: bool = False,
                   name: str = None, color: list = None) -> dict:
    """Create extruded 3D text.
    
    Args:
        text: Text content
        position: Position [x, y, z]
        height: Text height
        depth: Extrusion depth (default: 20% of height)
        font: Font name
        bold: Bold text
        name: Object name
        color: Color [r, g, b]
    """
    params = {
        "text": text,
        "height": height,
        "font": font,
        "bold": bold
    }
    if position:
        params["position"] = position
    if depth is not None:
        params["depth"] = depth
    if name:
        params["name"] = name
    if color:
        params["color"] = color
    
    with RhinoClient() as client:
        return client.send_command("create_3d_text", params)


def create_text_dot(text: str, position: list = None, secondary_text: str = None,
                    font_height: int = 14, name: str = None) -> dict:
    """Create a text dot (screen-oriented label).
    
    Args:
        text: Primary text
        position: Position [x, y, z]
        secondary_text: Secondary text (shown on hover)
        font_height: Font height in pixels
        name: Object name
    """
    params = {
        "text": text,
        "font_height": font_height
    }
    if position:
        params["position"] = position
    if secondary_text:
        params["secondary_text"] = secondary_text
    if name:
        params["name"] = name
    
    with RhinoClient() as client:
        return client.send_command("create_text_dot", params)


def create_leader(text: str, points: list, name: str = None) -> dict:
    """Create a leader (annotation arrow with text).
    
    Args:
        text: Leader text
        points: List of points [[x,y,z], [x,y,z], ...] - arrow tip first
        name: Object name
    """
    params = {
        "text": text,
        "points": points
    }
    if name:
        params["name"] = name
    
    with RhinoClient() as client:
        return client.send_command("create_leader", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text and annotation operations')
    subparsers = parser.add_subparsers(dest='action', help='Operation')
    
    # Annotation text
    text_p = subparsers.add_parser('text', help='Create annotation text')
    text_p.add_argument('content', help='Text content')
    text_p.add_argument('--position', '-p', type=str, default='0,0,0', help='x,y,z')
    text_p.add_argument('--height', '-H', type=float, default=1.0, help='Text height')
    text_p.add_argument('--font', '-f', type=str, default='Arial', help='Font name')
    text_p.add_argument('--bold', '-b', action='store_true', help='Bold')
    text_p.add_argument('--italic', '-i', action='store_true', help='Italic')
    text_p.add_argument('--name', '-n', type=str, help='Object name')
    text_p.add_argument('--color', '-c', type=str, help='r,g,b')
    
    # 3D text
    text3d_p = subparsers.add_parser('3d', help='Create extruded 3D text')
    text3d_p.add_argument('content', help='Text content')
    text3d_p.add_argument('--position', '-p', type=str, default='0,0,0', help='x,y,z')
    text3d_p.add_argument('--height', '-H', type=float, default=5.0, help='Text height')
    text3d_p.add_argument('--depth', '-d', type=float, help='Extrusion depth')
    text3d_p.add_argument('--font', '-f', type=str, default='Arial', help='Font name')
    text3d_p.add_argument('--bold', '-b', action='store_true', help='Bold')
    text3d_p.add_argument('--name', '-n', type=str, help='Object name')
    text3d_p.add_argument('--color', '-c', type=str, help='r,g,b')
    
    # Text dot
    dot_p = subparsers.add_parser('dot', help='Create text dot (label)')
    dot_p.add_argument('content', help='Text content')
    dot_p.add_argument('--position', '-p', type=str, default='0,0,0', help='x,y,z')
    dot_p.add_argument('--secondary', '-s', type=str, help='Secondary text')
    dot_p.add_argument('--size', type=int, default=14, help='Font height')
    dot_p.add_argument('--name', '-n', type=str, help='Object name')
    
    # Leader
    leader_p = subparsers.add_parser('leader', help='Create leader annotation')
    leader_p.add_argument('content', help='Text content')
    leader_p.add_argument('--points', required=True, type=str, 
                          help='Points as "x,y,z;x,y,z;..."')
    leader_p.add_argument('--name', '-n', type=str, help='Object name')
    
    args = parser.parse_args()
    
    def parse_point(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    def parse_points(s: str) -> list:
        return [parse_point(p) for p in s.split(';')]
    
    def parse_color(s: str) -> list:
        return [int(x) for x in s.split(',')]
    
    if args.action == 'text':
        result = create_text(
            args.content,
            position=parse_point(args.position),
            height=args.height,
            font=args.font,
            bold=args.bold,
            italic=args.italic,
            name=args.name,
            color=parse_color(args.color) if args.color else None
        )
    elif args.action == '3d':
        result = create_3d_text(
            args.content,
            position=parse_point(args.position),
            height=args.height,
            depth=args.depth,
            font=args.font,
            bold=args.bold,
            name=args.name,
            color=parse_color(args.color) if args.color else None
        )
    elif args.action == 'dot':
        result = create_text_dot(
            args.content,
            position=parse_point(args.position),
            secondary_text=args.secondary,
            font_height=args.size,
            name=args.name
        )
    elif args.action == 'leader':
        result = create_leader(
            args.content,
            points=parse_points(args.points),
            name=args.name
        )
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
