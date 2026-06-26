---
name: openclaw-screen-viewer
displayName: OPENCLAW(龙虾)-屏幕查看器
description: 此技能应被用于任何需要捕获屏幕截图、分析屏幕内容或处理屏幕图像的任务。包括：使用Python PIL库捕获整个屏幕或特定区域的截图；保存截图到指定位置；分析截图中的文字内容（支持中英文OCR识别）；对截图进行基本图像处理（裁剪、旋转、调整大小）。当用户提到"屏幕截图"、"截屏"、"查看屏幕"或需要分析屏幕上的内容时，使用此技能。
version: 1.0.0
author: CodeBuddy User
license: MIT
keywords:
  - 屏幕截图
  - OCR识别
  - 文字提取
  - 屏幕分析
  - 图像处理
  - 中文识别
  - openclaw
categories:
  - 图像处理
  - OCR
  - 屏幕工具
  - AI助手
---

# OPENCLAW(龙虾)-屏幕查看器

## 概述

此技能提供了使用Python进行屏幕截图和图像处理的功能。它依赖于Pillow (PIL) 和pyautogui库来捕获屏幕内容，并可选择性地使用pytesseract进行OCR文字识别。

## 安装依赖

### 方法1：一键安装（推荐）
```bash
python scripts/setup.py
```

### 方法2：手动安装

**必需依赖**（基础功能）：
```bash
pip install pillow pyautogui
```

**可选依赖**（OCR功能）：
```bash
pip install pytesseract
```

**Tesseract OCR引擎**（OCR功能必需）：
- Windows: 运行 `python scripts/install_tesseract.py` 自动安装
- Windows (手动): 从 https://github.com/UB-Mannheim/tesseract/wiki 下载安装
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

**可选依赖**（高级分析功能）：
```bash
pip install opencv-python numpy
```

### 验证安装
```bash
# 检查所有依赖
python scripts/dependency_check.py

# 测试截图功能
python scripts/test_screenshot.py

# 测试OCR功能
python scripts/test_ocr.py

# 运行所有示例
python examples/run_examples.py
```

## 使用方法

### 基本屏幕截图

使用`scripts/screenshot.py`脚本捕获整个屏幕：

```python
python scripts/screenshot.py --output screenshot.png
```

捕获特定区域：
```python
python scripts/screenshot.py --output screenshot.png --region "100,100,500,500"
```

### 文字识别

使用`scripts/ocr_screenshot.py`脚本捕获屏幕并识别文字：

```python
python scripts/ocr_screenshot.py --output screenshot.png --text-output text.txt
```

### 分析屏幕内容

使用`scripts/analyze_screen.py`脚本进行更复杂的分析：

```python
python scripts/analyze_screen.py --task find_text --text "搜索词"
```

## 工作流程

当用户请求屏幕相关操作时：

1. **确定需求** - 明确用户需要的是截图、文字识别还是其他分析
2. **选择脚本** - 根据需求选择合适的脚本
3. **设置参数** - 配置输出路径、区域等参数
4. **执行脚本** - 运行相应的Python脚本
5. **处理结果** - 将结果展示给用户或进行进一步分析

## 常见任务

### 任务1：快速截图
- 使用：`scripts/screenshot.py`
- 参数：`--output` 指定输出文件路径
- 示例：捕获整个屏幕并保存为当前目录的screenshot.png

### 任务2：区域截图
- 使用：`scripts/screenshot.py`
- 参数：`--region "x1,y1,x2,y2"`
- 示例：捕获屏幕左上角500x500像素区域

### 任务3：屏幕文字提取
- 使用：`scripts/ocr_screenshot.py`
- 参数：`--text-output` 指定文本输出文件
- 示例：捕获屏幕并提取所有文字保存到text.txt

### 任务4：查找特定内容
- 使用：`scripts/analyze_screen.py`
- 参数：`--task find_text --text "搜索内容"`
- 示例：在屏幕上查找特定文字并高亮显示

## 注意事项

1. **权限**：某些应用程序可能需要管理员权限才能捕获其窗口内容
2. **性能**：高分辨率屏幕截图可能需要较多内存
3. **OCR准确性**：文字识别准确性受字体、背景、分辨率影响
4. **多显示器**：脚本默认捕获主显示器，多显示器环境需要特殊处理

## 故障排除

如果截图失败：
1. 检查Python库是否正确安装
2. 确认有足够的权限
3. 尝试降低分辨率或捕获特定区域

如果OCR识别不准确：
1. 确保Tesseract正确安装
2. 尝试预处理图像（二值化、去噪）
3. 指定语言参数（如`--lang chi_sim`用于简体中文）
