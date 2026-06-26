#!/usr/bin/env python3
"""Render operations: lights, render settings, render to image."""

import argparse
import json
import sys
from pathlib import Path
from rhino_client import RhinoClient, CONFIG


def set_render_settings(width: int = None, height: int = None,
                        quality: str = None, background_color: list = None) -> dict:
    """Set render settings.
    
    Args:
        width: Render width in pixels
        height: Render height in pixels
        quality: Render quality ('draft', 'low', 'medium', 'high', 'final')
        background_color: Background color [r, g, b]
    """
    params = {}
    if width:
        params["width"] = width
    if height:
        params["height"] = height
    if quality:
        params["quality"] = quality
    if background_color:
        params["background_color"] = background_color
    
    with RhinoClient() as client:
        return client.send_command("set_render_settings", params)


def add_light(light_type: str, location: list = None, direction: list = None,
              target: list = None, color: list = None, intensity: float = None,
              name: str = None, spot_angle: float = None) -> dict:
    """Add a light to the scene.
    
    Args:
        light_type: 'point', 'directional', 'spot', 'rectangular', 'linear'
        location: Light position [x, y, z] (for point, spot)
        direction: Light direction [x, y, z] (for directional)
        target: Light target point [x, y, z] (for spot)
        color: Light color [r, g, b]
        intensity: Light intensity (0.0 - 1.0+)
        name: Light name
        spot_angle: Spot light angle in degrees (default: 45)
    """
    params = {"light_type": light_type}
    
    if location:
        params["location"] = location
    if direction:
        params["direction"] = direction
    if target:
        params["target"] = target
    if color:
        params["color"] = color
    if intensity is not None:
        params["intensity"] = intensity
    if name:
        params["name"] = name
    if spot_angle is not None:
        params["spot_angle_degrees"] = spot_angle
    
    with RhinoClient() as client:
        return client.send_command("add_light", params)


def set_camera(camera_location: list, target_location: list = None, 
               lens_length: float = None, viewport_name: str = "Perspective") -> dict:
    """Set camera position and target.
    
    Args:
        camera_location: Camera position [x, y, z]
        target_location: Look-at target [x, y, z] (optional)
        lens_length: Lens length in mm (optional)
        viewport_name: Viewport to modify
    """
    params = {
        "camera_location": camera_location,
        "viewport_name": viewport_name
    }
    if target_location:
        params["target_location"] = target_location
    if lens_length:
        params["lens_length"] = lens_length
    
    with RhinoClient() as client:
        return client.send_command("set_camera", params)


def render_view(viewport_name: str = "Perspective", width: int = 1920,
                height: int = 1080, filename: str = None) -> dict:
    """Render the viewport to an image.
    
    Args:
        viewport_name: Viewport to render
        width: Render width
        height: Render height
        filename: Output filename (optional, returns base64 if not provided)
    """
    # Validate dimensions to prevent GDI+ errors
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid dimensions: {width}x{height} (must be positive)")
    
    if width > 4096 or height > 4096:
        raise ValueError(f"Dimensions too large: {width}x{height} (max: 4096x4096)")
    
    # Get screenshot dir from config
    screenshots_config = CONFIG.get("screenshots", {})
    output_dir = screenshots_config.get("output_dir")
    
    # If filename is relative and we have output_dir, make it absolute
    if filename and output_dir and not Path(filename).is_absolute():
        filename = str(Path(output_dir) / filename)
    
    # Ensure output directory exists and is writable
    if filename:
        try:
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Test write access if file exists
            if output_path.exists():
                output_path.touch()  # This will fail if file is locked
                
        except OSError as e:
            raise ValueError(f"Cannot write to {filename}: {e}")
    
    params = {
        "viewport_name": viewport_name,
        "width": width,
        "height": height
    }
    if filename:
        params["filename"] = filename
    
    with RhinoClient() as client:
        return client.send_command("render_view", params)


