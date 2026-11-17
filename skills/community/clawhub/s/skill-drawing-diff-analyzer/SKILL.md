---
name: 图纸对比审核技能
slug: drawing-diff-analyzer
displayName: 图纸对比审核技能
description: 自动对比2D图纸与3D模型的尺寸、轮廓差异；输出JSON和Markdown格式差异报告；支持直径符号和几何公差识别；适用于设计评审阶段快速发现图纸不一致问题
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 图纸差异分析器 (Drawing Diff Analyzer)

## 任务目标
- 本 Skill 用于：设计评审阶段自动检测2D工程图与3D模型的差异
- 能力包含：图纸解析（支持直径Ø、半径R、几何公差识别）、特征提取、尺寸对比、轮廓对比、Markdown报告生成
- 触发条件：用户提供2D图纸和3D模型文件，要求对比差异

## 前置准备
- 依赖说明：
  - 2D解析：ezdxf(DWG/DXF)、pdfplumber+fitz(PDF)
  - 3D解析：numpy-stl/trimesh(STL)、cadquery(STEP/IGES)
- 工作目录准备：用户需提供2D和3D文件的相对路径

## 操作步骤

### 标准流程

1. **解析2D图纸** — 提取轮廓、尺寸标注和几何公差
   - 输入：2D图纸文件（DWG/DXF/PDF）
   - 脚本调用：`python scripts/parse_2d.py --input <2d_file> --output features_2d.json`
   - 输出：`features_2d.json`
     - `entities`：轮廓线、圆、弧等几何实体
     - `dimensions`：尺寸标注（线性、角度、直径Ø、半径R）
     - `geometric_tolerances`：几何公差（位置度、垂直度、平面度等）

2. **解析3D模型** — 提取几何特征和尺寸
   - 输入：3D模型文件（STL/STEP/IGES）
   - 脚本调用：`python scripts/parse_3d.py --input <3d_file> --output features_3d.json`
   - 输出：`features_3d.json`（顶点、边、面、包围盒尺寸）

3. **差异对比** — 执行多维度对比并生成报告
   - 脚本调用：`python scripts/compare.py --features-2d features_2d.json --features-3d features_3d.json --output diff_report --tolerance 0.1`
   - 对比维度：
     - 尺寸偏差：标注值 vs 3D测量值
     - 轮廓偏差：2D投影 vs 3D轮廓
     - 几何公差：记录并标注（需人工验证）
   - 输出：
     - `diff_report.json` — 结构化差异报告
     - `diff_report.md` — Markdown格式差异报告

### 可选参数
- `--tolerance`：尺寸公差阈值，默认0.1mm

## 尺寸与公差类型支持

### 尺寸类型
| 类型 | 示例 | 识别方式 |
|------|------|---------|
| 线性尺寸 | 10, 10.5, 100 | 纯数字 |
| 直径 | Ø10, Φ10, DIA10 | Ø/Φ/DIA前缀 |
| 半径 | R10 | R前缀 |
| 角度 | 45° | 数字+° |
| 带公差 | 10±0.05 | ±数值 |

### 几何公差类型
| 类型 | 关键字 | Unicode |
|------|--------|---------|
| 位置度 | 位置度, position | ⓞ, ◎ |
| 垂直度 | 垂直度, perpendicularity | ⊥ |
| 平行度 | 平行度, parallelism | ∥ |
| 平面度 | 平面度, flatness | □, ⿹ |
| 直线度 | 直线度, straightness | - |
| 圆度 | 圆度, circularity | ⧠ |
| 圆柱度 | 圆柱度, cylindricity | ⌭ |
| 同轴度 | 同轴度, concentricity | ◎ |
| 对称度 | 对称度, symmetry | - |
| 倾斜度 | 倾斜度, angularity | ∠ |

## 使用示例

### 示例1：基本对比流程
- 场景/输入：用户有 `blueprint.pdf` 和 `model.stl`，需要对比
- 预期产出：`diff_report.json` 和 `diff_report.md`
- 关键要点：按顺序执行解析→对比

### 示例2：精密对比（调整阈值）
- 场景/输入：对精密零件，要求±0.05mm公差
- 预期产出：更严格的差异检测结果
- 关键要点：`--tolerance 0.05`

## 资源索引

- 脚本：见 [scripts/parse_2d.py](scripts/parse_2d.py)（解析DWG/DXF/PDF）
- 脚本：见 [scripts/parse_3d.py](scripts/parse_3d.py)（解析STL/STEP/IGES）
- 脚本：见 [scripts/compare.py](scripts/compare.py)（对比并生成JSON+Markdown报告）
- 参考：见 [references/format-guide.md](references/format-guide.md)（格式详解）

## 注意事项

- 3D到2D投影默认使用正交投影
- 几何公差需要人工测量验证，3D模型无法自动检测
- 对比结果依赖文件质量和坐标系完整性，异常文件需人工确认

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
