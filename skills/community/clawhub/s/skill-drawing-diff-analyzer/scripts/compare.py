#!/usr/bin/env python3
"""
差异对比模块
执行2D与3D特征的多维度对比
输出：diff_report.json + diff_report.md
"""

import argparse
import json
import sys
from pathlib import Path
import numpy as np
from collections import defaultdict
from datetime import datetime


def load_features(features_2d_path, features_3d_path):
    """加载2D和3D特征文件"""
    with open(features_2d_path, 'r', encoding='utf-8') as f:
        features_2d = json.load(f)
    with open(features_3d_path, 'r', encoding='utf-8') as f:
        features_3d = json.load(f)
    return features_2d, features_3d


def compare_dimensions(features_2d, features_3d, tolerance=0.1):
    """对比尺寸"""
    differences = []
    
    dims_2d = features_2d.get("dimensions", [])
    key_dims_3d = features_3d.get("key_dimensions", {})
    dims_3d_values = [
        key_dims_3d.get("length", 0),
        key_dims_3d.get("width", 0),
        key_dims_3d.get("height", 0)
    ]
    
    for dim in dims_2d:
        val_2d = dim.get("value")
        dim_type = dim.get("dimension_type", "linear")
        
        if val_2d is None or val_2d <= 0:
            continue
        
        if dim_type == "diameter":
            candidates = [v / 2 for v in dims_3d_values if v > 0]
        elif dim_type == "radius":
            candidates = dims_3d_values
        else:
            candidates = dims_3d_values
        
        if not candidates:
            continue
        
        closest_3d = min(candidates, key=lambda x: abs(x - val_2d) if val_2d > 0 else float('inf'))
        
        if closest_3d > 0:
            diff = abs(val_2d - closest_3d)
            diff_ratio = diff / val_2d * 100 if val_2d > 0 else 0
            
            if diff > tolerance:
                differences.append({
                    "type": "dimension_mismatch",
                    "dimension_type": dim_type,
                    "location": dim.get("bbox"),
                    "page": dim.get("page"),
                    "value_2d": val_2d,
                    "value_3d": closest_3d,
                    "difference": round(diff, 4),
                    "difference_ratio": round(diff_ratio, 2),
                    "tolerance": tolerance,
                    "severity": "critical" if diff > tolerance * 5 else "warning"
                })
    
    return differences


def compare_geometric_tolerances(features_2d, features_3d, tolerance=0.05):
    """对比几何公差"""
    differences = []
    geo_tols_2d = features_2d.get("geometric_tolerances", [])
    
    for tol in geo_tols_2d:
        geo_type = tol.get("geometric_type", "unknown")
        value = tol.get("value")
        
        differences.append({
            "type": "geometric_tolerance",
            "geometric_type": geo_type,
            "geometric_type_cn": get_geometric_type_cn(geo_type),
            "location": tol.get("bbox"),
            "page": tol.get("page"),
            "tolerance_value": value,
            "severity": "info",
            "note": "几何公差需要人工测量验证，3D模型无法自动检测"
        })
    
    return differences


def get_geometric_type_cn(geo_type):
    """获取几何公差中文名称"""
    mapping = {
        "position": "位置度",
        "perpendicularity": "垂直度",
        "parallelism": "平行度",
        "angularity": "倾斜度",
        "flatness": "平面度",
        "straightness": "直线度",
        "circularity": "圆度",
        "cylindricity": "圆柱度",
        "concentricity": "同轴度",
        "symmetry": "对称度",
        "circular_runout": "圆跳动",
        "totalrunout": "全跳动",
        "profile": "轮廓度",
        "unknown": "未知"
    }
    return mapping.get(geo_type, geo_type)


