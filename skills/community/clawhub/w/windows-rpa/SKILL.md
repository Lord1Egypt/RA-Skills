---
name: windows-rpa
version: "1.1.0"
description: |
  Windows 桌面 RPA 自动化控制。使用场景：
  (1) 操作桌面应用程序（非 Web 应用）
  (2) 模拟鼠标键盘操作
  (3) 截图和图像识别
  (4) 窗口管理和应用启动
  (5) 剪贴板操作
  (6) Shell 命令执行
  
  NOT for: Web 应用操作（请使用 browser 工具）、Linux/Mac 系统
os:
  - win32
  - windows
security:
  permissions:
    - screen_capture
    - keyboard_input
    - mouse_input
    - clipboard_access
    - shell_execution
  user_approval: recommended
  sandbox: supported
  sensitive_operations:
    - desktop_shell
    - desktop_clipboard_get
    - desktop_screenshot
metadata:
  openclaw:
    emoji: "🖥️"
    os: ["win32"]
    requires:
      bins: ["python"]
      anyBins: ["pyautogui", "pywinauto"]
    install:
      - id: "pip-pyautogui"
        kind: "pip"
        package: "pyautogui pillow"
        bins: ["pyautogui"]
        label: "Install PyAutoGUI for mouse/keyboard automation"
      - id: "pip-pywinauto"
        kind: "pip"
        package: "pywinauto"
        bins: ["pywinauto"]
        label: "Install PyWinAuto for Windows UI Automation"
      - id: "pip-pyperclip"
        kind: "pip"
        package: "pyperclip"
        label: "Install Pyperclip for clipboard operations"
implementation:
  type: "python"
  entry: "scripts/rpa.py"
---

# Windows RPA 自动化

这个 skill 让 OpenClaw 能够直接操作 Windows 桌面，包括鼠标、键盘、窗口和应用程序。

## 核心能力

### 1. 鼠标操作

```
# 移动鼠标到坐标 (x, y)
desktop_mouse_move(x=500, y=300)

# 鼠标点击
desktop_mouse_click(x=500, y=300, button="left", clicks=1)

# 鼠标拖拽
desktop_mouse_drag(start_x=100, start_y=100, end_x=500, end_y=500)

# 鼠标滚轮
desktop_mouse_scroll(clicks=3)  # 正数向上，负数向下

# 获取鼠标位置
desktop_mouse_position()
```

### 2. 键盘操作

```
# 输入文本
desktop_keyboard_type(text="Hello World")

# 按键
desktop_keyboard_press(key="enter")
desktop_keyboard_press(key="tab")
desktop_keyboard_press(key="escape")

# 组合键
desktop_keyboard_hotkey(keys=["ctrl", "c"])  # 复制
desktop_keyboard_hotkey(keys=["ctrl", "v"])  # 粘贴
desktop_keyboard_hotkey(keys=["ctrl", "a"])  # 全选
desktop_keyboard_hotkey(keys=["alt", "f4"])  # 关闭窗口
```

### 3. 屏幕操作

```
# 截取全屏
desktop_screenshot()

# 截取指定区域
desktop_screenshot(region={"x": 0, "y": 0, "width": 800, "height": 600})

# 获取屏幕尺寸
desktop_screen_size()

# 图像定位（在屏幕上找图）
desktop_locate_on_screen(image_path="button.png", confidence=0.9)
```

### 4. 窗口管理

```
# 列出所有窗口
desktop_window_list()

# 激活窗口
desktop_window_activate(title_pattern="记事本")

# 查找窗口
desktop_find_window(title_contains="Chrome")

# 点击窗口控件
desktop_click_window(
    title_contains="记事本",
    control_type="Edit",
    action="set_text",
    control_name="Hello"
)
```

### 5. 应用程序启动

```
# 启动常用应用（支持别名）
desktop_launch_app(app_name="notepad")
desktop_launch_app(app_name="chrome")
desktop_launch_app(app_name="excel")
desktop_launch_app(app_name="word")

# 启动自定义程序
desktop_launch_app(app_name="C:\\Program Files\\MyApp\\app.exe")

# 带参数启动
desktop_launch_app(app_name="chrome", args="--incognito")
```

### 6. Shell 命令

