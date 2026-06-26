---
name: scrcpy-claw
description: >
  Lobster Android Assistant (龙虾安卓助手) - A comprehensive Android device control skill.
  Provides touch control, keyboard input, system operations, screen analysis,
  AI-assisted automation, and script recording/playback through ADB and scrcpy integration.
  Use this skill when the user wants to control Android devices, automate testing,
  perform remote control, or build automation workflows.
  当用户想要控制安卓设备、自动化测试、远程操作或构建自动化流程时，使用此技能。
---

# 龙虾安卓助手 / Lobster Android Assistant

一个强大的 Android 设备控制技能，通过 ADB 和 scrcpy 集成实现全面的设备控制能力。

A powerful Android device control skill with comprehensive capabilities through ADB and scrcpy integration.

## 功能特性 / Features

### 🎯 触摸控制 / Touch Control
- 点击、双击、长按 / Tap, double-tap, long press
- 滑动、手势操作 / Swipe, gestures
- 多点触控、缩放手势 / Multi-touch, pinch-to-zoom

### ⌨️ 键盘输入 / Keyboard Input
- 文本输入（支持中文） / Text input (Chinese supported)
- 按键事件、组合键 / Key events, key combinations
- 特殊按键（Home、Back、音量等）/ Special keys (Home, Back, Volume, etc.)

### 📱 系统控制 / System Control
- 电源管理 / Power management
- 应用启动与切换 / App launch and switching
- 截图、录屏 / Screenshot, screen recording
- 剪贴板操作 / Clipboard operations

### 🤖 AI 辅助自动化 / AI-Assisted Automation
- 屏幕分析与 UI 元素识别 / Screen analysis and UI element detection
- 智能决策与操作建议 / Intelligent decision-making
- 自然语言指令执行 / Natural language command execution

### 📹 Scrcpy 集成 / Scrcpy Integration
- 实时屏幕镜像 / Real-time screen mirroring
- 低延迟控制 / Low-latency control
- 完整控制消息支持 / Full control message support

### 🔄 脚本录制回放 / Script Recording & Playback
- 操作录制 / Action recording
- 脚本保存与加载 / Script save and load
- 变速回放 / Variable speed playback

## 快速开始 / Quick Start

### 基础使用 / Basic Usage

```python
from scripts.adb_controller import ADBController

# 初始化控制器 / Initialize controller
controller = ADBController()

# 触摸操作 / Touch operations
controller.tap(500, 800)              # 点击 / Tap
controller.swipe(100, 500, 500, 500)  # 滑动 / Swipe
controller.long_press(500, 800, 1000) # 长按 / Long press

# 键盘操作 / Keyboard operations
controller.press_home()               # 返回主页 / Go home
controller.press_back()               # 返回键 / Back
controller.input_text("Hello")        # 输入文本 / Input text

# 系统操作 / System operations
controller.screenshot("screen.png")   # 截图 / Screenshot
controller.start_app("com.android.settings")  # 启动应用 / Launch app
```

### AI 自动化 / AI Automation

```python
from scripts.adb_controller import ADBController
from scripts.ai_controller import ScreenAnalyzer, AIDecisionEngine

controller = ADBController()
analyzer = ScreenAnalyzer()
engine = AIDecisionEngine(controller, analyzer)

# 执行自动化任务 / Execute automation
engine.run_automation("打开设置并启用深色模式")
# Open settings and enable dark mode
```

### 脚本录制 / Script Recording

```python
from scripts.adb_controller import ADBController, ActionRecorder

controller = ADBController()
recorder = ActionRecorder(controller)

# 开始录制 / Start recording
recorder.start_recording()
recorder.record_action('tap', {'x': 500, 'y': 800})
recorder.stop_recording()

# 保存并回放 / Save and playback
recorder.save_to_file("script.json")
actions = recorder.load_from_file("script.json")
recorder.playback(actions, speed=2.0)
```

## 环境要求 / Requirements

- Python 3.7+
- Android SDK (adb 命令可用 / adb command available)
- 已开启 USB 调试的 Android 设备 / Android device with USB debugging enabled

## 安装说明 / Installation

1. 确保已安装 ADB 并添加到系统 PATH
   Ensure ADB is installed and added to system PATH