def compare_contours(features_2d, features_3d, tolerance=0.1):
    """对比轮廓"""
    differences = []
    entities_2d = features_2d.get("entities", [])
    proj_3d = features_3d.get("projection_2d", {})
    vertices_3d = proj_3d.get("vertices", [])
    
    if not vertices_3d:
        bb_3d = features_3d.get("bounding_box", {})
        if bb_3d:
            min_3d = bb_3d.get("min", [0, 0, 0])[:2]
            max_3d = bb_3d.get("max", [1, 1, 1])[:2]
            vertices_3d = [min_3d, [max_3d[0], min_3d[1]], max_3d, [min_3d[0], max_3d[1]]]
    
    circles_2d = [e for e in entities_2d if e.get("type") == "CIRCLE"]
    
    for circle in circles_2d:
        center_2d = np.array(circle.get("center", [0, 0]))
        radius_2d = circle.get("radius", 0)
        
        if radius_2d <= 0:
            continue
        
        if vertices_3d:
            distances = [np.linalg.norm(np.array(v[:2]) - center_2d) for v in vertices_3d]
            avg_dist = np.mean(distances) if distances else 0
            
            if abs(avg_dist - radius_2d) > tolerance:
                differences.append({
                    "type": "contour_deviation",
                    "circle_center": center_2d.tolist(),
                    "circle_radius": radius_2d,
                    "projected_range": round(avg_dist, 4),
                    "deviation": round(abs(avg_dist - radius_2d), 4),
                    "severity": "warning"
                })
    
    lines_2d = [e for e in entities_2d if e.get("type") == "LINE"]
    
    for line in lines_2d:
        start_2d = np.array(line.get("start", [0, 0]))
        end_2d = np.array(line.get("end", [0, 0]))
        length_2d = np.linalg.norm(end_2d - start_2d)
        
        if length_2d <= tolerance:
            continue
        
        edges_3d = proj_3d.get("edges", [])
        matched = False
        for edge in edges_3d:
            if len(edge) == 2:
                start_3d = np.array(edge[0])
                end_3d = np.array(edge[1])
                length_3d = np.linalg.norm(end_3d - start_3d)
                
                if abs(length_2d - length_3d) < tolerance * 10:
                    matched = True
                    break
        
        if not matched and length_2d > tolerance:
            differences.append({
                "type": "missing_contour",
                "line_start": start_2d.tolist(),
                "line_end": end_2d.tolist(),
                "line_length": round(length_2d, 4),
                "severity": "info",
                "note": "2D线段在3D投影中未找到对应"
            })
    
    return differences


def compare_bounding_box(features_2d, features_3d, tolerance=0.1):
    """对比包围盒"""
    differences = []
    bb_2d = features_2d.get("bounding_box", {})
    bb_3d = features_3d.get("bounding_box", {})
    
    if not bb_2d or not bb_3d:
        return differences
    
    dims_2d = np.array(bb_2d.get("max", [1, 1])) - np.array(bb_2d.get("min", [0, 0]))
    dims_3d = np.array(bb_3d.get("dimensions", [1, 1, 1])[:2])
    diff = np.abs(dims_2d - dims_3d)
    
    if np.any(diff > tolerance):
        differences.append({
            "type": "bounding_box_mismatch",
            "dimensions_2d": dims_2d.tolist(),
            "dimensions_3d": dims_3d.tolist(),
            "difference": diff.tolist(),
            "severity": "critical" if np.any(diff > tolerance * 10) else "warning"
        })
    
    return differences


def generate_summary(differences, tolerance):
    """生成差异摘要"""
    summary = {
        "total_differences": len(differences),
        "by_type": defaultdict(int),
        "by_severity": {"critical": 0, "warning": 0, "info": 0},
        "tolerance": tolerance,
        "geometric_types_found": []
    }
    
    for diff in differences:
        summary["by_type"][diff["type"]] += 1
        severity = diff.get("severity", "info")
        summary["by_severity"][severity] += 1
        
        if diff["type"] == "geometric_tolerance":
            geo_type = diff.get("geometric_type_cn", "未知")
            if geo_type not in summary["geometric_types_found"]:
                summary["geometric_types_found"].append(geo_type)
    
    summary["by_type"] = dict(summary["by_type"])
    return summary


