---
name: windows-screenshot-ocr
description: Windows全屏截图（自动标记鼠标位置）+ 原生OCR文字识别。完全本地运行，无需联网，无需API Key。适用于需要截图分析屏幕内容、自动化OCR识别的场景。
---

# Windows Screenshot + OCR Skill

本技能提供两个核心功能：
1. **全屏截图**：截取当前屏幕并在截图上标记鼠标位置（红色准星）
2. **OCR文字识别**：使用 Windows 系统内置 OCR 引擎识别图片中的文字

## 环境要求

- Windows 10 / 11（64位）
- Python 3.8+
- 已安装中文/英文 OCR 语言包（系统设置 → 语言）

## 安装依赖

```bash
pip install mss pyautogui Pillow
pip install winrt
```

## 使用方法

### 截图
```bash
python screenshot.py
```
截图保存在 `E:\桌面\auto_screenshot\`，文件名带时间戳。

### OCR识别
```bash
python windows_ocr.py
```
修改脚本中的 `image_path` 为目标图片路径，识别结果保存到 `ocr_result.txt`。

## 文件说明

- `screenshot.py` — 截图脚本，带鼠标位置标记
- `windows_ocr.py` — OCR识别脚本，使用Windows原生引擎
- `README.md` — 详细说明文档

## 注意事项

- 截图路径默认为 `E:\桌面\auto_screenshot\`，可在脚本中修改 `save_folder`
- OCR 依赖 Windows 系统语言包，如识别失败请在系统设置中添加对应语言
- 完全本地运行，不联网，不上传任何数据

## 作者

QClaw AI Assistant（由用户对话生成，2026-03-26）
