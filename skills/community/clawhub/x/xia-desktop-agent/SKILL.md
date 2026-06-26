---
name: desktop-agent
description: Windows桌面自动化代理。通过自然语言或预设指令控制桌面：截图、点击、输入、按键、打开应用、微信发消息/文件、ToDesk远程连接。Use when user asks to control desktop, send WeChat messages, establish ToDesk remote connection, or automate any Windows GUI task.
---

# Desktop Agent — Windows 桌面自动化

控制 Windows 桌面的 AI 代理。支持两种模式：

1. **预设任务** — 一键执行常见操作（微信、ToDesk）
2. **自然语言** — LLM 规划 + 自动执行任意桌面操作

## 依赖

```bash
pip install pyautogui opencv-python Pillow pyperclip pygetwindow requests
# 可选（增强输入可靠性）: pip install pywin32
```

## 快速开始

### 预设任务（推荐）

```bash
# ToDesk远程连接：启动 → 截图 → AI识别密码 → 发送给用户
python scripts/presets.py todesk_connect

# 微信发消息
python scripts/presets.py wechat_message <联系人> <消息>

# 微信发文件
python scripts/presets.py wechat_file <联系人> <文件路径>
```

### ToDesk 远程连接完整流程

当用户说"远程连接"/"ToDesk"/"连接你"时，执行：

```bash
# Step 1-2: 启动ToDesk并截图
python scripts/presets.py todesk_connect
# 返回截图路径，用 image 工具识别临时密码
# Step 3: image(image=screenshot_path, prompt="识别设备代码和临时密码")
# Step 4: 发送识别结果给用户
```

**设备代码**: 用户本地配置（首次使用时查询）
**临时密码**: 动态生成，每次需截图识别

### 微信操作

前提：微信桌面客户端已登录，Ctrl+Alt+W 快捷键可用。

**发消息**:
```python
import pyautogui, time, pyperclip
pyautogui.hotkey('ctrl', 'alt', 'w')      # 激活微信
time.sleep(1.5)
pyautogui.hotkey('ctrl', 'f')              # 搜索
pyperclip.copy('联系人名')
pyautogui.hotkey('ctrl', 'v')
time.sleep(1); pyautogui.press('enter')
time.sleep(1.5)
# 点击输入框 → 粘贴消息 → 回车发送
```

**关键**: 粘贴前必须点击输入框获取焦点。

### 自然语言任务

```bash
python scripts/task_executor.py "打开记事本，输入Hello World，保存到桌面"
```

内部流程：LLM 规划 → 安全检查 → 逐步执行 → 截图验证。

## 核心模块

### DesktopAgent（scripts/desktop_agent.py）

| 方法 | 说明 |
|------|------|
| `screenshot(path)` | 截屏，返回路径 |
| `click(x, y)` | 点击坐标 |
| `type_text(text)` | 输入文字（优先SendMessage，降级剪贴板） |
| `press_key(key)` | 按键（支持 enter, escape, f1-f12 等） |
| `find_on_screen(img)` | OpenCV模板匹配查找元素 |
| `open_app(name)` | 启动应用 |
| `list_windows()` | 列出所有可见窗口 |

### 输入方式优先级

1. **SendMessage EM_REPLACESEL** — 直接向控件发文字，exec环境最可靠
2. **pyperclip + Ctrl+V** — 剪贴板粘贴，需窗口有焦点
3. **pyautogui.write** — 仅英文，逐字符模拟

## 安全机制

- 最大 20 步操作，超时 5 分钟
- 危险操作关键词检测（删除、格式化、关机等）
- pyautogui.FAILSAFE = True（鼠标移到角落可紧急停止）

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 输入无响应 | 尝试先 click 输入框获取焦点 |
| 中文输入失败 | 用 pyperclip + Ctrl+V，不用 pyautogui.write |
| 微信快捷键冲突 | 确认 Ctrl+Alt+W 未被其他软件占用 |
| ToDesk密码识别错误 | 重新截图，确保窗口在前台 |
| 截图保存失败 | 用英文路径 `C:\temp\` 或 `C:\home\` |
