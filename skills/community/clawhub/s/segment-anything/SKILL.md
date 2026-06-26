---
name: sam-segmentation-zh
description: 使用 SAM（Segment Anything Model）去除图像背景，将前景主体提取为透明 PNG。适用于去除背景、抠图、提取前景主体或图像分割等需求。
metadata:
  openclaw:
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: pillow
      - kind: uv
        package: numpy
      - kind: uv
        package: torch
      - kind: uv
        package: torchvision
---

# SAM 背景去除

使用 Meta 的 Segment Anything Model 从图像中提取前景主体，输出透明背景的 PNG 文件。

## 快速开始

```bash
python3 scripts/segment.py <输入图像> <输出.png>
```

默认以图像中心作为前景提示点——适用于主体居中的人像和产品图。

## 参数说明

| 参数 | 说明 | 默认值 |
|---|---|---|
| `input` | 输入图像路径 | 必填 |
| `output` | 输出 PNG 路径（单目标模式）或目录（`--all` 模式） | 必填 |
| `--model` | 模型大小：`vit_b`（快速）· `vit_l`（中等）· `vit_h`（最佳质量） | `vit_h` |
| `--checkpoint` | 本地权重文件路径；省略时自动下载 | 自动 |
| `--points` | 前景提示点，格式为 `x,y`，可指定多个 | 中心点 |
| `--all` | 网格扫描模式：提取所有独立元素 | 关闭 |
| `--grid` | `--all` 模式的网格密度；16 表示 16×16=256 个探测点 | `16` |
| `--iou-thresh` | 接受掩码的最低预测 IoU（`--all` 模式） | `0.88` |
| `--min-area` | 掩码最小面积占图像比例（`--all` 模式） | `0.001` |

## 使用示例

```bash
# 基础背景去除（自动下载 vit_h 约 2.5GB）
python3 scripts/segment.py photo.jpg output.png

# 主体偏离中心时指定提示点
python3 scripts/segment.py photo.jpg output.png --points 320,240

# 多提示点 + 轻量模型
python3 scripts/segment.py photo.jpg output.png --model vit_b --points 320,240 400,300

# 提取所有元素（每个元素输出一个 PNG）
python3 scripts/segment.py photo.jpg ./elements/ --all

# 使用更密集的网格捕获小物体
python3 scripts/segment.py photo.jpg ./elements/ --all --grid 32

# 使用本地权重文件
python3 scripts/segment.py photo.jpg output.png --checkpoint /path/to/sam_vit_h_4b8939.pth
```

## 依赖安装

`segment_anything` 首次运行时自动安装，也可手动安装：

```bash
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install pillow numpy torch torchvision
```

## 工作流程

1. 用户提供图像路径
2. 询问是否需要提示点（主体偏离中心时）
3. 运行脚本；权重文件首次使用时自动下载至 `~/.cache/sam/`
4. 输出透明背景的 PNG 文件

## 模型选择

| 模型 | 大小 | 速度 | 质量 |
|---|---|---|---|
| `vit_b` | ~375 MB | 最快 | 良好 |
| `vit_l` | ~1.25 GB | 中等 | 较好 |
| `vit_h` | ~2.5 GB | 较慢 | 最佳 |

有 GPU 时自动使用 CUDA 加速。
