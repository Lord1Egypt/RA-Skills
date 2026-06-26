# 龙虾安卓助手 / Lobster Android Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Android-orange)
![License](https://img.shields.io/badge/license-MIT-purple)

**一个强大的 Android 设备自动化控制技能**

A Powerful Android Device Automation Control Skill

[功能特性](#功能特性) • [快速开始](#快速开始) • [API文档](#api-文档) • [使用示例](#使用示例) • [常见问题](#常见问题)

</div>

---

## 📖 简介 / Introduction

**龙虾安卓助手 (scrcpy-claw)** 是一个为 WorkBuddy/ClawHub 设计的 Android 设备控制技能，基于 ADB 和 scrcpy 技术，提供全面的设备控制能力。

**Lobster Android Assistant (scrcpy-claw)** is an Android device control skill designed for WorkBuddy/ClawHub, based on ADB and scrcpy technologies, providing comprehensive device control capabilities.

### 🎯 核心能力 / Core Capabilities

| 功能模块 | 描述 |
|---------|------|
| 🖐️ **触摸控制** | 点击、滑动、长按、多点触控、手势操作 |
| ⌨️ **键盘输入** | 文本输入、按键事件、组合键、特殊按键 |
| 📱 **系统控制** | 电源管理、应用管理、截图录屏、剪贴板 |
| 🤖 **AI 自动化** | 屏幕分析、智能决策、自然语言控制 |
| 📺 **Scrcpy 集成** | 实时镜像、低延迟控制、完整消息支持 |
| 🔄 **脚本录制** | 操作录制、脚本保存、变速回放 |

---

## ✨ 功能特性 / Features

### 1. 触摸控制 / Touch Control

```python
# 点击操作 / Tap operations
controller.tap(500, 800)                    # 单击 / Single tap
controller.double_tap(500, 800)             # 双击 / Double tap
controller.long_press(500, 800, 1000)       # 长按1秒 / Long press 1s

# 滑动手势 / Swipe gestures
controller.swipe(100, 500, 500, 500)        # 自定义滑动 / Custom swipe
controller.swipe_direction('up')            # 方向滑动 / Directional swipe

# 多点触控 / Multi-touch
points = [TouchPoint(0, 300, 500), TouchPoint(1, 500, 500)]
controller.multi_touch(points, MotionEventAction.ACTION_DOWN)
```

### 2. 键盘输入 / Keyboard Input

```python
# 文本输入 / Text input
controller.input_text("Hello World")        # 输入文本 / Input text
controller.input_text("你好世界")            # 支持中文 / Chinese supported

# 按键事件 / Key events
controller.press_home()                     # 返回主页 / Home button
controller.press_back()                     # 返回键 / Back button
controller.press_power()                    # 电源键 / Power button
controller.volume_up()                      # 音量+ / Volume up
controller.volume_down()                    # 音量- / Volume down

# 组合键 / Key combinations
controller.send_key(KeyCode.KEYCODE_A, metastate=MetaKey.META_CTRL_ON)  # Ctrl+A
```

### 3. 系统控制 / System Control

```python
# 应用管理 / App management
controller.start_app("com.tencent.mm")      # 启动微信 / Launch WeChat
controller.force_stop("com.tencent.mm")     # 强制停止 / Force stop
controller.list_packages()                  # 列出应用 / List apps
controller.get_current_app()                # 当前应用 / Current app

# 屏幕操作 / Screen operations
controller.screenshot("screen.png")         # 截图 / Screenshot
controller.start_screen_record()            # 录屏 / Screen recording

# 系统功能 / System functions
controller.open_url("https://example.com")  # 打开链接 / Open URL
controller.set_clipboard("text")            # 设置剪贴板 / Set clipboard
controller.expand_notifications()           # 展开通知 / Expand notifications
```

### 4. AI 辅助自动化 / AI-Assisted Automation

```python
from scripts.ai_controller import ScreenAnalyzer, AIDecisionEngine

# 初始化 / Initialize
analyzer = ScreenAnalyzer()
engine = AIDecisionEngine(controller, analyzer)

# 自然语言控制 / Natural language control
engine.run_automation("打开微信")
engine.run_automation("在设置中启用深色模式")
engine.run_automation("搜索并发送消息给张三")

# 屏幕分析 / Screen analysis
elements = analyzer.dump_ui()               # 获取 UI 元素 / Get UI elements
buttons = analyzer.find_clickable_elements() # 查找可点击元素
text_fields = analyzer.find_text_fields()   # 查找输入框

# 元素查找 / Element search
results = analyzer.find_element_by_text("搜索")  # 按文本查找
results = analyzer.find_element_by_id("search")  # 按 ID 查找
```

### 5. Scrcpy 集成 / Scrcpy Integration

```python
from scripts.scrcpy_controller import ScrcpyController

# 初始化并连接 / Initialize and connect
scrcpy = ScrcpyController()
scrcpy.start_server()
scrcpy.connect()

# 实时控制 / Real-time control
scrcpy.tap(500, 800)
scrcpy.scroll(540, 1000, 0, -1.0)           # 滚动 / Scroll
scrcpy.rotate_device()                      # 旋转屏幕 / Rotate
scrcpy.turn_screen_off()                    # 关闭屏幕 / Turn off screen

# 断开连接 / Disconnect
scrcpy.disconnect()
```

### 6. 脚本录制回放 / Script Recording & Playback

```python
from scripts.adb_controller import ActionRecorder

recorder = ActionRecorder(controller)

# 录制操作 / Record actions
recorder.start_recording()
# ... 执行操作 ...
recorder.record_action('tap', {'x': 500, 'y': 800})
recorder.record_action('swipe', {'start_x': 100, 'start_y': 500, 
                                  'end_x': 500, 'end_y': 500})
actions = recorder.stop_recording()

# 保存脚本 / Save script
recorder.save_to_file("automation.json")

# 加载并回放 / Load and playback
actions = recorder.load_from_file("automation.json")
recorder.playback(actions, speed=2.0)       # 2倍速回放 / 2x speed
```

---

## 🚀 快速开始 / Quick Start

### 环境要求 / Requirements

- Python 3.7 或更高版本 / Python 3.7 or higher
- Android SDK (adb 命令可用) / Android SDK (adb command available)
- Android 设备 (已开启 USB 调试) / Android device (USB debugging enabled)

### 安装步骤 / Installation Steps

1. **检查 ADB** / **Check ADB**

```bash
adb version
# 应显示版本信息 / Should show version info
```

2. **连接设备** / **Connect Device**

```bash
# USB 连接 / USB connection
adb devices

# 无线连接 / Wireless connection
adb tcpip 5555
adb connect <设备IP>:5555
```

3. **加载技能** / **Load Skill**

在 WorkBuddy/ClawHub 中加载 `scrcpy-claw` 技能即可使用。

Load the `scrcpy-claw` skill in WorkBuddy/ClawHub to start using.

### 基础示例 / Basic Example

```python
from scripts.adb_controller import ADBController

# 创建控制器 / Create controller
controller = ADBController()

# 获取设备信息 / Get device info
info = controller.get_device_info()
print(f"设备: {info.get('ro.product.model', 'Unknown')}")

# 打开应用 / Open app
controller.start_app("com.tencent.mm")

# 截图 / Screenshot
controller.screenshot("screenshot.png")

# 执行操作 / Perform actions
controller.tap(540, 1000)
controller.input_text("Hello from Lobster!")
```

---

## 📚 API 文档 / API Documentation

### ADBController 类 / ADBController Class

主要的设备控制器，通过 ADB 命令实现设备控制。

Primary device controller using ADB commands.

#### 设备信息 / Device Info

| 方法 | 参数 | 返回值 | 描述 |
|------|------|--------|------|
| `get_device_info()` | - | `Dict` | 获取设备详细信息 |
| `get_screen_size()` | - | `(int, int)` | 获取屏幕分辨率 |
| `list_devices()` | - | `List[Dict]` | 列出已连接设备 |
| `screenshot(path)` | `path: str` | `str` | 截图并保存 |

#### 触摸操作 / Touch Operations

| 方法 | 参数 | 返回值 | 描述 |
|------|------|--------|------|
| `tap(x, y, duration)` | `x, y: int, duration: int` | `bool` | 点击坐标 |
| `double_tap(x, y)` | `x, y: int` | `bool` | 双击 |
| `long_press(x, y, duration)` | `x, y, duration: int` | `bool` | 长按 |
| `swipe(x1, y1, x2, y2, duration)` | 坐标和时长 | `bool` | 滑动手势 |
| `swipe_direction(direction)` | `direction: str` | `bool` | 方向滑动 |
| `pinch(cx, cy, start, end)` | 中心点和距离 | `bool` | 缩放手势 |

#### 键盘操作 / Keyboard Operations

| 方法 | 参数 | 返回值 | 描述 |
|------|------|--------|------|
| `input_text(text)` | `text: str` | `bool` | 输入文本 |
| `keyevent(keycode)` | `keycode: int` | `bool` | 发送按键事件 |
| `press_home()` | - | `bool` | 返回主页 |
| `press_back()` | - | `bool` | 返回键 |
| `press_menu()` | - | `bool` | 菜单键 |
| `press_power()` | - | `bool` | 电源键 |
| `press_enter()` | - | `bool` | 回车键 |
| `volume_up()` | - | `bool` | 音量+ |
| `volume_down()` | - | `bool` | 音量- |

#### 系统操作 / System Operations

| 方法 | 参数 | 返回值 | 描述 |
|------|------|--------|------|
| `start_app(package)` | `package: str` | `bool` | 启动应用 |
| `force_stop(package)` | `package: str` | `bool` | 强制停止 |
| `open_url(url)` | `url: str` | `bool` | 打开链接 |
| `set_clipboard(text)` | `text: str` | `bool` | 设置剪贴板 |
| `expand_notifications()` | - | `bool` | 展开通知栏 |

---

## 💡 使用示例 / Usage Examples

### 示例 1: 自动化测试流程 / Example 1: Automated Testing

```python
def test_login_flow():
    """测试登录流程 / Test login flow"""
    controller = ADBController()
    
    # 打开应用 / Open app
    controller.start_app("com.example.app")
    time.sleep(2)
    
    # 输入用户名 / Input username
    controller.tap(500, 800)
    controller.input_text("testuser")
    
    # 输入密码 / Input password
    controller.tap(500, 1000)
    controller.input_text("password123")
    
    # 点击登录 / Click login
    controller.tap(500, 1200)
    time.sleep(3)
    
    # 验证结果 / Verify result
    screenshot = controller.screenshot()
    # ... 验证逻辑 ...
```

### 示例 2: 微信自动回复 / Example 2: WeChat Auto Reply

```python
def wechat_auto_reply(contact_name, message):
    """微信自动回复 / WeChat auto reply"""
    controller = ADBController()
    analyzer = ScreenAnalyzer()
    
    # 打开微信 / Open WeChat
    controller.start_app("com.tencent.mm")
    time.sleep(2)
    
    # 搜索联系人 / Search contact
    controller.tap(540, 150)  # 搜索框
    controller.input_text(contact_name)
    time.sleep(1)
    
    # 点击联系人 / Click contact
    controller.tap(540, 400)
    time.sleep(1)
    
    # 发送消息 / Send message
    controller.tap(540, 2300)  # 输入框
    controller.input_text(message)
    controller.tap(1000, 2300)  # 发送按钮
```

### 示例 3: 批量操作 / Example 3: Batch Operations

```python
def batch_tap(positions):
    """批量点击 / Batch tap"""
    controller = ADBController()
    for x, y in positions:
        controller.tap(x, y)
        time.sleep(0.5)

# 执行批量点击 / Execute batch tap
positions = [(100, 200), (200, 300), (300, 400)]
batch_tap(positions)
```

---

## ❓ 常见问题 / FAQ

### Q1: 设备连接不上怎么办？/ Device not connecting?

**A:** 
1. 确保已开启 USB 调试：设置 > 开发者选项 > USB 调试
2. 重启 ADB 服务：`adb kill-server && adb start-server`
3. 检查驱动是否正确安装

### Q2: 中文输入显示乱码？/ Chinese input shows garbled text?

**A:** 安装 ADBKeyboard 输入法：
```bash
adb install ADBKeyboard.apk
adb shell ime set com.android.adbkeyboard/.AdbIME
```

### Q3: 截图失败？/ Screenshot failed?

**A:** 
1. 检查存储权限
2. 尝试使用 root 权限
3. 使用替代方法：`adb shell screencap -p`

### Q4: 滑动不准确？/ Swipe not accurate?

**A:** 
1. 检查屏幕分辨率是否正确获取
2. 调整滑动持续时间参数
3. 使用更精细的坐标

---

## 🙏 致谢 / Acknowledgements

本项目基于 [scrcpy](https://github.com/Genymobile/scrcpy) 项目开发，感谢 Genymobile 团队提供的优秀开源工具。

This project is built upon [scrcpy](https://github.com/Genymobile/scrcpy). Special thanks to the Genymobile team for their excellent open-source tool.

> scrcpy 是一个用于显示和控制 Android 设备的高性能应用，通过 USB 或 TCP/IP 连接，无需 root 权限。本项目借鉴了其控制消息协议和设备通信机制。
>
> scrcpy is a high-performance application for displaying and controlling Android devices connected via USB or TCP/IP, without requiring root access. This project draws inspiration from its control message protocol and device communication mechanisms.

### 相关项目 / Related Projects

- [scrcpy](https://github.com/Genymobile/scrcpy) - Display and control your Android device
- [ADBKeyboard](https://github.com/senzhk/ADBKeyBoard) - Android Keyboard for ADB input
- [uiautomator2](https://github.com/openatx/uiautomator2) - Android UI Automation

---

## 📄 许可证 / License

MIT License

Copyright (c) 2024 Lobster Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

---

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

Welcome to submit Issues and Pull Requests!

---

<div align="center">

**Made with ❤️ by Lobster Team**

</div>
