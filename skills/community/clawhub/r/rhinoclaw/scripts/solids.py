#!/usr/bin/env python3
"""Solid operations: fillet/chamfer edges, split, trim."""

import argparse
import json
import sys
from rhino_client import RhinoClient


def fillet_edges(object_id: str, radius: float, edge_indices: list = None, 
                 delete_input: bool = True) -> dict:
    """Fillet (round) edges of a solid.
    
    Args:
        object_id: Solid (Brep) GUID
        radius: Fillet radius
        edge_indices: Optional list of edge indices to fillet (all if not specified)
        delete_input: Delete original object
    """
    params = {
        "object_id": object_id,
        "radius": radius,
        "delete_input": delete_input
    }
    if edge_indices:
        params["edge_indices"] = edge_indices
    
    with RhinoClient() as client:
        return client.send_command("fillet_edges", params)


def chamfer_edges(object_id: str, distance: float, distance2: float = None,
                  edge_indices: list = None, delete_input: bool = True) -> dict:
    """Chamfer (bevel) edges of a solid.
    
    Args:
        object_id: Solid (Brep) GUID
        distance: Chamfer distance
        distance2: Optional second distance for asymmetric chamfer
        edge_indices: Optional list of edge indices (all if not specified)
        delete_input: Delete original object
    """
    params = {
        "object_id": object_id,
        "distance": distance,
        "delete_input": delete_input
    }
    if distance2 is not None:
        params["distance2"] = distance2
    if edge_indices:
        params["edge_indices"] = edge_indices
    
    with RhinoClient() as client:
        return client.send_command("chamfer_edges", params)


def split_brep(object_id: str, cutter_id: str, delete_input: bool = True,
               delete_cutter: bool = False) -> dict:
    """Split a solid with another solid or surface.
    
    Args:
        object_id: Object to split
        cutter_id: Cutter object (Brep or Surface)
        delete_input: Delete original object
        delete_cutter: Delete cutter object
    
    Returns:
        All resulting pieces
    """
    params = {
        "object_id": object_id,
        "cutter_id": cutter_id,
        "delete_input": delete_input,
        "delete_cutter": delete_cutter
    }
    
    with RhinoClient() as client:
        return client.send_command("split_brep", params)


def trim_brep(object_id: str, cutter_id: str, keep_point: list = None,
              delete_input: bool = True, delete_cutter: bool = False) -> dict:
    """Trim a solid, keeping one side.
    
    Args:
        object_id: Object to trim
        cutter_id: Cutter object
        keep_point: Point [x,y,z] indicating which side to keep (largest piece if not specified)
        delete_input: Delete original object
        delete_cutter: Delete cutter object
    """
    params = {
        "object_id": object_id,
        "cutter_id": cutter_id,
        "delete_input": delete_input,
        "delete_cutter": delete_cutter
    }
    if keep_point:
        params["keep_point"] = keep_point
    
    with RhinoClient() as client:
        return client.send_command("trim_brep", params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solid operations')
    subparsers = parser.add_subparsers(dest='action', help='Operation')
    
    # Fillet edges
    fillet_p = subparsers.add_parser('fillet', help='Fillet solid edges')
    fillet_p.add_argument('object_id', help='Solid GUID')
    fillet_p.add_argument('--radius', '-r', type=float, required=True, help='Fillet radius')
    fillet_p.add_argument('--edges', '-e', type=int, nargs='+', help='Edge indices')
    fillet_p.add_argument('--keep', '-k', action='store_true', help='Keep original')
    
    # Chamfer edges
    chamfer_p = subparsers.add_parser('chamfer', help='Chamfer solid edges')
    chamfer_p.add_argument('object_id', help='Solid GUID')
    chamfer_p.add_argument('--distance', '-d', type=float, required=True, help='Chamfer distance')
    chamfer_p.add_argument('--distance2', type=float, help='Second distance')
    chamfer_p.add_argument('--edges', '-e', type=int, nargs='+', help='Edge indices')
    chamfer_p.add_argument('--keep', '-k', action='store_true', help='Keep original')
    
    # Split
    split_p = subparsers.add_parser('split', help='Split solid with cutter')
    split_p.add_argument('object_id', help='Object to split')
    split_p.add_argument('cutter_id', help='Cutter object')
    split_p.add_argument('--keep', '-k', action='store_true', help='Keep original')
    split_p.add_argument('--keep-cutter', action='store_true', help='Keep cutter')
    
    # Trim
    trim_p = subparsers.add_parser('trim', help='Trim solid, keep one side')
    trim_p.add_argument('object_id', help='Object to trim')
    trim_p.add_argument('cutter_id', help='Cutter object')
    trim_p.add_argument('--keep-point', '-p', type=str, help='Point to keep as x,y,z')
    trim_p.add_argument('--keep', '-k', action='store_true', help='Keep original')
    trim_p.add_argument('--keep-cutter', action='store_true', help='Keep cutter')
    
    args = parser.parse_args()
    
    def parse_point(s: str) -> list:
        return [float(x) for x in s.split(',')]
    
    if args.action == 'fillet':
        result = fillet_edges(args.object_id, args.radius, args.edges, 
                              delete_input=not args.keep)
    elif args.action == 'chamfer':
        result = chamfer_edges(args.object_id, args.distance, args.distance2,
                               args.edges, delete_input=not args.keep)
    elif args.action == 'split':
        result = split_brep(args.object_id, args.cutter_id,
                            delete_input=not args.keep,
                            delete_cutter=not getattr(args, 'keep_cutter', False))
    elif args.action == 'trim':
        keep_pt = parse_point(args.keep_point) if args.keep_point else None
        result = trim_brep(args.object_id, args.cutter_id, keep_pt,
                           delete_input=not args.keep,
                           delete_cutter=not getattr(args, 'keep_cutter', False))
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
