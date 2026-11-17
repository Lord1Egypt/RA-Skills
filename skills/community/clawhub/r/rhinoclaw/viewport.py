#!/usr/bin/env python3
"""Viewport operations: views, camera, screenshots."""

import argparse
import json
import math
import sys
from pathlib import Path, PureWindowsPath
from typing import Optional
from rhino_client import RhinoClient, CONFIG


def set_view(view_name: str) -> dict:
    """Set viewport to a standard view.
    
    Args:
        view_name: One of 'Top', 'Bottom', 'Front', 'Back', 'Left', 'Right', 
                   'Perspective', 'TwoPointPerspective'
    """
    params = {"view_type": view_name}
    
    with RhinoClient() as client:
        return client.send_command("set_view", params)


def zoom_extents(viewport_name: str = "Perspective") -> dict:
    """Zoom to show all objects."""
    params = {"viewport_name": viewport_name}
    
    with RhinoClient() as client:
        return client.send_command("zoom_extents", params)


def zoom_selected(viewport_name: str = "Perspective") -> dict:
    """Zoom to show selected objects."""
    params = {"viewport_name": viewport_name}
    
    with RhinoClient() as client:
        return client.send_command("zoom_selected", params)


def orbit_camera(
    direction: str,
    angle_degrees: float = 15.0,
    viewport_name: Optional[str] = None,
) -> dict:
    """Orbit the camera around the target.

    Args:
        direction: One of ``right``, ``left``, ``up``, or ``down``.
        angle_degrees: Positive finite rotation angle in degrees.
        viewport_name: Optional localized name, GUID, or ``Layout::Detail``.
    """
    normalized_direction = direction.strip().lower() if isinstance(direction, str) else ""
    if normalized_direction not in {"right", "left", "up", "down"}:
        raise ValueError("direction must be 'right', 'left', 'up', or 'down'")
    if (
        isinstance(angle_degrees, bool)
        or not isinstance(angle_degrees, (int, float))
        or not math.isfinite(angle_degrees)
        or angle_degrees <= 0
    ):
        raise ValueError("angle_degrees must be a positive finite number")

    params = {
        "direction": normalized_direction,
        "angle_degrees": float(angle_degrees),
    }
    if viewport_name is not None and viewport_name.strip():
        params["viewport_name"] = viewport_name.strip()
    
    with RhinoClient() as client:
        return client.send_command("orbit_camera", params)


def set_camera(position: list, target: list, lens: float = 50.0, 
               viewport_name: str = "Perspective") -> dict:
    """Set camera position, target, and lens.
    
    Args:
        position: Camera position [x, y, z]
        target: Look-at target [x, y, z]
        lens: Lens length in mm (default: 50)
        viewport_name: Viewport to modify
    """
    params = {
        "camera_location": position,
        "target_location": target,
        "lens_length": lens,
        "viewport_name": viewport_name
    }
    
    with RhinoClient() as client:
        return client.send_command("set_camera", params)


def capture_viewport(viewport_name: str = "Perspective", width: int = 1920, 
                     height: int = 1080, filename: str = None) -> dict:
    """Capture viewport to image.
    
    Args:
        viewport_name: Viewport to capture
        width: Image width
        height: Image height
        filename: Output filename (auto-generated if not provided)
    
    Returns:
        Dict with 'linux_path' for reading and 'windows_path' sent to Rhino
    """
    import time
    
    # Get screenshot dirs from config
    screenshots_config = CONFIG.get("screenshots", {})
    linux_dir = screenshots_config.get("linux_dir", "/tmp")
    windows_dir = screenshots_config.get("windows_dir")
    
    # Generate filename if not provided
    if not filename:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
    
    # Build paths
    linux_path = str(Path(linux_dir) / filename)
    
    # Rhino is a Windows process: never send a POSIX fallback across TCP.
    # A configured drive/UNC root is also the explicit mapping that makes the
    # reported linux_path refer to the same file written by Rhino.
    if not isinstance(windows_dir, str) or not windows_dir.strip():
        raise ValueError(
            "screenshots.windows_dir must be configured as an absolute "
            "Windows or UNC path before capturing to a file"
        )
    windows_root = PureWindowsPath(windows_dir.strip())
    if not windows_root.is_absolute():
        raise ValueError(
            "screenshots.windows_dir must be an absolute Windows or UNC path"
        )
    windows_path = str(windows_root / filename)
    
    params = {
        "viewport_name": viewport_name,
        "width": width,
        "height": height,
        "filename": windows_path
    }
    
    with RhinoClient() as client:
        result = client.send_command("capture_viewport", params)
    
    # Add linux path for easy reading
    if result.get("status") == "success" or result.get("success"):
        payload = result.get("result", result)
        payload["linux_path"] = linux_path
        payload["windows_path"] = windows_path
    
    return result


