---
name: "wine-desktop-automation"
description: "Controls desktop applications with mouse and keyboard automation. Invoke when user needs to automate GUI operations, control desktop software, or perform UI testing on Ubuntu+Wine environment."
---

# Wine Desktop Automation

Wine 桌面自动化技能，提供全面的鼠标和键盘操作控制。专门针对 Ubuntu + Wine 环境优化，支持 Linux 原生应用和 Wine 运行的 Windows 应用程序自动化。

## 使用场景

当用户需要以下功能时调用此技能：
- 自动化 GUI 操作（点击、输入、导航）
- 程序化控制桌面应用程序
- 执行 UI 测试或回归测试
- 通过 Wine 自动化 Windows 应用程序
- 图像识别和视觉自动化
- 自动化重复性桌面任务

## 核心功能

### 鼠标控制
- 移动鼠标到绝对或相对坐标
- 单击、双击、右键操作
- 拖拽功能
- 滚轮控制
- 可配置速度的平滑移动

### 键盘控制
- 文本输入和单个按键
- 特殊键支持（Enter、Tab、Esc 等）
- 键盘快捷键和组合键
- 按键和释放操作

### 窗口管理
- 通过标题或类名查找窗口
- 激活、最小化、最大化、关闭窗口
- 获取窗口位置和大小信息
- 支持 Wine 应用窗口
- 列出所有活动窗口

### 图像识别
- 使用图像模板在屏幕上查找元素
- 等待图像出现或消失
- 截屏功能
- 多重图像匹配和置信度
- 基于区域的图像搜索

### Wine 集成
- 通过 Wine 启动 Windows 应用程序
- 管理 Wine 进程
- 处理 Wine 特定的窗口行为
- 支持 Wine 虚拟桌面配置

## 快速开始

### 安装依赖

```bash
# 系统依赖（Ubuntu）
sudo apt-get install wine64 xdotool wmctrl scrot

# Python 依赖
pip install -r requirements.txt
```

### 基本使用

```python
# 鼠标操作
from scripts.mouse_controller import mouse
mouse.move(100, 200)
mouse.click()

# 键盘操作
from scripts.keyboard_controller import keyboard
keyboard.type('Hello, World!')
keyboard.hotkey('ctrl', 's')

# 窗口管理
from scripts.window_manager import window
window.activate('Notepad')

# 图像识别
from scripts.image_recognizer import image
button = image.find('button.png', confidence=0.9)

# Wine 应用
from scripts.wine_launcher import wine_launcher
wine_launcher.launch('notepad.exe')
```

## 使用示例

### 自动化记事本

```python
from scripts.wine_launcher import wine_launcher
from scripts.window_manager import window
from scripts.keyboard_controller import keyboard
import time

# 启动 Wine 记事本
wine_launcher.launch('notepad.exe')

# 等待窗口
window.wait_for_window('Notepad', timeout=10)
window.activate('Notepad')

# 输入文本
keyboard.type('Hello from Wine!')

# 保存文件
keyboard.hotkey('ctrl', 's')
time.sleep(1)
keyboard.type('demo.txt')
keyboard.enter()
```

### 图像识别自动化

```python
from scripts.image_recognizer import image
from scripts.mouse_controller import mouse

# 查找并点击按钮
button = image.find('submit_button.png', confidence=0.9)
if button:
    mouse.click(button.center_x, button.center_y)

# 等待加载完成
image.wait_for('loading_complete.png', timeout=10)
```

## 配置

通过 `utils/config.py` 配置：
- 鼠标移动速度和延迟
- 键盘输入延迟
- 图像识别置信度阈值
- Wine 路径和前缀设置
- 日志级别和输出

## 系统要求

- Ubuntu 20.04 或更高版本
- Wine 5.0 或更高版本
- Python 3.8 或更高版本
- X11 显示服务器
- 必需系统工具：xdotool, wmctrl, scrot

## 最佳实践

1. **尽可能使用图像识别**以获得更稳健的自动化
2. **在操作之间添加适当延迟**以允许 UI 响应
3. **优雅处理异常**当窗口或元素未找到时
4. **使用相对坐标**处理可调整大小的窗口
5. **在不同屏幕分辨率和 DPI 设置下充分测试**

## 故障排除

### 常见问题

**鼠标操作不准确：**
- 检查显示缩放设置
- 调整配置中的坐标偏移
- 验证 xdotool 正常工作

**窗口查找失败：**
- 确认窗口标题正确
- 增加等待超时
- 尝试使用部分标题的模糊匹配

**Wine 应用无法启动：**
- 验证 Wine 安装
- 检查应用程序路径
- 查看 Wine 日志中的错误

**图像识别失败：**
- 确保截图分辨率与模板匹配
- 调整置信度阈值
- 使用灰度图像以获得更好的匹配

## 安全注意事项

- 始终在安全环境中测试自动化脚本
- 谨慎使用自动化键盘输入（可能触发意外操作）
- 实现适当的错误处理和日志记录
- 尊重应用程序使用条款和条件
- 不要用于恶意目的或未经授权的访问