def generate_markdown_report(report):
    """生成Markdown格式报告"""
    summary = report["summary"]
    differences = report["differences"]
    
    # 时间格式化
    generated_at = report["report_info"]["generated_at"]
    try:
        dt = datetime.fromisoformat(generated_at)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        time_str = generated_at
    
    md = []
    md.append("# 图纸差异分析报告")
    md.append("")
    md.append("## 基本信息")
    md.append("")
    md.append("| 项目 | 内容 |")
    md.append("|------|------|")
    md.append(f"| 分析时间 | {time_str} |")
    md.append(f"| 2D图纸 | {report['source_files']['2d_drawing']} |")
    md.append(f"| 3D模型 | {report['source_files']['3d_model']} |")
    md.append(f"| 公差阈值 | {report['tolerance']}mm |")
    md.append("")
    
    md.append("## 统计摘要")
    md.append("")
    md.append(f"- **差异总数**: {summary['total_differences']}")
    md.append(f"- **关键问题 (Critical)**: {summary['by_severity']['critical']}")
    md.append(f"- **警告 (Warning)**: {summary['by_severity']['warning']}")
    md.append(f"- **提示 (Info)**: {summary['by_severity']['info']}")
    md.append("")
    
    if summary.get("geometric_types_found"):
        md.append(f"- **检测到的几何公差**: {', '.join(summary['geometric_types_found'])}")
        md.append("")
    
    md.append("### 按类型统计")
    md.append("")
    md.append("| 类型 | 数量 |")
    md.append("|------|------|")
    for diff_type, count in summary["by_type"].items():
        type_name = TYPE_NAMES.get(diff_type, diff_type)
        md.append(f"| {type_name} | {count} |")
    md.append("")
    
    # 文件统计
    stats = report["file_stats"]
    md.append("## 文件统计")
    md.append("")
    md.append("| 项目 | 数量 |")
    md.append("|------|------|")
    md.append(f"| 2D尺寸标注 | {stats['2d_dimensions_count']} |")
    md.append(f"| 2D几何公差 | {stats['2d_geometric_tolerances_count']} |")
    md.append(f"| 2D几何实体 | {stats['2d_entities_count']} |")
    md.append(f"| 3D顶点 | {stats['3d_vertices_count']} |")
    md.append(f"| 3D三角面 | {stats['3d_triangles_count']} |")
    md.append("")
    
    # 差异详情
    md.append("## 差异详情")
    md.append("")
    
    if not differences:
        md.append("*未发现显著差异*")
        md.append("")
    else:
        # 按类型分组显示
        dims = [d for d in differences if d["type"] == "dimension_mismatch"]
        geos = [d for d in differences if d["type"] == "geometric_tolerance"]
        contours = [d for d in differences if d["type"] in ["contour_deviation", "missing_contour"]]
        bboxes = [d for d in differences if d["type"] == "bounding_box_mismatch"]
        
        # 尺寸差异
        if dims:
            md.append("### 尺寸差异")
            md.append("")
            md.append("| 编号 | 类型 | 2D值 | 3D值 | 偏差 | 偏差率 | 严重性 |")
            md.append("|------|------|------|------|------|--------|--------|")
            for d in dims:
                dim_type = DIM_TYPE_NAMES.get(d.get("dimension_type", ""), d.get("dimension_type", ""))
                v2d = d.get("value_2d", "-")
                v3d = d.get("value_3d", "-")
                diff = d.get("difference", "-")
                ratio = d.get("difference_ratio", "-")
                sev = d.get("severity", "info").upper()
                md.append(f"| {d['id']} | {dim_type} | {v2d} | {v3d} | {diff} | {ratio}% | {sev} |")
            md.append("")
        
        # 几何公差
        if geos:
            md.append("### 几何公差 (需人工验证)")
            md.append("")
            md.append("| 编号 | 类型 | 公差值 | 页码 |")
            md.append("|------|------|--------|------|")
            for d in geos:
                geo_type = d.get("geometric_type_cn", "未知")
                value = d.get("tolerance_value", "-")
                page = d.get("page", "-")
                md.append(f"| {d['id']} | {geo_type} | {value} | {page} |")
            md.append("")
        
        # 轮廓差异
        if contours:
            md.append("### 轮廓差异")
            md.append("")
            md.append("| 编号 | 类型 | 描述 | 严重性 |")
            md.append("|------|------|------|--------|")
            for d in contours:
                diff_type = d.get("type", "")
                desc = d.get("note", "") if diff_type == "missing_contour" else f"半径偏差: {d.get('deviation', '-')}"
                sev = d.get("severity", "info").upper()
                type_name = "轮廓缺失" if diff_type == "missing_contour" else "轮廓偏差"
                md.append(f"| {d['id']} | {type_name} | {desc} | {sev} |")
            md.append("")
        
        # 包围盒差异
        if bboxes:
            md.append("### 整体尺寸差异")
            md.append("")
            md.append("| 编号 | 2D尺寸 | 3D尺寸 | 偏差 | 严重性 |")
            md.append("|------|--------|--------|------|--------|")
            for d in bboxes:
                dims_2d = d.get("dimensions_2d", [])
                dims_3d = d.get("dimensions_3d", [])
                diff = d.get("difference", [])
                sev = d.get("severity", "info").upper()
                md.append(f"| {d['id']} | {dims_2d} | {dims_3d} | {diff} | {sev} |")
            md.append("")
    
    # 建议
    md.append("## 处理建议")
    md.append("")
    critical_count = summary["by_severity"]["critical"]
    warning_count = summary["by_severity"]["warning"]
    
    if critical_count > 0:
        md.append(f"1. **优先处理 {critical_count} 个关键问题**，这些差异超过公差5倍，必须修改设计或重新建模")
    if warning_count > 0:
        md.append(f"2. **建议核查 {warning_count} 个警告项**，确认是否为设计意图或实际错误")
    if summary["by_severity"]["info"] > 0:
        md.append(f"3. **{summary['by_severity']['info']} 个提示信息**仅供参考，可根据实际情况决定是否处理")
    if critical_count == 0 and warning_count == 0:
        md.append("*当前图纸与模型基本一致，无需特殊处理*")
    
    md.append("")
    md.append("---")
    md.append(f"*报告由 drawing-diff-analyzer 自动生成*")
    
    return "\n".join(md)