def render_view(viewport_name: str = "Perspective", width: int = 1920,
                height: int = 1080, filename: str = None) -> dict:
    """Render viewport (with materials/lighting).
    
    Args:
        viewport_name: Viewport to render
        width: Render width
        height: Render height
        filename: Output filename (optional)
    """
    params = {
        "viewport_name": viewport_name,
        "width": width,
        "height": height
    }
    if filename:
        params["filename"] = filename
    
    with RhinoClient() as client:
        return client.send_command("render_view", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Viewport operations')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Set view
    view_p = subparsers.add_parser('view', help='Set standard view')
    view_p.add_argument('name', choices=['Top', 'Bottom', 'Front', 'Back', 
                                          'Left', 'Right', 'Perspective'],
                        help='View name')
    
    # Zoom extents
    zoom_p = subparsers.add_parser('zoom', help='Zoom extents')
    zoom_p.add_argument('--viewport', '-v', default='Perspective', help='Viewport name')
    zoom_p.add_argument('--selected', '-s', action='store_true', help='Zoom to selection')
    
    # Orbit
    orbit_p = subparsers.add_parser('orbit', help='Orbit camera')
    orbit_p.add_argument(
        'direction',
        choices=['right', 'left', 'up', 'down'],
        help='Orbit direction',
    )
    orbit_p.add_argument(
        '--angle', '-a',
        type=float,
        default=15.0,
        help='Positive rotation angle in degrees',
    )
    orbit_p.add_argument('--viewport', '-v', default=None, help='Viewport name or GUID')
    
    # Camera
    camera_p = subparsers.add_parser('camera', help='Set camera')
    camera_p.add_argument('--position', type=str, required=True, help='Position as x,y,z')
    camera_p.add_argument('--target', type=str, required=True, help='Target as x,y,z')
    camera_p.add_argument('--lens', type=float, default=50.0, help='Lens mm')
    camera_p.add_argument('--viewport', '-v', default='Perspective', help='Viewport name')
    
    # Screenshot
    screenshot_p = subparsers.add_parser('screenshot', help='Capture viewport')
    screenshot_p.add_argument('--viewport', '-v', default='Perspective', help='Viewport name')
    screenshot_p.add_argument('--width', '-W', type=int, default=1920, help='Width')
    screenshot_p.add_argument('--height', '-H', type=int, default=1080, help='Height')
    screenshot_p.add_argument('--output', '-o', type=str, help='Output filename')
    
    # Render
    render_p = subparsers.add_parser('render', help='Render viewport')
    render_p.add_argument('--viewport', '-v', default='Perspective', help='Viewport name')
    render_p.add_argument('--width', '-W', type=int, default=1920, help='Width')
    render_p.add_argument('--height', '-H', type=int, default=1080, help='Height')
    render_p.add_argument('--output', '-o', type=str, help='Output filename')
    
    args = parser.parse_args()
    
    def parse_point(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    if args.action == 'view':
        result = set_view(args.name)
    elif args.action == 'zoom':
        if args.selected:
            result = zoom_selected(args.viewport)
        else:
            result = zoom_extents(args.viewport)
    elif args.action == 'orbit':
        result = orbit_camera(args.direction, args.angle, args.viewport)
    elif args.action == 'camera':
        result = set_camera(
            parse_point(args.position),
            parse_point(args.target),
            args.lens,
            args.viewport
        )
    elif args.action == 'screenshot':
        result = capture_viewport(args.viewport, args.width, args.height, args.output)
    elif args.action == 'render':
        result = render_view(args.viewport, args.width, args.height, args.output)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