```
# PowerShell 命令
desktop_shell(command="Get-Process | Select-Object -First 5")

# CMD 命令
desktop_shell(command="dir C:\\", shell_type="cmd")
```

### 7. 剪贴板

```
# 获取剪贴板内容
desktop_clipboard_get()

# 设置剪贴板内容
desktop_clipboard_set(text="要复制的内容")
```

### 8. 桌面状态

```
# 获取完整桌面状态（鼠标位置、活动窗口、截图等）
desktop_get_state(capture_screenshot=True)

# 检查环境
desktop_check()
```

## 使用示例

### 示例 1: 自动填写表单

```
# 1. 启动应用程序
desktop_launch_app(app_name="notepad")

# 2. 等待窗口出现
time.sleep(1)

# 3. 输入内容
desktop_keyboard_type(text="这是一段自动输入的文字")

# 4. 保存文件
desktop_keyboard_hotkey(keys=["ctrl", "s"])
desktop_keyboard_type(text="auto_saved.txt")
desktop_keyboard_press(key="enter")
```

### 示例 2: 图像识别点击

```
# 1. 先截图保存按钮图像
desktop_screenshot(save_path="screen.png")

# 2. 用户手动截取按钮区域保存为 button.png

# 3. 在屏幕上定位并点击
result = desktop_locate_on_screen(image_path="button.png", confidence=0.9)
# 如果找到，会返回中心坐标，然后点击
```

### 示例 3: 操作特定窗口

```
# 1. 查找目标窗口
windows = desktop_find_window(title_contains="计算器")

# 2. 激活窗口
desktop_window_activate(title_pattern="计算器")

# 3. 点击窗口中的按钮
desktop_click_window(
    title_contains="计算器",
    control_type="Button",
    control_name="1"
)
```

## 安全注意事项

### 权限要求
本技能需要以下系统权限：
- **屏幕捕获**: 用于截图功能
- **键盘输入**: 用于文本输入和快捷键
- **鼠标输入**: 用于点击、移动等操作
- **剪贴板访问**: 用于读写剪贴板
- **Shell 执行**: 用于运行命令（可选）

### 敏感操作
以下操作建议开启用户确认：
- `desktop_shell` - 执行任意 Shell 命令
- `desktop_clipboard_get` - 读取剪贴板（可能包含敏感信息）
- `desktop_screenshot` - 屏幕截图（可能包含隐私内容）

### 用户批准机制
建议在 OpenClaw 配置中启用审批模式：
1. 敏感操作执行前会请求用户确认
2. 用户可以选择批准、拒绝或修改参数
3. 可设置白名单跳过审批

### 沙箱支持
- 建议在不包含敏感数据的测试环境中首次运行
- Shell 命令可在受限环境中执行
- 截图功能可限制截取区域

### 安全最佳实践
1. **审批模式**: 建议开启命令审批，每次执行前确认
2. **坐标依赖**: 屏幕坐标可能因分辨率不同而变化，优先使用图像识别
3. **窗口标题**: 使用模糊匹配而非精确匹配，提高鲁棒性
4. **超时处理**: 复杂操作应设置合理的等待时间
5. **最小权限**: 仅请求必要的权限，避免过度授权

## 后端选择

系统支持两种后端：

- **pyautogui** (默认): 纯坐标操作，简单可靠
- **pywinauto** (备用): Windows UI Automation，支持控件级操作

切换后端：
```
desktop_set_backend(backend="pywinauto")
```

## 错误处理

所有操作返回 JSON 格式结果：

```json
{
  "status": "ok",  // 或 "error"
  "message": "操作描述",
  // 其他字段...
}
```

建议检查 `status` 字段确认操作是否成功。

## 常见问题

**Q: 为什么鼠标移动不准确？**
A: 可能是分辨率缩放问题，尝试使用 `desktop_screen_size()` 检查实际分辨率。

**Q: 图像识别找不到目标？**
A: 降低 `confidence` 参数值，或确保图像与屏幕显示一致。

**Q: 中文输入乱码？**
A: 确保系统编码正确，或使用剪贴板方式输入。

**Q: pywinauto 无法找到控件？**
A: 部分应用使用自定义 UI，无法被 UI Automation 识别，改用坐标或图像方式。
