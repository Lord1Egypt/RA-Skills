#!/usr/bin/env python3
"""
2D图纸解析模块
支持格式：DWG, DXF, PDF
提取内容：轮廓线、圆、弧、尺寸标注、几何公差、基准点
"""

import argparse
import json
import sys
import re
from pathlib import Path


# 几何公差符号映射
GEOMETRIC_TOLERANCE_SYMBOLS = {
    'straightness': '直线度',
    'flatness': '平面度',
    'circularity': '圆度',
    'cylindricity': '圆柱度',
    'profile_of_a_line': '线轮廓度',
    'profile_of_a_surface': '面轮廓度',
    'angularity': '倾斜度',
    'perpendicularity': '垂直度',
    'parallelism': '平行度',
    'position': '位置度',
    'concentricity': '同轴度',
    'symmetry': '对称度',
    'circular_runout': '圆跳动',
    'totalrunout': '全跳动'
}

# 直径符号变体
DIAMETER_SYMBOLS = ['Ø', 'Φ', 'phi', 'dia', 'DIA', 'Diameter', '直径']
# 特殊符号的正则
DIAMETER_PATTERNS = [
    r'Ø(\d+\.?\d*)',
    r'Φ(\d+\.?\d*)',
    r'DIA\s*(\d+\.?\d*)',
    r'dia\s*(\d+\.?\d*)',
    r'直径\s*(\d+\.?\d*)',
    r'\\u00D8(\d+\.?\d*)',  # Ø的Unicode
]

# 几何公差符号Unicode映射
TOLERANCE_UNICODE = {
    '⊥': 'perpendicularity',    # 垂直度
    '⊥': 'angularity',          # 倾斜度(可能)
    '∥': 'parallelism',          # 平行度
    'ⓞ': 'position',             # 位置度
    '◎': 'position',             # 位置度
    '⧠': 'circularity',          # 圆度
    '□': 'flatness',             # 平面度(方框)
    '⿹': 'flatness',            # 平面度
    '⌭': 'cylindricity',         # 圆柱度
}


