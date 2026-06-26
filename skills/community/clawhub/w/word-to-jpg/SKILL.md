---
name: word-to-jpg
description: Convert Word documents (.docx/.doc) to high-quality JPG images with 100% formatting fidelity. Uses Word COM interface to export PDF, then PyMuPDF renders at 300 DPI.
allowed-tools: Bash(word-to-jpg:*)
version: 1.0.0
license: MIT-0
---

# word-to-jpg Skill

将 Word 文档转换为高质量 JPG 图片（300 DPI，100% 格式保真）。

## 触发词

当用户提到以下任一短语时，触发此技能：
- "转成图片" / "转为 JPG"
- "word 转图片" / "doc 转图片"
- "转成高质量图片"
- "文档转图片"

## 功能

- 自动查找最新接收的 Word 文档
- Word 原生导出 PDF（100% 格式保真）
- PyMuPDF 渲染为 300 DPI JPG
- 支持中文文件名、多页文档

## 依赖

首次使用安装：
```powershell
pip install comtypes pymupdf -q
```

## 使用方法

**直接转换**（接收文件后）:
```
转成图片
```

**指定文件**:
```
word-to-jpg C:\path\to\document.docx
```

**指定目录**（转换最新文件）:
```
word-to-jpg C:\path\to\docs\
```

## 输出

- **目录**: `~/.openclaw/media/outbound/word-images`
- **命名**: `page_1.jpg`, `page_2.jpg`, ...
- **分辨率**: 2382×3368 (300 DPI)
- **质量**: JPG 95%

## 原理

1. **Word → PDF**: comtypes 调用 Word COM 接口静默导出
2. **PDF → JPG**: PyMuPDF 4 倍缩放渲染 (72×4=288 DPI)

## 要求

- ✅ Microsoft Word（必需）
- ❌ WPS（不兼容）
- ⚠️ 中文文件名自动处理（复制到临时英文路径）

## 常见问题

**缺模块**: `pip install comtypes pymupdf -q`
**无 Word**: 需安装 Microsoft Word（WPS 不兼容）
**速度慢**: 首次启动 Word 较慢，后续正常
**调 DPI**: 修改脚本 zoom 参数（4.0=300 DPI, 2.0=150 DPI）

## 文件结构

```
~/.openclaw/skills/word-to-jpg/
├── SKILL.md
└── scripts/
    └── word-to-jpg-converter.py
```

## 更新日志

- **1.0.0** (2026-03-30): 初始版本
  - Word → PDF → JPG 两步转换
  - 300 DPI 高质量输出
  - 中文文件名自动处理
