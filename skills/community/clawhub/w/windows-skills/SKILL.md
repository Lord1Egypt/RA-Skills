---
name: windows-skills
description: Windows desktop automation skills - screenshot capture, OCR text extraction, and image-based UI element location. Use when: (1) capturing screen content (2) extracting text from images (3) locating UI elements for automation
---

# Windows Desktop Automation

## Quick Start

### Dependencies
```bash
pip install mss pytesseract pillow pyautogui opencv-python numpy
```
Note: OCR requires [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed

### Core Features

#### 1. Screenshot
```python
from scripts.screenshot import capture_screen, capture_region, capture_window

# Full screen
capture_screen("output.png")

# Region (x, y, width, height)
capture_region(0, 0, 800, 600, "region.png")

# Window by title
capture_window("Notepad", "notepad.png")
```

#### 2. OCR (Text Recognition)
```python
from scripts.ocr import extract_text

# Extract text from image
text = extract_text("screenshot.png")
print(text)

# Specify language (chi_sim=Chinese, eng=English)
text = extract_text("screenshot.png", lang="chi_sim+eng")
```

#### 3. Image Location
```python
from scripts.image_locate import locate_on_screen, locate_all

# Find image position (returns center coordinates)
pos = locate_on_screen("button.png")
if pos:
    x, y, confidence = pos
    pyautogui.click(x, y)  # Click the found element

# Find all matches
positions = locate_all("icon.png")
```

## Scripts

| Script | Description |
|--------|-------------|
| `screenshot.py` | Screenshot capture |
| `ocr.py` | Text recognition |
| `image_locate.py` | Image-based element location |
| `helpers.py` | Common utilities |

## Notes

- Image location is sensitive to image similarity; keep screenshots consistent
- OCR quality depends on image quality and text clarity
- Tesseract path needs to be in system PATH or specified in code

---

# Windows 桌面自动化

## 快速开始

### 依赖安装
```bash
pip install mss pytesseract pillow pyautogui opencv-python numpy
```
注意：OCR 需要安装 [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

### 核心功能

#### 1. 截图
```python
from scripts.screenshot import capture_screen, capture_region, capture_window

# 全屏截图
capture_screen("output.png")

# 区域截图 (x, y, width, height)
capture_region(0, 0, 800, 600, "region.png")

# 窗口截图
capture_window("Notepad", "notepad.png")
```

#### 2. 文字识别 (OCR)
```python
from scripts.ocr import extract_text

# 从图片提取文字
text = extract_text("screenshot.png")
print(text)

# 指定语言 (chi_sim = 简体中文, eng = 英文)
text = extract_text("screenshot.png", lang="chi_sim+eng")
```

#### 3. 图像定位
```python
from scripts.image_locate import locate_on_screen, locate_all

# 查找图片位置 (返回中心坐标)
pos = locate_on_screen("button.png")
if pos:
    x, y, conf = pos
    pyautogui.click(x, y)  # 点击找到的元素

# 查找所有匹配位置
positions = locate_all("icon.png")
```

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `screenshot.py` | 截图功能 |
| `ocr.py` | 文字识别 |
| `image_locate.py` | 图像定位 |
| `helpers.py` | 公共工具 |

## 注意事项

- 图像定位对图片相似度敏感，建议截图时保持一致
- OCR 效果取决于图片质量和文字清晰度
- Tesseract 路径需要添加到系统 PATH 或在代码中指定