def parse_dwg_dxf(file_path):
    """解析DWG/DXF文件"""
    try:
        import ezdxf
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        
        features = {
            "format": "DWG/DXF",
            "entities": [],
            "dimensions": [],
            "geometric_tolerances": [],
            "reference_points": [],
            "bounding_box": None
        }
        
        min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
        
        for entity in msp:
            entity_type = entity.dxftype()
            entity_data = {"type": entity_type}
            
            if entity_type == 'LINE':
                start = entity.dxf.start
                end = entity.dxf.end
                entity_data.update({
                    "start": [start.x, start.y],
                    "end": [end.x, end.y]
                })
                min_x = min(min_x, start.x, end.x)
                min_y = min(min_y, start.y, end.y)
                max_x = max(max_x, start.x, end.x)
                max_y = max(max_y, start.y, end.y)
                
            elif entity_type == 'CIRCLE':
                center = entity.dxf.center
                radius = entity.dxf.radius
                entity_data.update({
                    "center": [center.x, center.y],
                    "radius": radius
                })
                min_x = min(min_x, center.x - radius)
                min_y = min(min_y, center.y - radius)
                max_x = max(max_x, center.x + radius)
                max_y = max(max_y, center.y + radius)
                
            elif entity_type == 'ARC':
                center = entity.dxf.center
                radius = entity.dxf.radius
                start_angle = entity.dxf.start_angle
                end_angle = entity.dxf.end_angle
                entity_data.update({
                    "center": [center.x, center.y],
                    "radius": radius,
                    "start_angle": start_angle,
                    "end_angle": end_angle
                })
                min_x = min(min_x, center.x - radius)
                min_y = min(min_y, center.y - radius)
                max_x = max(max_x, center.x + radius)
                max_y = max(max_y, center.y + radius)
                
            elif entity_type == 'LWPOLYLINE' or entity_type == 'POLYLINE':
                points = []
                if hasattr(entity, 'get_points'):
                    for point in entity.get_points():
                        points.append([point[0], point[1]])
                entity_data["points"] = points
                if points:
                    xs = [p[0] for p in points]
                    ys = [p[1] for p in points]
                    min_x = min(min_x, min(xs))
                    min_y = min(min_y, min(ys))
                    max_x = max(max_x, max(xs))
                    max_y = max(max_y, max(ys))
                    
            elif entity_type == 'DIMENSION':
                dim_text = entity.dxf.text if hasattr(entity.dxf, 'text') else ""
                def_point = entity.dxf.defpoint if hasattr(entity.dxf, 'defpoint') else None
                
                # 解析尺寸类型
                dim_type = parse_dimension_type(dim_text)
                
                entity_data.update({
                    "text": str(dim_text),
                    "dimension_type": dim_type,
                    "defpoint": [def_point.x, def_point.y] if def_point else None
                })
                
                # 区分尺寸标注和几何公差
                if is_geometric_tolerance(dim_text):
                    features["geometric_tolerances"].append(entity_data)
                else:
                    features["dimensions"].append(entity_data)
                continue
            
            features["entities"].append(entity_data)
        
        if min_x != float('inf'):
            features["bounding_box"] = {
                "min": [min_x, min_y],
                "max": [max_x, max_y]
            }
            
        return features
        
    except ImportError:
        print(json.dumps({"error": "ezdxf not installed. Run: pip install ezdxf"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Failed to parse DWG/DXF: {str(e)}"}))
        sys.exit(1)


def parse_pdf(file_path):
    """解析PDF文件"""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        
        features = {
            "format": "PDF",
            "entities": [],
            "dimensions": [],
            "geometric_tolerances": [],
            "reference_points": [],
            "bounding_box": None
        }
        
        min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
        
        for page_num, page in enumerate(doc):
            text_dict = page.get_text("dict")
            
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            bbox = span["bbox"]
                            
                            # 解析文本内容
                            parsed = parse_dimension_text(text)
                            
                            if parsed:
                                item = {
                                    "text": text,
                                    "original": parsed["original"],
                                    "dimension_type": parsed["type"],
                                    "value": parsed["value"],
                                    "tolerance": parsed.get("tolerance"),
                                    "bbox": list(bbox),
                                    "page": page_num + 1
                                }
                                
                                # 区分几何公差和尺寸标注
                                if is_geometric_tolerance(text):
                                    features["geometric_tolerances"].append(item)
                                else:
                                    features["dimensions"].append(item)
                            else:
                                features["entities"].append({
                                    "type": "text",
                                    "content": text,
                                    "bbox": list(bbox)
                                })
                            
                            min_x = min(min_x, bbox[0])
                            min_y = min(min_y, bbox[1])
                            max_x = max(max_x, bbox[2])
                            max_y = max(max_y, bbox[3])
                            
                # 提取矢量图形
                path_list = block.get("paths", [])
                for path in path_list:
                    if path.get("items"):
                        features["entities"].append({
                            "type": "path",
                            "items": path.get("items", []),
                            "bbox": path.get("rect", [])
                        })
                        
        if min_x != float('inf'):
            features["bounding_box"] = {
                "min": [min_x, min_y],
                "max": [max_x, max_y]
            }
            
        return features
        
    except ImportError:
        print(json.dumps({"error": "PyMuPDF not installed. Run: pip install PyMuPDF"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Failed to parse PDF: {str(e)}"}))
        sys.exit(1)


def parse_dimension_text(text):
    """
    解析尺寸文本，返回结构化数据
    支持: Ø10, Φ10, 10±0.05, 10.5, 位置度0.05, 垂直度0.02 等
    """
    if not text:
        return None
    
    result = {
        "original": text,
        "type": "linear",  # 默认线性尺寸
        "value": None,
        "tolerance": None
    }
    
    original_text = text.strip()
    
    # 1. 检测直径符号 Ø/Φ
    for pattern in DIAMETER_PATTERNS:
        match = re.search(pattern, original_text, re.IGNORECASE)
        if match:
            result["type"] = "diameter"
            if match.groups():
                try:
                    result["value"] = float(match.group(1))
                except:
                    pass
            # 提取数字
            nums = re.findall(r'\d+\.?\d*', original_text)
            if nums and result["value"] is None:
                try:
                    result["value"] = float(nums[0])
                except:
                    pass
            return result
    
    # 2. 检测几何公差符号 (Unicode)
    for symbol, tol_type in TOLERANCE_UNICODE.items():
        if symbol in original_text:
            result["type"] = "geometric"
            result["geometric_type"] = tol_type
            # 提取数值
            nums = re.findall(r'\d+\.?\d*', original_text)
            if nums:
                try:
                    result["value"] = float(nums[0])
                except:
                    pass
            return result
    
    # 3. 检测几何公差关键字
    geo_keywords = {
        '位置度': 'position',
        '垂直度': 'perpendicularity', 
        '平行度': 'parallelism',
        '倾斜度': 'angularity',
        '平面度': 'flatness',
        '直线度': 'straightness',
        '圆度': 'circularity',
        '圆柱度': 'cylindricity',
        '同轴度': 'concentricity',
        '对称度': 'symmetry',
        '圆跳动': 'circular_runout',
        '全跳动': 'totalrunout',
        '轮廓度': 'profile',
        '位置': 'position',
        '垂直': 'perpendicularity',
        '平行': 'parallelism',
        '平面': 'flatness'
    }
    
    for keyword, geo_type in geo_keywords.items():
        if keyword in original_text:
            result["type"] = "geometric"
            result["geometric_type"] = geo_type
            nums = re.findall(r'\d+\.?\d*', original_text)
            if nums:
                try:
                    result["value"] = float(nums[0])
                except:
                    pass
            return result
    
    # 4. 检测半径 R
    r_match = re.search(r'R\s*(\d+\.?\d*)', original_text, re.IGNORECASE)
    if r_match:
        result["type"] = "radius"
        try:
            result["value"] = float(r_match.group(1))
        except:
            pass
        return result
    
    # 5. 检测角度 °
    deg_match = re.search(r'(\d+\.?\d*)\s*°', original_text)
    if deg_match:
        result["type"] = "angular"
        try:
            result["value"] = float(deg_match.group(1))
        except:
            pass
        return result
    
    # 6. 普通线性尺寸
    if any(c.isdigit() for c in original_text):
        # 提取数字
        nums = re.findall(r'\d+\.?\d*', original_text)
        if nums:
            try:
                result["value"] = float(nums[0])
            except:
                pass
            # 检测公差 (如 ±0.05)
            tol_match = re.search(r'[±+\-]\s*(\d+\.?\d*)', original_text)
            if tol_match:
                try:
                    result["tolerance"] = float(tol_match.group(1))
                except:
                    pass
            return result
    
    return None


def is_geometric_tolerance(text):
    """判断是否为几何公差"""
    if not text:
        return False
    
    geometric_keywords = [
        '位置度', '垂直度', '平行度', '倾斜度', '平面度',
        '直线度', '圆度', '圆柱度', '同轴度', '对称度',
        '圆跳动', '全跳动', '轮廓度',
        '⊥', '∥', 'ⓞ', '◎', '⌭', '□', '⿹'
    ]
    
    return any(keyword in text for keyword in geometric_keywords)


def parse_dimension_type(dim_text):
    """解析DXF中的尺寸类型"""
    if not dim_text:
        return "unknown"
    
    text = str(dim_text).upper()
    
    if 'Ø' in text or 'PHI' in text or 'DIA' in text:
        return "diameter"
    elif 'R' in text and not 'OR' in text:
        return "radius"
    elif '°' in text:
        return "angular"
    else:
        return "linear"


def main():
    parser = argparse.ArgumentParser(description='Parse 2D drawing files')
    parser.add_argument('--input', '-i', required=True, help='Input 2D drawing file')
    parser.add_argument('--output', '-o', default='features_2d.json', help='Output JSON file')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(json.dumps({"error": f"File not found: {args.input}"}))
        sys.exit(1)
    
    suffix = input_path.suffix.lower()
    
    if suffix in ['.dwg', '.dxf']:
        features = parse_dwg_dxf(str(input_path))
    elif suffix == '.pdf':
        features = parse_pdf(str(input_path))
    else:
        print(json.dumps({"error": f"Unsupported format: {suffix}"}))
        sys.exit(1)
    
    features["source_file"] = str(input_path)
    features["file_size"] = input_path.stat().st_size
    
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(features, f, indent=2, ensure_ascii=False)
    
    print(json.dumps({
        "status": "success",
        "output": str(output_path),
        "entities_count": len(features["entities"]),
        "dimensions_count": len(features["dimensions"]),
        "geometric_tolerances_count": len(features["geometric_tolerances"])
    }))


if __name__ == "__main__":
    main()
