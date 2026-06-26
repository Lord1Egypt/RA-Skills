#!/usr/bin/env python3
"""
Material management for Rhino via RhinoClaw.
Supports both legacy custom materials and PBR materials.
"""

import argparse
import json
import sys
from rhino_client import RhinoClient


def create_material(name: str, color: list, shine: float = None,
                    material_type: str = None, metallic: float = None, 
                    roughness: float = None) -> dict:
    """
    Create a material.
    
    For legacy materials: use shine (0.0-1.0)
    For PBR materials: use material_type='pbr', metallic (0.0-1.0), roughness (0.0-1.0)
    """
    params = {
        "name": name,
        "color": color
    }
    
    if material_type == 'pbr':
        params["material_type"] = "pbr"
        if metallic is not None:
            params["metallic"] = metallic
        if roughness is not None:
            params["roughness"] = roughness
    elif shine is not None:
        params["shine"] = shine
    
    with RhinoClient() as client:
        return client.send_command("create_material", params)


def assign_material_to_layer(layer_name: str, material_id: str) -> dict:
    """Assign a material to a layer."""
    with RhinoClient() as client:
        return client.send_command("assign_material_to_layer", {
            "layer_name": layer_name,
            "material_id": material_id
        })


def main():
    parser = argparse.ArgumentParser(description='Rhino material management')
    subparsers = parser.add_subparsers(dest='action', required=True)
    
    # Create legacy material
    cp = subparsers.add_parser('create', help='Create a legacy material')
    cp.add_argument('name', type=str)
    cp.add_argument('--color', '-c', type=str, required=True, help='r,g,b')
    cp.add_argument('--shine', '-s', type=float, default=0.5, help='0.0-1.0')
    
    # Create PBR material
    pbr = subparsers.add_parser('pbr', help='Create a PBR material')
    pbr.add_argument('name', type=str)
    pbr.add_argument('--color', '-c', type=str, required=True, help='r,g,b')
    pbr.add_argument('--metallic', '-m', type=float, default=0.9, help='0.0-1.0')
    pbr.add_argument('--roughness', '-r', type=float, default=0.1, help='0.0-1.0')
    
    # Assign to layer
    ap = subparsers.add_parser('assign', help='Assign material to layer')
    ap.add_argument('layer_name', type=str)
    ap.add_argument('material_id', type=str)
    
    # Presets
    presets = subparsers.add_parser('preset', help='Create preset PBR material')
    presets.add_argument('preset', choices=['gold', 'silver', 'platinum', 'copper', 'bronze'])
    
    args = parser.parse_args()
    
    def parse_color(s):
        return [int(x) for x in s.split(',')]
    
    if args.action == 'create':
        result = create_material(
            name=args.name,
            color=parse_color(args.color),
            shine=args.shine
        )
    elif args.action == 'pbr':
        result = create_material(
            name=args.name,
            color=parse_color(args.color),
            material_type='pbr',
            metallic=args.metallic,
            roughness=args.roughness
        )
    elif args.action == 'assign':
        result = assign_material_to_layer(args.layer_name, args.material_id)
    elif args.action == 'preset':
        presets_data = {
            'gold': {'color': [255, 215, 0], 'metallic': 0.95, 'roughness': 0.05},
            'silver': {'color': [192, 192, 192], 'metallic': 0.90, 'roughness': 0.08},
            'platinum': {'color': [229, 228, 226], 'metallic': 0.92, 'roughness': 0.06},
            'copper': {'color': [184, 115, 51], 'metallic': 0.85, 'roughness': 0.15},
            'bronze': {'color': [205, 127, 50], 'metallic': 0.80, 'roughness': 0.20},
        }
        p = presets_data[args.preset]
        result = create_material(
            name=f"{args.preset.title()}_PBR",
            color=p['color'],
            material_type='pbr',
            metallic=p['metallic'],
            roughness=p['roughness']
        )
    else:
        print(f"Unknown action: {args.action}", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