```bash
adb version
```

2. 连接 Android 设备并授权 USB 调试
   Connect Android device and authorize USB debugging

```bash
adb devices
```

3. 加载技能即可使用
   Load the skill and start using

## API 参考 / API Reference

### ADBController

主要设备控制器 / Primary device controller.

| 方法 Method | 描述 Description |
|-------------|------------------|
| `tap(x, y, duration_ms)` | 点击坐标 / Tap at coordinates |
| `swipe(x1, y1, x2, y2, duration_ms)` | 滑动手势 / Swipe gesture |
| `long_press(x, y, duration_ms)` | 长按操作 / Long press |
| `input_text(text)` | 输入文本 / Input text |
| `keyevent(keycode)` | 发送按键事件 / Send key event |
| `press_home()` | 返回主页 / Press HOME |
| `press_back()` | 返回键 / Press BACK |
| `screenshot(path)` | 截图 / Take screenshot |
| `start_app(package)` | 启动应用 / Launch app |

### ScrcpyController

高级控制器（需 scrcpy 服务）/ Advanced controller (requires scrcpy server).

| 方法 Method | 描述 Description |
|-------------|------------------|
| `start_server()` | 启动 scrcpy 服务 / Start scrcpy server |
| `connect()` | 连接到设备 / Connect to device |
| `scroll(x, y, h, v)` | 滚动操作 / Scroll operation |
| `rotate_device()` | 旋转屏幕 / Rotate screen |
| `multi_touch(points)` | 多点触控 / Multi-touch |

### AIDecisionEngine

AI 决策引擎 / AI decision engine.

| 方法 Method | 描述 Description |
|-------------|------------------|
| `analyze_and_suggest(goal)` | 分析并建议操作 / Analyze and suggest |
| `execute_suggestion(suggestion)` | 执行建议 / Execute suggestion |
| `run_automation(goal)` | 执行自动化任务 / Run automation |

## 使用场景 / Use Cases

### 自动化测试 / Automated Testing

```python
# 运行测试序列 / Run test sequence
controller.start_app("com.example.app")
controller.tap(500, 800)
controller.input_text("test input")
controller.press_back()
```

### 远程控制 / Remote Control

```python
# 镜像用户指令 / Mirror user commands
def handle_command(cmd):
    if cmd.type == 'tap':
        controller.tap(cmd.x, cmd.y)
    elif cmd.type == 'type':
        controller.input_text(cmd.text)
```

### AI 辅助操作 / AI-Assisted Operations

```python
# 让 AI 自动完成任务 / Let AI complete tasks
engine.run_automation("打开微信发送消息给张三")
# Open WeChat and send message to Zhang San
```

## 故障排除 / Troubleshooting

### 设备未找到 / Device Not Found

```bash
adb devices
adb kill-server && adb start-server
```

### 权限被拒绝 / Permission Denied

在设备上启用 USB 调试：设置 > 开发者选项 > USB 调试
Enable USB debugging on device: Settings > Developer Options > USB Debugging

### 中文输入问题 / Chinese Input Issues

建议安装 ADBKeyboard 以支持中文输入：
Install ADBKeyboard for Chinese input support:
```bash
adb install ADBKeyboard.apk
adb shell ime set com.android.adbkeyboard/.AdbIME
```

## 技术架构 / Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     龙虾安卓助手                              │
│                    Lobster Android Assistant                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ ADB 控制器  │  │ Scrcpy 控制器│  │   AI 决策引擎       │  │
│  │ADB Controller│ │Scrcpy Ctrl │  │AI Decision Engine  │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          │                                   │
│                   ┌──────┴──────┐                            │
│                   │  Android 设备│                            │
│                   │Android Device│                           │
│                   └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

## 版本信息 / Version Info

- 版本 Version: 1.0.0
- 作者 Author: Lobster Team
- 许可证 License: MIT

## 更新日志 / Changelog

### v1.0.0
- 初始版本发布 / Initial release
- ADB 完整控制支持 / Full ADB control support
- Scrcpy 集成 / Scrcpy integration
- AI 自动化功能 / AI automation features
- 脚本录制回放 / Script recording & playback
