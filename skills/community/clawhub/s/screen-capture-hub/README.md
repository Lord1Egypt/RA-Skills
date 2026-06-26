# OPENCLAW(龙虾)-屏幕查看器

一个功能强大的屏幕截图、OCR识别和屏幕分析技能包，专为AI助手设计。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ✨ 功能特性

- **🎯 全屏/区域截图** - 灵活捕获屏幕内容
- **🔍 OCR文字识别** - 提取屏幕文字，支持多语言
- **📊 屏幕分析** - 查找特定文字、颜色、检测边缘
- **⚡ 快速操作** - 简化的命令行界面
- **🔄 定时监控** - 自动定时截图和变化检测
- **📁 多种格式输出** - 支持PNG、JSON、TXT等格式
- **🌍 跨平台** - Windows、macOS、Linux全支持

## 🚀 快速开始

### 一键安装（推荐）

运行一键安装脚本，自动安装所有依赖和OCR引擎：

```bash
# 运行安装脚本
python scripts/setup.py
```

### 手动安装

#### 1. 安装Python依赖库

**基础依赖（必需）** - 屏幕截图功能需要：
```bash
pip install pillow pyautogui
```

**OCR功能（可选）** - 文字识别功能需要：
```bash
pip install pytesseract
```

**图像分析（可选）** - 高级屏幕分析功能需要：
```bash
pip install opencv-python numpy
```

#### 2. 安装Tesseract OCR引擎（OCR功能必需）

**Windows（推荐方法）**：
```bash
# 自动下载和安装
python scripts/install_tesseract.py
```

**Windows（手动方法）**：
1. 访问：https://github.com/UB-Mannheim/tesseract/wiki
2. 下载最新的 `.exe` 安装程序
3. 运行安装程序，使用默认设置

**macOS**：
```bash
brew install tesseract
```

**Linux**：
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim
```

### 验证安装

运行测试脚本验证所有功能：
```bash
# 测试屏幕截图功能
python scripts/test_screenshot.py

# 测试OCR功能
python scripts/test_ocr.py
```

### 基础使用

```bash
# 快速截图
python scripts/quick_capture.py

# 查看屏幕信息
python scripts/screenshot.py --list-displays

# 区域截图
python scripts/screenshot.py --region "0,0,500,500" --output region.png

# OCR文字识别
python scripts/ocr_screenshot.py --text-output screen_text.txt

# 屏幕分析
python scripts/analyze_screen.py --task screen_info
```

## 📖 详细文档

### 脚本说明

| 脚本 | 功能 | 示例 |
|------|------|------|
| `quick_capture.py` | 快速截图工具 | `python quick_capture.py -o screenshot.png` |
| `screenshot.py` | 完整截图工具 | `python screenshot.py --region "100,100,500,500"` |
| `ocr_screenshot.py` | OCR文字识别 | `python ocr_screenshot.py --lang chi_sim` |
| `analyze_screen.py` | 屏幕分析 | `python analyze_screen.py --task find_text --text "搜索词"` |
| `test_screenshot.py` | 环境测试 | `python test_screenshot.py` |
| `setup.py` | 安装脚本 | `python setup.py` |

### 参数说明

#### 截图参数
- `--output, -o`: 输出文件路径
- `--region, -r`: 截图区域 (x1,y1,x2,y2)
- `--list-displays, -l`: 显示屏幕信息

#### OCR参数
- `--text-output, -t`: 文字输出文件
- `--lang, -l`: OCR语言 (默认: eng+chi_sim)
- `--list-langs`: 显示支持的语言

#### 分析参数
- `--task, -t`: 分析任务 (screen_info, find_text, find_color, detect_edges)
- `--text`: 要搜索的文字
- `--color`: 要搜索的颜色 (#RRGGBB)
- `--tolerance`: 颜色匹配容差 (0-255)

## 🎯 使用示例

### 1. 基本截图
```bash
# 全屏截图
python scripts/quick_capture.py

# 指定区域截图
python scripts/screenshot.py --region "100,100,600,400" --output window.png

# 带时间戳的截图
python scripts/quick_capture.py -o screenshot_$(date +%Y%m%d_%H%M%S).png
```

### 2. OCR文字提取
```bash
# 提取全屏文字
python scripts/ocr_screenshot.py --text-output full_text.txt

# 提取中文文字
python scripts/ocr_screenshot.py --lang chi_sim --text-output chinese.txt

# 提取特定区域文字
python scripts/ocr_screenshot.py --region "200,200,800,600" --text-output region_text.txt
```

### 3. 屏幕分析
```bash
# 获取屏幕信息
python scripts/analyze_screen.py --task screen_info --output info.json

# 查找特定文字
python scripts/analyze_screen.py --task find_text --text "错误" --output errors.json

# 查找特定颜色
python scripts/analyze_screen.py --task find_color --color "#FF0000" --output red_items.json

# 检测屏幕边缘
python scripts/analyze_screen.py --task detect_edges --output edges.png
```

### 4. 高级应用
```python
# 定时截图监控
import time
from datetime import datetime
from PIL import ImageGrab

for i in range(10):  # 每5秒截图一次，共10次
    screenshot = ImageGrab.grab()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot.save(f"monitor_{timestamp}.png")
    time.sleep(5)
```

## 🔧 API参考

### Python API
```python
from PIL import ImageGrab
import pyautogui

# 获取屏幕信息
screen_width, screen_height = pyautogui.size()
mouse_x, mouse_y = pyautogui.position()

# 截图
screenshot = ImageGrab.grab()  # 全屏
region_screenshot = ImageGrab.grab(bbox=(100, 100, 500, 500))  # 区域

# OCR识别
import pytesseract
text = pytesseract.image_to_string(screenshot, lang='eng+chi_sim')
```

## 📁 项目结构

```
screen-capture-hub/
├── SKILL.md              # 技能定义文件
├── README.md             # 项目文档
├── package.json          # 包元数据
├── LICENSE               # MIT许可证
├── CHANGELOG.md          # 版本日志
├── requirements.txt      # Python依赖
├── INSTALL.md            # 安装指南
├── scripts/              # Python脚本
│   ├── quick_capture.py
│   ├── screenshot.py
│   ├── ocr_screenshot.py
│   ├── analyze_screen.py
│   ├── test_screenshot.py
│   ├── setup.py
│   └── __init__.py
├── references/           # 参考文档
│   └── usage_examples.md
└── assets/              # 静态资源
    └── (图标、模板等)
```

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 开发设置
```bash
# 克隆仓库
git clone https://github.com/your-username/screen-capture-hub.git

# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python scripts/test_screenshot.py
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Pillow (PIL Fork)](https://python-pillow.org/) - Python图像处理库
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - 跨平台GUI自动化
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR引擎
- [OpenCV](https://opencv.org/) - 计算机视觉库

## 📞 支持

- **问题反馈**: [GitHub Issues](https://github.com/your-username/screen-capture-hub/issues)
- **功能请求**: 开启新的Issue
- **文档**: 查看 [references/](references/) 目录

## 🔗 相关链接

- [OpenClaw Hub](https://hub.openclaw.org/) - AI技能市场
- [Python官方文档](https://docs.python.org/3/)
- [Pillow文档](https://pillow.readthedocs.io/)
- [PyAutoGUI文档](https://pyautogui.readthedocs.io/)

---

**Screen Capture Hub** - 让屏幕操作更智能！ 🚀