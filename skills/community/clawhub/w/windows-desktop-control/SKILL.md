---
name: desktop-control
description: "Windows 桌面控制工具 (仅Windows) - 截屏、窗口管理、鼠标键盘控制、进程管理、系统信息。当用户要求截屏、查看进程、关闭程序、桌面控制时使用此技能。"
metadata: 
  openclaw: 
    emoji: "🖥️"
    requires: 
      bins: ["python", "powershell"]
      pip: ["pyautogui", "mss", "pillow"]
---

# Desktop Control Skill

Windows 桌面控制工具 - 通过 Python 脚本实现桌面自动化控制。

## 功能列表

| 命令 | 说明 |
|------|------|
| `screenshot` | 截取屏幕 |
| `processes` | 进程列表 |
| `mouse` | 获取鼠标位置 |
| `click` | 鼠标点击 |
| `move` | 鼠标移动 |
| `type` | 输入文本 |
| `press` | 按键 |
| `hotkey` | 快捷键 |
| `kill` | 结束进程 (白名单限制) |
| `clipboard` | 剪贴板操作 |
| `info` | 系统信息 |

## 依赖安装

```bash
pip install pyautogui mss pillow
```

## 使用示例

### 截屏
```bash
python scripts/desktop_ctrl.py screenshot
```

### 进程列表
```bash
python scripts/desktop_ctrl.py processes
```

### 结束进程
```bash
python scripts/desktop_ctrl.py kill notepad
```

### 系统信息
```bash
python scripts/desktop_ctrl.py info
```

### 剪贴板
```bash
# 读取剪贴板
python scripts/desktop_ctrl.py clipboard get

# 写入剪贴板
python scripts/desktop_ctrl.py clipboard set "要复制的文字"
```

## 触发关键词

- "截屏"、"截图"、"屏幕快照"
- "查看进程"、"列出进程"  
- "关闭程序"、"结束进程"
- "桌面控制"
- "系统信息"、"电脑配置"
- "鼠标位置"
- "剪贴板"

## 注意事项

- **仅支持 Windows 系统**（使用 PowerShell 和 Win32 API）
- 截图保存在用户图片目录 `~/Pictures/OpenClaw/`
- 鼠标坐标以屏幕左上角为原点 (0, 0)
- 部分操作可能需要管理员权限
- `kill` 命令仅限白名单进程
- `exec` 命令已禁用（安全原因）
