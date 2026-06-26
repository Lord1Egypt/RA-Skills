# Windows RPA 自动化 Skill

让 OpenClaw/龙虾能够直接操作 Windows 桌面的 RPA 自动化技能。

## 功能特性

- **鼠标操作**: 移动、点击、拖拽、滚轮
- **键盘操作**: 输入文本、按键、组合键
- **屏幕操作**: 截图、图像定位
- **窗口管理**: 列出窗口、激活窗口
- **应用启动**: 启动常用应用程序
- **剪贴板**: 读写剪贴板内容
- **Shell命令**: 执行 PowerShell/CMD 命令

## 安装

### 1. 安装依赖

```bash
pip install pyautogui pillow pywinauto pyperclip
```

### 2. 复制到 OpenClaw skills 目录

```bash
# Linux/Mac
cp -r windows-rpa ~/.openclaw/skills/

# Windows
xcopy /E /I windows-rpa %USERPROFILE%\.openclaw\skills\windows-rpa
```

### 3. 重启 OpenClaw

```bash
# 重启后自动加载
```

## 使用示例

### 鼠标操作

```
# 移动鼠标到 (500, 300)
desktop_mouse_move --x 500 --y 300

# 点击
desktop_mouse_click --x 500 --y 300 --button left

# 滚轮
desktop_mouse_scroll --clicks 3
```

### 键盘操作

```
# 输入文本
desktop_keyboard_type --text "Hello World"

# 按键
desktop_keyboard_press --key enter

# 组合键
desktop_keyboard_hotkey --keys ctrl,c
```

### 应用启动

```
# 启动记事本
desktop_launch_app --app notepad

# 启动 Chrome（隐身模式）
desktop_launch_app --app chrome --args "--incognito"
```

### 截图

```
# 全屏截图
desktop_screenshot

# 保存到指定路径
desktop_screenshot --output screenshot.png
```

## 注意事项

1. **仅支持 Windows**: 此 skill 专为 Windows 设计
2. **需要 Python**: 确保系统已安装 Python 3.8+
3. **分辨率**: 坐标基于实际屏幕分辨率
4. **中文输入**: 自动使用剪贴板方式输入中文

## 与 iFlow CLI 集成

此 skill 与 iFlow CLI 的 `desktop` 模块共享相同的核心代码，可以无缝切换使用。

## 许可证

MIT
