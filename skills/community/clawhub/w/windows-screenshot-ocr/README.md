# windows-screenshot-ocr

> Windows 全屏截图 + 鼠标标记 + 原生 OCR 文字识别工具
> 作者：QClaw AI Assistant（由用户对话生成）

## 功能介绍

### 1. screenshot.py — 截图并标记鼠标位置
- 截取当前全屏
- 自动在截图上标记鼠标所在位置（红色准星）
- 文件名带时间戳，不会覆盖历史截图
- 保存到指定文件夹

### 2. windows_ocr.py — 图片文字识别（OCR）
- 使用 Windows 系统内置 OCR 引擎（无需联网、无需API）
- 支持中英文识别
- 识别结果保存为 txt 文件

---

## 环境要求

- Windows 10 / 11（64位）
- Python 3.8+
- Windows 已安装中文/英文 OCR 语言包（系统设置 → 语言）

---

## 安装依赖

```bash
pip install mss pyautogui Pillow
pip install winrt
```

---

## 使用方法

### 截图
```bash
python screenshot.py
```
截图保存在 `E:\桌面\auto_screenshot\` 目录，文件名格式：`screen_20260326_113827.png`

### OCR识别
```bash
python windows_ocr.py
```
修改脚本中的 `image_path` 为你要识别的图片路径，识别结果保存到 `ocr_result.txt`

---

## 文件结构

```
windows-screenshot-ocr/
├── screenshot.py       # 截图脚本
├── windows_ocr.py      # OCR识别脚本
├── README.md           # 说明文档
```

---

## 注意事项

1. 截图保存路径默认为 `E:\桌面\auto_screenshot\`，可在脚本中修改 `save_folder`
2. OCR 依赖 Windows 系统语言包，如识别失败请在"系统设置 → 时间和语言 → 语言"中添加对应语言
3. 本工具完全本地运行，不联网，不上传任何数据

---

## License

MIT — 自由使用、修改、分发
