#!/usr/bin/env python3
"""
3D模型解析模块
支持格式：STL, STEP, IGES
提取内容：顶点、边、面、包围盒尺寸、法向量
"""

import argparse
import json
import sys
from pathlib import Path
import numpy as np


def parse_stl(file_path):
    """解析STL文件"""
    try:
        import trimesh
        
        mesh = trimesh.load(file_path, force='mesh')
        
        # 提取顶点
        vertices = mesh.vertices.tolist()
        
        # 提取面（三角形索引）
        faces = mesh.faces.tolist()
        
        # 提取边
        edges = mesh.edges.tolist()
        
        # 计算包围盒
        bounds = mesh.bounds
        bounding_box = {
            "min": bounds[0].tolist(),
            "max": bounds[1].tolist(),
            "dimensions": (bounds[1] - bounds[0]).tolist()
        }
        
        # 提取关键尺寸
        dimensions = bounding_box["dimensions"]
        key_dimensions = {
            "length": max(dimensions),
            "width": sorted(dimensions)[1] if dimensions[0] != max(dimensions) else sorted(dimensions)[1],
            "height": min(dimensions)
        }
        
        # 计算总面积和体积
        surface_area = float(mesh.area)
        volume = float(mesh.volume) if mesh.is_watertight else 0
        
        features = {
            "format": "STL",
            "source_file": str(Path(file_path).resolve()),
            "vertices": vertices,
            "faces": faces,
            "edges": edges,
            "bounding_box": bounding_box,
            "key_dimensions": key_dimensions,
            "surface_area": surface_area,
            "volume": volume,
            "triangles_count": len(faces),
            "vertices_count": len(vertices),
            "is_watertight": mesh.is_watertight
        }
        
        return features
        
    except ImportError:
        print(json.dumps({"error": "trimesh not installed. Run: pip install trimesh"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Failed to parse STL: {str(e)}"}))
        sys.exit(1)


def parse_step_iges(file_path):
    """解析STEP/IGES文件"""
    try:
        import cadquery as cq
        
        # 加载模型
        result = cq.importers.importStep(str(file_path))
        
        # 获取包围盒
        bb = result.val().BoundingBox()
        bounding_box = {
            "min": [bb.xmin, bb.ymin, bb.zmin],
            "max": [bb.xmax, bb.ymax, bb.zmax],
            "dimensions": [bb.xmax - bb.xmin, bb.ymax - bb.ymin, bb.zmax - bb.zmin]
        }
        
        # 获取关键尺寸
        dimensions = bounding_box["dimensions"]
        key_dimensions = {
            "length": max(dimensions),
            "width": sorted(dimensions)[1],
            "height": min(dimensions)
        }
        
        # 提取实体（简化为包围盒信息）
        solids = result.val().Solids()
        faces = result.val().Faces()
        edges = result.val().Edges()
        
        # 转换为可序列化格式
        vertices = set()
        for edge in edges:
            verts = edge.Vertices()
            for v in verts:
                vertices.add((round(v.X(), 6), round(v.Y(), 6), round(v.Z(), 6)))
        vertices = list(vertices)
        
        features = {
            "format": "STEP/IGES",
            "source_file": str(Path(file_path).resolve()),
            "bounding_box": bounding_box,
            "key_dimensions": key_dimensions,
            "solids_count": len(solids),
            "faces_count": len(faces),
            "edges_count": len(edges),
            "vertices_count": len(vertices),
            "vertices": vertices[:1000] if len(vertices) > 1000 else vertices,  # 限制数量
            "extraction_note": "Simplified representation. Full BREP data requires CAD viewer."
        }
        
        return features
        
    except ImportError:
        print(json.dumps({"error": "cadquery not installed. Run: pip install cadquery"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Failed to parse STEP/IGES: {str(e)}"}))
        sys.exit(1)


def project_to_2d(features_3d, axis='z'):
    """将3D特征投影到2D平面"""
    projected = {
        "vertices": [],
        "edges": [],
        "bounding_box_2d": None
    }
    
    vertices = features_3d.get("vertices", [])
    
    # 根据投影轴选择2D坐标
    axis_map = {'x': (1, 2), 'y': (0, 2), 'z': (0, 1)}
    ax1, ax2 = axis_map.get(axis, (0, 1))
    
    for v in vertices:
        if len(v) >= 3:
            projected["vertices"].append([v[ax1], v[ax2]])
    
    # 投影包围盒
    bb = features_3d.get("bounding_box", {})
    if bb:
        min_pt = bb.get("min", [])
        max_pt = bb.get("max", [])
        if len(min_pt) >= 3 and len(max_pt) >= 3:
            projected["bounding_box_2d"] = {
                "min": [min_pt[ax1], min_pt[ax2]],
                "max": [max_pt[ax1], max_pt[ax2]]
            }
    
    # 投影边
    edges = features_3d.get("edges", [])
    for edge in edges:
        if len(edge) == 2 and all(len(vertices) >= max(edge) + 1 for vertices in [vertices]):
            v1 = vertices[edge[0]] if edge[0] < len(vertices) else None
            v2 = vertices[edge[1]] if edge[1] < len(vertices) else None
            if v1 and v2 and len(v1) >= 3 and len(v2) >= 3:
                projected["edges"].append([
                    [v1[ax1], v1[ax2]],
                    [v2[ax1], v2[ax2]]
                ])
    
    return projected


def main():
    parser = argparse.ArgumentParser(description='Parse 3D model files')
    parser.add_argument('--input', '-i', required=True, help='Input 3D model file')
    parser.add_argument('--output', '-o', default='features_3d.json', help='Output JSON file')
    parser.add_argument('--project-axis', '-a', default='z', choices=['x', 'y', 'z'],
                        help='Projection axis for 2D comparison (default: z)')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(json.dumps({"error": f"File not found: {args.input}"}))
        sys.exit(1)
    
    suffix = input_path.suffix.lower()
    
    if suffix == '.stl':
        features = parse_stl(str(input_path))
    elif suffix in ['.step', '.stp', '.iges', '.igs']:
        features = parse_step_iges(str(input_path))
    else:
        print(json.dumps({"error": f"Unsupported format: {suffix}"}))
        sys.exit(1)
    
    # 添加投影数据
    features["projection_2d"] = project_to_2d(features, axis=args.project_axis)
    features["projection_axis"] = args.project_axis
    features["file_size"] = input_path.stat().st_size
    
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(features, f, indent=2, ensure_ascii=False)
    
    print(json.dumps({
        "status": "success",
        "output": str(output_path),
        "vertices_count": features.get("vertices_count", 0),
        "triangles_count": features.get("triangles_count", 0),
        "projection_axis": args.project_axis
    }))


if __name__ == "__main__":
    main()
