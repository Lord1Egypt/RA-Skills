---
name: smseow-peekaboo
version: 1.0.2
description: (Simon专属) 桌面控制 skill - AI 操控电脑。macOS 用 Peekaboo，Linux 用 MCP 工具。
keywords: [桌面控制,macOS,Linux,自动化,AI操控,截屏,点击,WSL2]
---

# 桌面控制 (Desktop Control)
AI 操控电脑 - macOS / Linux / WSL2

---

## 概述

让 AI 能"看"屏幕、"动"桌面。

| 系统 | 工具 | GitHub |
|---------|--------|--------|
| **macOS 15+** | Peekaboo | `openclaw/Peekaboo` |
| **Linux** | Ubuntu Desktop Control MCP | `charettep/...` |
| **WSL2** | python-xlib + X server | - |

---

## 触发词

`桌面控制` / `操控电脑` / `截屏` / `desktop`

---

## 🖥️ macOS (Peekaboo)

### 安装
```bash
npx -y @steipete/peekaboo

# 授权
peekaboo permissions grant
```

### 命令
```bash
# 截图
peekaboo image --mode screen

# 点击
peekaboo click --on "按钮文字"

# 输入
peekaboo type --text "内容"

# 快捷键
peekaboo hotkey cmd,c
```

---

## 🐧 Linux (桌面 MCP)

### 方案1: Ubuntu Desktop Control MCP
```bash
# 安装
pip install mcp-desktop-control

# 运行
mcp-desktop-control
```

### 方案2: mcp-desktop-pro (跨平台)
```bash
# 安装运行
npx -y mcp-desktop-pro serve

# 截图
# mcp-desktop-pro screenshot

# 点击
# mcp-desktop-pro click --x 100 --y 200
```

### 方案3: kwin-mcp (KDE Wayland)
```bash
git clone https://github.com/bhyoo/kwin-mcp
cd kwin-mcp
python kwin-mcp.py
```

---

## 💻 WSL2 方案

### 1. 安装 X server (Windows)
下载安装 [VcXsrv](https://github.com/ArcticaProject/vcxsrv)

### 2. WSL2 配置
```bash
# .bashrc 添加
export DISPLAY=localhost:0

# 安装依赖
sudo apt install python3-xlib flameshot scrot
```

### 3. Python 自动化
```python
from pymouse import PyMouse
from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()

# 点击
m.click(100, 200)

# 输入
k.type_string("Hello")

# 快捷键
k.press_key('ctrl')
k.tap_key('c')
k.release_key('ctrl')
```

---

## 使用示例

### macOS
```
你说：打开Safari去openclaw官网
我 → peekaboo app launch Safari
   → peekaboo type --text "openclaw.ai"
   → peekaboo press return
```

### Linux
```
你说：截个图
我 → mcp-desktop-control screenshot
```

### WSL2
```
你说：点击这个按钮
我 → 用坐标点击
```

---

## 注意事项

- ⚠️ macOS 需要 15+，授权辅助功能
- ⚠️ Linux 需要 X server 或 Wayland
- ⚠️ WSL2 需要 VcXsrv

---

*桌面控制 | AI 操控电脑*