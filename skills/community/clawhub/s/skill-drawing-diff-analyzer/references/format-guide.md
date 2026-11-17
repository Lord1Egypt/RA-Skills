# 图纸格式指南

## 支持的输入格式

### 2D图纸格式

| 格式 | 文件扩展名 | 解析库 | 支持内容 |
|------|-----------|--------|---------|
| AutoCAD | .dwg, .dxf | ezdxf | 实体(线/圆/弧/多段线)、尺寸标注、块参照 |
| 便携文档 | .pdf | pdfplumber + fitz | 文本、矢量图形、尺寸标注、几何公差 |

### 3D模型格式

| 格式 | 文件扩展名 | 解析库 | 支持内容 |
|------|-----------|--------|---------|
| STL | .stl | trimesh | 三角网格、顶点、边、法向量 |
| STEP | .step, .stp | cadquery | BREP几何、实体、面、边 |
| IGES | .iges, .igs | cadquery | 同STEP |

---

## 输出文件说明

### 1. 特征文件 (features_*.json)

**2D特征结构**:
```json
{
  "format": "DWG/DXF/PDF",
  "source_file": "path/to/file",
  "entities": [
    {
      "type": "LINE/CIRCLE/ARC/POLYLINE",
      "start": [x, y],
      "end": [x, y],
      "center": [x, y],
      "radius": 10.5
    }
  ],
  "dimensions": [
    {
      "text": "Ø10",
      "original": "Ø10",
      "dimension_type": "diameter",
      "value": 10.0,
      "tolerance": null,
      "bbox": [x1, y1, x2, y2],
      "page": 1
    }
  ],
  "geometric_tolerances": [
    {
      "text": "位置度0.05",
      "geometric_type": "position",
      "geometric_type_cn": "位置度",
      "value": 0.05,
      "bbox": [x1, y1, x2, y2],
      "page": 1
    }
  ],
  "bounding_box": {
    "min": [x_min, y_min],
    "max": [x_max, y_max]
  }
}
```

**3D特征结构**:
```json
{
  "format": "STL/STEP/IGES",
  "source_file": "path/to/file",
  "vertices": [[x, y, z], ...],
  "faces": [[i, j, k], ...],
  "bounding_box": {
    "min": [x_min, y_min, z_min],
    "max": [x_max, y_max, z_max],
    "dimensions": [length, width, height]
  },
  "key_dimensions": {
    "length": 100.0,
    "width": 50.0,
    "height": 30.0
  },
  "projection_2d": {
    "vertices": [[x, y], ...],
    "edges": [[[x1, y1], [x2, y2]], ...],
    "bounding_box_2d": {...}
  }
}
```

### 2. 差异报告 (diff_report.json)

```json
{
  "report_info": {
    "generated_at": "2024-01-01T12:00:00",
    "tool": "drawing-diff-analyzer",
    "version": "1.0"
  },
  "source_files": {
    "2d_drawing": "blueprint.dwg",
    "3d_model": "model.stl"
  },
  "file_stats": {
    "2d_dimensions_count": 15,
    "2d_geometric_tolerances_count": 5,
    "2d_entities_count": 120,
    "3d_vertices_count": 5000,
    "3d_triangles_count": 3000
  },
  "summary": {
    "total_differences": 12,
    "by_type": {
      "dimension_mismatch": 5,
      "geometric_tolerance": 3,
      "contour_deviation": 2,
      "bounding_box_mismatch": 1
    },
    "by_severity": {
      "critical": 2,
      "warning": 7,
      "info": 3
    },
    "tolerance": 0.1,
    "geometric_types_found": ["位置度", "垂直度", "平面度"]
  },
  "differences": [
    {
      "id": 1,
      "type": "dimension_mismatch",
      "dimension_type": "diameter",
      "location": [150, 200],
      "page": 1,
      "value_2d": 10.0,
      "value_3d": 9.8,
      "difference": 0.2,
      "difference_ratio": 2.0,
      "tolerance": 0.1,
      "severity": "critical"
    },
    {
      "id": 2,
      "type": "geometric_tolerance",
      "geometric_type": "position",
      "geometric_type_cn": "位置度",
      "location": [200, 300],
      "tolerance_value": 0.05,
      "severity": "info",
      "note": "几何公差需要人工测量验证，3D模型无法自动检测"
    }
  ],
  "tolerance": 0.1
}
```

---

## 差异类型说明

| 类型 | 说明 | 判定标准 |
|------|------|---------|
| dimension_mismatch | 尺寸值不一致 | 标注值与测量值偏差 > 公差 |
| geometric_tolerance | 几何公差标注 | 记录在案，需人工验证 |
| contour_deviation | 轮廓形状偏差 | 轮廓拟合误差 > 公差 |
| bounding_box_mismatch | 整体尺寸不匹配 | 包围盒尺寸偏差 > 公差 |
| missing_contour | 2D轮廓在3D中缺失 | 线段/弧在投影中找不到对应 |

## 尺寸类型识别

| 类型 | 示例 | 识别规则 |
|------|------|---------|
| diameter | Ø10, Φ10, DIA10 | Ø/Φ/DIA前缀 |
| radius | R10 | R前缀 |
| angular | 45° | 数字+° |
| linear | 10, 10.5 | 纯数字 |

## 几何公差类型

| 英文类型 | 中文名称 | 关键字 |
|----------|---------|--------|
| position | 位置度 | 位置度, ⓞ, ◎ |
| perpendicularity | 垂直度 | 垂直度, ⊥ |
| parallelism | 平行度 | 平行度, ∥ |
| angularity | 倾斜度 | 倾斜度 |
| flatness | 平面度 | 平面度, □, ⿹ |
| straightness | 直线度 | 直线度 |
| circularity | 圆度 | 圆度, ⧠ |
| cylindricity | 圆柱度 | 圆柱度, ⌭ |
| concentricity | 同轴度 | 同轴度 |
| symmetry | 对称度 | 对称度 |
| circular_runout | 圆跳动 | 圆跳动 |
| totalrunout | 全跳动 | 全跳动 |
| profile | 轮廓度 | 轮廓度 |

## 严重性定义

| 级别 | 触发条件 | 处理建议 |
|------|---------|---------|
| CRITICAL | 偏差 > 5倍公差 或 关键尺寸缺失 | 必须修改 |
| WARNING | 偏差 > 1倍公差 | 建议核查 |
| INFO | 偏差 < 1倍公差 或 几何公差需人工验证 | 仅供参考 |

## 公差配置

默认公差: ±0.1mm

可通过 `--tolerance` 参数调整:
- 精密零件: 0.01~0.05mm
- 一般零件: 0.1mm
- 粗加工件: 0.5~1.0mm