# 类型名称映射
TYPE_NAMES = {
    "dimension_mismatch": "尺寸差异",
    "geometric_tolerance": "几何公差",
    "contour_deviation": "轮廓偏差",
    "missing_contour": "轮廓缺失",
    "bounding_box_mismatch": "整体尺寸差异"
}

DIM_TYPE_NAMES = {
    "linear": "线性",
    "diameter": "直径",
    "radius": "半径",
    "angular": "角度"
}


def main():
    parser = argparse.ArgumentParser(description='Compare 2D and 3D features')
    parser.add_argument('--features-2d', '-2', required=True, help='2D features JSON file')
    parser.add_argument('--features-3d', '-3', required=True, help='3D features JSON file')
    parser.add_argument('--output', '-o', default='diff_report', help='Output base name (will generate .json and .md)')
    parser.add_argument('--tolerance', '-t', type=float, default=0.1, help='Comparison tolerance (mm)')
    args = parser.parse_args()
    
    for path in [args.features_2d, args.features_3d]:
        if not Path(path).exists():
            print(json.dumps({"error": f"File not found: {path}"}))
            sys.exit(1)
    
    features_2d, features_3d = load_features(args.features_2d, args.features_3d)
    
    differences = []
    differences.extend(compare_dimensions(features_2d, features_3d, args.tolerance))
    differences.extend(compare_geometric_tolerances(features_2d, features_3d, args.tolerance))
    differences.extend(compare_contours(features_2d, features_3d, args.tolerance))
    differences.extend(compare_bounding_box(features_2d, features_3d, args.tolerance))
    
    # 按严重性排序
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    sorted_diffs = sorted(differences, key=lambda x: severity_order.get(x.get("severity", "info"), 3))
    
    for i, diff in enumerate(sorted_diffs, 1):
        diff["id"] = i
    
    summary = generate_summary(sorted_diffs, args.tolerance)
    
    source_2d = features_2d.get("source_file", "")
    source_3d = features_3d.get("source_file", "")
    dims_2d_count = len(features_2d.get("dimensions", []))
    geo_tols_2d_count = len(features_2d.get("geometric_tolerances", []))
    entities_2d_count = len(features_2d.get("entities", []))
    vertices_3d_count = features_3d.get("vertices_count", 0)
    triangles_3d_count = features_3d.get("triangles_count", 0)
    
    report = {
        "report_info": {
            "generated_at": datetime.now().isoformat(),
            "tool": "drawing-diff-analyzer",
            "version": "1.0"
        },
        "source_files": {
            "2d_drawing": source_2d,
            "3d_model": source_3d
        },
        "file_stats": {
            "2d_dimensions_count": dims_2d_count,
            "2d_geometric_tolerances_count": geo_tols_2d_count,
            "2d_entities_count": entities_2d_count,
            "3d_vertices_count": vertices_3d_count,
            "3d_triangles_count": triangles_3d_count
        },
        "summary": summary,
        "differences": sorted_diffs,
        "tolerance": args.tolerance
    }
    
    # 保存JSON
    output_json = Path(args.output).with_suffix('.json')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 生成Markdown
    output_md = Path(args.output).with_suffix('.md')
    md_content = generate_markdown_report(report)
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(json.dumps({
        "status": "success",
        "output_json": str(output_json),
        "output_md": str(output_md),
        "total_differences": summary["total_differences"],
        "critical": summary["by_severity"]["critical"],
        "warning": summary["by_severity"]["warning"],
        "info": summary["by_severity"]["info"]
    }))


if __name__ == "__main__":
    main()
