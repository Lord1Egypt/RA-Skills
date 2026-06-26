---
name: receipt-word-tool
description: |
  付款截图Word排版工具。批量处理微信/支付宝付款截图，EasyOCR自动识别实付金额，生成带缩略图、金额、小计、总计的Word文档。
  完整GUI工具，支持手动修正金额、缩略图预览。包含源码、维护指南、国内离线模型下载方案。
  适用场景：
  - "帮我处理付款截图"（批量OCR识别+Word排版）
  - "修正一下识别错误的金额"（手动修正OCR结果）
  - "生成报销文档"（带缩略图+金额+小计+总计的Word文档）
metadata:
  openclaw:
    emoji: "🧾"
    author: "以七"
version: 1.0.0
---

# 付款截图 Word 排版工具

一款 tkinter GUI 工具，批量将付款截图（微信/支付宝）转换为格式化 Word 报销文档。用户选择截图文件夹后，EasyOCR 自动识别每张图的实付金额，支持手动修正，一键生成包含缩略图、金额标注、小计和总计的 Word 文档。

## 核心功能

1. 用户选择付款截图文件夹（`.jpg/.png/.bmp/.gif/.webp/.tiff`）
2. EasyOCR 读取每张图，自动提取最终实付金额
3. 用户可手动修正任何识别错误的金额
4. 生成格式化 Word 文档：
   - 每页 2列 × 3行 = 6 张图
   - 每张图下方居中显示金额（红色加粗）
   - 每 18 张（3页）插入蓝色小计行
   - 文档末尾红色加粗总计

## 文件结构

| 文件 | 用途 |
|---|---|
| `scripts/receipt_word_tool.py` | 完整可运行的 GUI 工具源码 |
| `scripts/启动付款排版工具.bat` | Windows 一键启动脚本 |
| `references/maintenance_guide.md` | 技术维护记录（14个已修复问题） |
| `references/easyocr_offline_setup.md` | 国内离线模型下载指南 |

## 运行方式

```bash
python scripts/receipt_word_tool.py
```

**依赖**：`easyocr`, `Pillow`, `python-docx`, `numpy`
