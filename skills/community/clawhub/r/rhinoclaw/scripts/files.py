#!/usr/bin/env python3
"""File operations: open, save, import, export."""

import argparse
import json
import sys
from pathlib import Path
from rhino_client import RhinoClient


def open_file(file_path: str) -> dict:
    """Open a Rhino 3DM file.
    
    Args:
        file_path: Path to .3dm file
    """
    params = {"file_path": file_path}
    
    with RhinoClient() as client:
        return client.send_command("open_file", params)


def save_file(file_path: str = None) -> dict:
    """Save the current document.
    
    Args:
        file_path: Optional path for Save As (must be .3dm)
    """
    params = {}
    if file_path:
        params["file_path"] = file_path
    
    with RhinoClient() as client:
        return client.send_command("save_file", params)


def export_file(file_path: str, format: str = None, object_ids: list = None) -> dict:
    """Export geometry to various formats.
    
    Args:
        file_path: Output file path
        format: Export format (auto-detected from extension if not specified)
                Supported: STEP, IGES, OBJ, STL, DXF, DWG, 3DS, FBX, DAE
        object_ids: Optional list of object GUIDs to export (all if not specified)
    """
    params = {"file_path": file_path}
    
    if format:
        params["format"] = format.upper()
    
    if object_ids:
        params["object_ids"] = object_ids
    
    with RhinoClient() as client:
        return client.send_command("export_file", params)


def import_mesh(file_path: str) -> dict:
    """Import a mesh file (OBJ, STL, etc.).
    
    Args:
        file_path: Path to mesh file
    """
    params = {"file_path": file_path}
    
    with RhinoClient() as client:
        return client.send_command("import_mesh", params)


def export_mesh(file_path: str, object_ids: list = None, format: str = None) -> dict:
    """Export meshes to file.
    
    Args:
        file_path: Output file path
        object_ids: Mesh GUIDs to export (all meshes if not specified)
        format: OBJ, STL, PLY, etc.
    """
    params = {"file_path": file_path}
    
    if object_ids:
        params["object_ids"] = object_ids
    if format:
        params["format"] = format.upper()
    
    with RhinoClient() as client:
        return client.send_command("export_mesh", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File operations')
    subparsers = parser.add_subparsers(dest='action', help='File operation')
    
    # Open
    open_p = subparsers.add_parser('open', help='Open a .3dm file')
    open_p.add_argument('path', help='File path')
    
    # Save
    save_p = subparsers.add_parser('save', help='Save current document')
    save_p.add_argument('--path', '-p', help='Optional new path (Save As)')
    
    # Export
    export_p = subparsers.add_parser('export', help='Export to various formats')
    export_p.add_argument('path', help='Output file path')
    export_p.add_argument('--format', '-f', 
                          choices=['step', 'iges', 'obj', 'stl', 'dxf', 'dwg', '3ds', 'fbx', 'dae'],
                          help='Export format (auto-detected from extension)')
    export_p.add_argument('--ids', nargs='+', help='Object GUIDs to export')
    
    # Import mesh
    import_p = subparsers.add_parser('import', help='Import mesh file')
    import_p.add_argument('path', help='File path')
    
    # Export mesh
    mesh_export_p = subparsers.add_parser('mesh-export', help='Export meshes')
    mesh_export_p.add_argument('path', help='Output file path')
    mesh_export_p.add_argument('--format', '-f', choices=['obj', 'stl', 'ply'], help='Format')
    mesh_export_p.add_argument('--ids', nargs='+', help='Mesh GUIDs to export')
    
    args = parser.parse_args()
    
    if args.action == 'open':
        result = open_file(args.path)
    elif args.action == 'save':
        result = save_file(args.path)
    elif args.action == 'export':
        result = export_file(args.path, args.format, args.ids)
    elif args.action == 'import':
        result = import_mesh(args.path)
    elif args.action == 'mesh-export':
        result = export_mesh(args.path, args.ids, args.format)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
