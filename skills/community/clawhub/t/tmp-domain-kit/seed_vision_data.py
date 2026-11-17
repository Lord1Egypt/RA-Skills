"""
视觉方向测试数据录入
录入缺陷类型、视觉模型及相关关系
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from storage.knowledge_store import KnowledgeStore
from utils.id_generator import generate_entity_id, generate_relation_id

store = KnowledgeStore(str(Path(__file__).parent / "storage"))

# ===== 缺陷类型 =====

# 1. 表面划痕
scratch = {
    "name": "表面划痕",
    "category": "表面",
    "characteristics": ["线性痕迹", "深度不一", "方向随机", "长度0.5-50mm"],
    "severity_level": "major"
}
scratch_id = generate_entity_id("DefectType", scratch, "docs/vision/defect_catalog.pdf")
store.add_entity(scratch_id, "DefectType", scratch,
    provenance={"source_type": "document", "source_path": "docs/vision/defect_catalog.pdf",
                "extracted_at": "2026-07-12T11:00:00Z", "confidence": 0.95},
    tags=["表面划痕", "表面缺陷", "划痕", "缺陷", "视觉", "视觉检测", "表面检测"])

# 2. 尺寸偏差
dimension = {
    "name": "尺寸偏差",
    "category": "尺寸",
    "characteristics": ["长/宽/高超出公差", "对称度偏差", "圆度偏差"],
    "severity_level": "critical"
}
dimension_id = generate_entity_id("DefectType", dimension, "docs/vision/defect_catalog.pdf")
store.add_entity(dimension_id, "DefectType", dimension,
    provenance={"source_type": "document", "source_path": "docs/vision/defect_catalog.pdf",
                "extracted_at": "2026-07-12T11:00:00Z", "confidence": 0.95},
    tags=["尺寸偏差", "尺寸缺陷", "偏差", "缺陷", "视觉", "视觉检测", "测量"])

# 3. 颜色异常
color = {
    "name": "颜色异常",
    "category": "颜色",
    "characteristics": ["色差ΔE>3", "局部变色", "色差均匀性差"],
    "severity_level": "minor"
}
color_id = generate_entity_id("DefectType", color, "docs/vision/defect_catalog.pdf")
store.add_entity(color_id, "DefectType", color,
    provenance={"source_type": "document", "source_path": "docs/vision/defect_catalog.pdf",
                "extracted_at": "2026-07-12T11:00:00Z", "confidence": 0.92},
    tags=["颜色异常", "颜色缺陷", "色差", "缺陷", "视觉", "视觉检测"])

# 4. 表面凹坑
dent = {
    "name": "表面凹坑",
    "category": "表面",
    "characteristics": ["局部凹陷", "直径0.1-5mm", "深度<0.5mm"],
    "severity_level": "major"
}
dent_id = generate_entity_id("DefectType", dent, "docs/vision/defect_catalog.pdf")
store.add_entity(dent_id, "DefectType", dent,
    provenance={"source_type": "document", "source_path": "docs/vision/defect_catalog.pdf",
                "extracted_at": "2026-07-12T11:00:00Z", "confidence": 0.90},
    tags=["表面凹坑", "表面缺陷", "凹坑", "缺陷", "视觉", "视觉检测"])

# 5. 形状变形
deform = {
    "name": "形状变形",
    "category": "形状",
    "characteristics": ["翘曲", "弯曲", "扭曲", "平面度超差"],
    "severity_level": "critical"
}
deform_id = generate_entity_id("DefectType", deform, "docs/vision/defect_catalog.pdf")
store.add_entity(deform_id, "DefectType", deform,
    provenance={"source_type": "document", "source_path": "docs/vision/defect_catalog.pdf",
                "extracted_at": "2026-07-12T11:00:00Z", "confidence": 0.88},
    tags=["形状变形", "形状缺陷", "变形", "缺陷", "视觉", "视觉检测"])

# ===== 视觉模型 =====

# 1. YOLO 目标检测
yolo = {
    "name": "YOLOv8-Defect",
    "algorithm": "YOLOv8",
    "applicable_defects": ["表面划痕", "表面凹坑", "形状变形"],
    "precision": 0.92,
    "recall": 0.89,
    "hardware_requirement": {"gpu": "NVIDIA T4+", "resolution": "2448x2048", "fps": 30}
}
yolo_id = generate_entity_id("VisionModel", yolo, "docs/vision/model_specs.md")
store.add_entity(yolo_id, "VisionModel", yolo,
    provenance={"source_type": "document", "source_path": "docs/vision/model_specs.md",
                "extracted_at": "2026-07-12T11:30:00Z", "confidence": 0.93},
    tags=["YOLO", "YOLOv8", "目标检测", "视觉", "视觉模型", "模型"])

# 2. ResNet 图像分类
resnet = {
    "name": "ResNet50-Classifier",
    "algorithm": "ResNet-50",
    "applicable_defects": ["颜色异常", "表面划痕"],
    "precision": 0.95,
    "recall": 0.91,
    "hardware_requirement": {"gpu": "NVIDIA Jetson Nano+", "resolution": "640x480", "fps": 15}
}
resnet_id = generate_entity_id("VisionModel", resnet, "docs/vision/model_specs.md")
store.add_entity(resnet_id, "VisionModel", resnet,
    provenance={"source_type": "document", "source_path": "docs/vision/model_specs.md",
                "extracted_at": "2026-07-12T11:30:00Z", "confidence": 0.91},
    tags=["ResNet", "ResNet50", "图像分类", "视觉", "视觉模型", "模型"])

# 3. 传统视觉测量
traditional = {
    "name": "VisionPro-Measure",
    "algorithm": "传统机器视觉(边缘检测+模板匹配)",
    "applicable_defects": ["尺寸偏差", "形状变形"],
    "precision": 0.98,
    "recall": 0.96,
    "hardware_requirement": {"camera": "Basler ace2", "lens": "远心镜头", "lighting": "同轴光"}
}
traditional_id = generate_entity_id("VisionModel", traditional, "docs/vision/model_specs.md")
store.add_entity(traditional_id, "VisionModel", traditional,
    provenance={"source_type": "document", "source_path": "docs/vision/model_specs.md",
                "extracted_at": "2026-07-12T11:30:00Z", "confidence": 0.95},
    tags=["传统视觉", "VisionPro", "测量", "视觉", "视觉模型", "模型", "精度"])

# ===== 关系 =====

# VisionModel detects DefectType
# YOLO → 表面划痕, 表面凹坑, 形状变形
for defect_id in [scratch_id, dent_id, deform_id]:
    rel_id = generate_relation_id(yolo_id, defect_id, "detects")
    store.add_relation(rel_id, yolo_id, defect_id, "detects", confidence=0.9,
        provenance={"source_path": "docs/vision/model_specs.md"})

# ResNet → 颜色异常, 表面划痕
for defect_id in [color_id, scratch_id]:
    rel_id = generate_relation_id(resnet_id, defect_id, "detects")
    store.add_relation(rel_id, resnet_id, defect_id, "detects", confidence=0.85,
        provenance={"source_path": "docs/vision/model_specs.md"})

# Traditional → 尺寸偏差, 形状变形
for defect_id in [dimension_id, deform_id]:
    rel_id = generate_relation_id(traditional_id, defect_id, "detects")
    store.add_relation(rel_id, traditional_id, defect_id, "detects", confidence=0.95,
        provenance={"source_path": "docs/vision/model_specs.md"})

print("视觉方向数据录入完成:")
print(f"  DefectType: 5 个 (表面划痕, 尺寸偏差, 颜色异常, 表面凹坑, 形状变形)")
print(f"  VisionModel: 3 个 (YOLOv8, ResNet50, VisionPro-Measure)")
print(f"  关系: detects (8条)")