def add_point_light(location: list, color: list = None, intensity: float = 1.0,
                    name: str = None) -> dict:
    """Add a point light (convenience function)."""
    return add_light("point", location=location, color=color, 
                     intensity=intensity, name=name)


def add_directional_light(direction: list, color: list = None, 
                          intensity: float = 1.0, name: str = None) -> dict:
    """Add a directional light (sun-like)."""
    return add_light("directional", direction=direction, color=color,
                     intensity=intensity, name=name)


def add_spot_light(location: list, target: list, color: list = None,
                   intensity: float = 1.0, name: str = None) -> dict:
    """Add a spot light."""
    return add_light("spot", location=location, target=target, color=color,
                     intensity=intensity, name=name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Render operations')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Render settings
    settings_p = subparsers.add_parser('settings', help='Set render settings')
    settings_p.add_argument('--width', '-W', type=int, help='Render width')
    settings_p.add_argument('--height', '-H', type=int, help='Render height')
    settings_p.add_argument('--quality', '-q', 
                            choices=['draft', 'low', 'medium', 'high', 'final'],
                            help='Render quality')
    settings_p.add_argument('--background', type=str, help='Background color as r,g,b')
    
    # Add light
    light_p = subparsers.add_parser('light', help='Add a light')
    light_p.add_argument('type', choices=['point', 'directional', 'spot'],
                         help='Light type')
    light_p.add_argument('--location', '-l', type=str, help='Location as x,y,z (point/spot)')
    light_p.add_argument('--direction', '-d', type=str, help='Direction as x,y,z (directional)')
    light_p.add_argument('--target', '-t', type=str, help='Target as x,y,z (spot)')
    light_p.add_argument('--color', '-c', type=str, help='Color as r,g,b')
    light_p.add_argument('--intensity', '-i', type=float, default=1.0, help='Intensity')
    light_p.add_argument('--name', '-n', type=str, help='Light name')
    light_p.add_argument('--spot-angle', type=float, help='Spot angle degrees')
    
    # Camera
    camera_p = subparsers.add_parser('camera', help='Set camera')
    camera_p.add_argument('--location', '-l', type=str, required=True, help='Camera location as x,y,z')
    camera_p.add_argument('--target', '-t', type=str, help='Target as x,y,z')
    camera_p.add_argument('--lens', type=float, help='Lens length mm')
    camera_p.add_argument('--viewport', '-v', default='Perspective', help='Viewport name')
    
    # Render
    render_p = subparsers.add_parser('render', help='Render viewport')
    render_p.add_argument('--viewport', '-v', default='Perspective', help='Viewport name')
    render_p.add_argument('--width', '-W', type=int, default=1920, help='Width')
    render_p.add_argument('--height', '-H', type=int, default=1080, help='Height')
    render_p.add_argument('--output', '-o', type=str, help='Output filename')
    
    args = parser.parse_args()
    
    def parse_point(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    def parse_color(s: str) -> list:
        return [int(x) for x in s.split(',')]
    
    if args.action == 'settings':
        bg_color = parse_color(args.background) if args.background else None
        result = set_render_settings(
            width=args.width,
            height=args.height,
            quality=args.quality,
            background_color=bg_color
        )
    elif args.action == 'light':
        location = parse_point(args.location) if args.location else None
        direction = parse_point(args.direction) if args.direction else None
        target = parse_point(args.target) if args.target else None
        color = parse_color(args.color) if args.color else None
        result = add_light(
            args.type,
            location=location,
            direction=direction,
            target=target,
            color=color,
            intensity=args.intensity,
            name=args.name,
            spot_angle=args.spot_angle
        )
    elif args.action == 'camera':
        target = parse_point(args.target) if args.target else None
        result = set_camera(
            parse_point(args.location),
            target,
            args.lens,
            args.viewport
        )
    elif args.action == 'render':
        result = render_view(
            args.viewport,
            args.width,
            args.height,
            args.output
        )
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
