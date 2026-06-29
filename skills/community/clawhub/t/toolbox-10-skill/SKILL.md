---
name: 实用工具匣
slug: toolbox-10-skill
description: 集合四大高频实用图像工具：去水印/OCR文字识别/图片压缩/标准证件照生成。一站式解决日常图片处理需求。
version: "1.0.0"
tags: [toolbox, image-processing, ocr, watermark-removal, id-photo, compression, utility]
license: MIT
allowed-tools:
  - Bash(python3*)
  - Bash(pip*)
  - Read
  - Write
requires:
  bins:
    - python3
  env:
    - EASYOCR_MODULE_PATH
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - EASYOCR_MODULE_PATH
---

# 实用工具匣 — AI 图像处理四合一 Skill

一站式解决四大高频图像处理需求：去水印、OCR文字识别、图片压缩、标准证件照生成。

## 触发词

用户自然语言中包含以下关键词任一即触发本技能：
- **去水印**: 去水印、消除水印、移除水印、水印去除、remove watermark
- **OCR**: OCR、文字识别、提取文字、图片转文字、识字、识别文字
- **图片压缩**: 图片压缩、压缩图片、缩小图片体积、压缩照片、compress image
- **证件照**: 证件照、一寸照、二寸照、ID照片、护照照片、签证照、换底色、红底照片、蓝底照片、白底照片

## 四大工具概览

| 工具 | 脚本 | 核心能力 |
|------|------|---------|
| 🔧 去水印 | `scripts/remove_watermark.py` | 自动检测水印区域并修复，支持手动选区 |
| 📝 OCR识别 | `scripts/ocr_recognize.py` | 中英文混合识别，输出文字+位置坐标 |
| 📦 图片压缩 | `scripts/compress_image.py` | 智能压缩，支持质量/尺寸/格式调节 |
| 📸 证件照 | `scripts/id_photo.py` | 去背景+裁剪+换底色，支持一寸/二寸等规格 |

## 工作流程

### 1. 接收用户意图
识别用户要使用哪个（或哪些）工具，确认输入文件路径和参数。

### 2. 确认输入
- 检查用户提供的图片文件是否存在
- 如果用户没有明确指定参数，使用智能默认值
- 对于去水印：如用户未指定水印区域，自动检测
- 对于图片压缩：默认质量 85%，保持原格式
- 对于证件照：默认一寸（295×413px），蓝底
- 对于 OCR：自动识别中英文

### 3. 执行脚本
调用对应 Python 脚本，等待完成。所有脚本返回 JSON 格式结果。

### 4. 展示结果
- 输出文件路径
- 关键指标（压缩率、识别文字摘要、证件照规格等）
- 如有异常或质量不佳，主动提醒用户

## 依赖安装

首次使用前需要安装 Python 依赖：

```bash
python3 -m pip install easyocr opencv-python-headless Pillow rembg numpy onnxruntime
```

> **注意**: `easyocr` 首次运行会自动下载模型文件，需要联网，模型约 100-300MB。

## AI 使用规则

1. **优先使用脚本**: 所有图像处理操作通过 `scripts/` 下的 Python 脚本完成，不要尝试用纯 Shell 命令。
2. **传递完整路径**: 脚本的所有输入输出路径使用绝对路径。
3. **检查依赖**: 首次使用或脚本报错 `ModuleNotFoundError` 时，自动安装依赖。
4. **处理结果**: 读取脚本的 stdout JSON 输出，解析后以友好方式呈现给用户。
5. **错误处理**: 脚本返回非零退出码时，将 stderr 展示给用户并提供解决建议。
6. **去水印交互**: 去水印时使用 `--auto` 自动检测模式；用户指定区域时用 `--x1 --y1 --x2 --y2` 参数。
7. **证件照底色**: 底色参数 `--bg` 支持: red(红), blue(蓝), white(白)，默认 blue。
8. **压缩策略**: 默认平衡模式(quality=85)，用户可指定 `--quality 30-95` 或 `--max-size 200`(KB)。
