# Peekaboo / PeekabooWin 使用指南

本 skill 在不同平台上使用不同的自动化引擎：

| 平台 | 引擎 | 语言 | 安装方式 |
|------|------|------|----------|
| **macOS** | Peekaboo CLI | Swift/原生 | `brew install` |
| **Windows** | PeekabooWin | Node.js 22+ | `git clone` + `npm install` |

---

## macOS: Peekaboo CLI

### 安装

```bash
brew install steipete/peekaboo/peekaboo
```

### 验证安装

```bash
peekaboo version
peekaboo permissions
```

### 权限配置

1. 打开 **系统设置** → **隐私与安全性**
2. 授予 **屏幕录制** 权限给 Peekaboo
3. 授予 **辅助功能** 权限给 Peekaboo
4. 重启终端后验证: `peekaboo permissions`

### 命令速查

#### 截图类

| 命令 | 用途 | 示例 |
|------|------|------|
| `peekaboo image --mode window --app 微信 --retina --path FILE` | 截取微信窗口 | 高清 retina 截图 |
| `peekaboo see --app 微信 --annotate --path FILE` | 截图并标注 UI 元素 | 用于定位按钮/输入框坐标 |
| `peekaboo image --mode screen --retina --path FILE` | 截取全屏 | 微信不在前台时使用 |

#### 窗口/应用控制

| 命令 | 用途 |
|------|------|
| `peekaboo app switch --to 微信` | 切换到微信前台 |
| `peekaboo app unhide --app 微信` | 取消隐藏微信 |
| `peekaboo app hide --app 微信` | 隐藏微信 |
| `peekaboo list apps --json` | 列出所有运行中的应用 |

#### 输入操作

| 命令 | 用途 | 注意事项 |
|------|------|---------|
| `peekaboo click --coords X,Y --app 微信` | 点击指定坐标 | 需要先确定正确坐标 |
| `peekaboo type "文字" --app 微信` | 输入文字 | 模拟真人打字速度 |
| `peekaboo type "" --app 微信 --return` | 发送消息（回车） | 微信必须用此方式发送 |
| `peekaboo press --key return` | 按回车键 | 对微信不可靠 |

---

## Windows: PeekabooWin

### 前置条件

| 要求 | 说明 |
|------|------|
| **操作系统** | Windows 10 或 Windows 11 |
| **Node.js** | 22.0.0 或更高版本 ([下载地址](https://nodejs.org)) |
| **Shell** | PowerShell（推荐）或 CMD |
| **Python** | 3.7+ （监控脚本需要） |

### 安装步骤

```powershell
# 1. 克隆仓库
git clone https://github.com/FelixKruger/PeekabooWin
cd PeekabooWin

# 2. 安装依赖
npm install

# 3. 运行测试确认安装成功
npm test
```

### 设置环境变量

监控脚本需要知道 PeekabooWin 安装在哪里。

```powershell
# 方式1: 临时设置（仅当前 PowerShell 窗口有效）
$env:PEEKABOO_WIN_DIR = "C:\Users\<你的用户名>\PeekabooWin"

# 方式2: 永久设置（推荐，所有窗口生效）
[System.Environment]::SetEnvironmentVariable(
    "PEEKABOO_WIN_DIR",
    "C:\Users\<你的用户名>\PeekabooWin",
    "User"
)
```

> 设置永久环境变量后，**需要重新打开 PowerShell 窗口**才能生效。

### 验证安装

```powershell
# 检查 Node.js 版本
node --version
# 应显示 v22.x.x 或更高

# 检查 PeekabooWin 是否可用
node C:\Users\<你的用户名>\PeekabooWin\bin\peekaboo-win.js --help

# 列出所有窗口
node C:\Users\<你的用户名>\PeekabooWin\bin\peekaboo-win.js windows list

# 截取微信窗口
node C:\Users\<你的用户名>\PeekabooWin\bin\peekaboo-win.js screen capture --output %TEMP%\wechat_test.png
```

### 权限注意事项

- 部分操作可能需要**管理员权限**运行 PowerShell
- 确保微信窗口未被 Windows "专注助手" (Focus Assist) 屏蔽
- Windows OCR 运行时通常已内置，无需额外安装
- 某些安全软件可能拦截模拟输入，需添加白名单

### 命令速查

#### 截图类

| 命令 | 用途 |
|------|------|
| `peekaboo-win screen capture --output FILE` | 截取全屏 |
| `peekaboo-win window capture --hwnd <id>` | 截取指定窗口 |
| `peekaboo-win see --mode window --title "微信"` | 截图 + 索引 UI 控件 |
| `peekaboo-win snapshot list` | 查看已保存的快照 |

> 以下命令中的 `peekaboo-win` 是 `node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js` 的简写。

#### 应用控制

| 命令 | 用途 |
|------|------|
| `peekaboo-win app list` | 列出所有运行中的应用 |
| `peekaboo-win app switch --name "微信"` | 切换到微信 |
| `peekaboo-win app launch --command WeChat.exe` | 启动微信 |
| `peekaboo-win app quit --name "微信"` | 退出微信 |

#### 输入操作

| 命令 | 用途 |
|------|------|
| `peekaboo-win click --on "标签"` | 通过 UI 标签点击（推荐） |
| `peekaboo-win click --on "100,200"` | 通过坐标点击 |
| `peekaboo-win mouse click --x 900 --y 780` | 鼠标点击坐标 |
| `peekaboo-win type --text "文字"` | 输入文字 |
| `peekaboo-win type --text "文字" --clear` | 清空后输入文字 |
| `peekaboo-win press --keys "Enter"` | 按单个键 |
| `peekaboo-win hotkey --keys ctrl,shift,t` | 组合键 |

#### 窗口管理

| 命令 | 用途 |
|------|------|
| `peekaboo-win window focus --hwnd <id>` | 聚焦窗口 |
| `peekaboo-win window state --title "微信" --state restore` | 恢复窗口 |
| `peekaboo-win window state --title "微信" --state maximize` | 最大化 |
| `peekaboo-win window move --title "微信" --x 100 --y 100` | 移动窗口 |

### 微信输入框定位（Windows）

PeekabooWin 比 macOS Peekaboo 更强大：支持通过 **UI 标签** 点击，无需硬编码坐标。

```powershell
# 1. 查看微信窗口中有哪些 UI 元素
peekaboo-win see --mode window --title "微信"

# 2. 找到输入框的标签（可能是 "消息", "输入" 等）
# 3. 通过标签点击
peekaboo-win click --on "消息" --title "微信"

# 4. 如果标签点击不可靠，用坐标
peekaboo-win mouse click --x 900 --y 780
```

### macOS vs Windows 命令对照表

| 操作 | macOS (Peekaboo) | Windows (PeekabooWin) |
|------|-----------------|----------------------|
| 截图 | `peekaboo image --mode window --app 微信 --path FILE` | `peekaboo-win screen capture --output FILE` |
| 切换应用 | `peekaboo app switch --to 微信` | `peekaboo-win app switch --name "微信"` |
| 点击 | `peekaboo click --coords X,Y --app 微信` | `peekaboo-win click --on "label"` 或 `mouse click --x --y` |
| 输入文字 | `peekaboo type "text" --app 微信` | `peekaboo-win type --text "text"` |
| 发送消息 | `peekaboo type "" --app 微信 --return` | `peekaboo-win press --keys "Enter"` |
| 列出应用 | `peekaboo list apps` | `peekaboo-win app list` |
| 查看元素 | `peekaboo see --app 微信 --annotate` | `peekaboo-win see --mode window --title "微信"` |

### 踩坑记录（Windows）

1. **Node.js 版本**：必须 22+，低于 22 会报错
2. **环境变量**：必须设置 `PEEKABOO_WIN_DIR`，否则监控脚本找不到 PeekabooWin
3. **微信窗口最小化**：PeekabooWin 截取全屏时，最小化的窗口不会出现。请保持微信窗口在前台或至少未最小化
4. **OCR 精度**：Windows 内置 OCR 对中文识别较好，但密集文字可能遗漏
5. **管理员权限**：某些窗口操作需要以管理员身份运行 PowerShell
6. **pyautogui failsafe**：将鼠标移到屏幕左上角会紧急停止所有操作

---

## 常见问题

### Q: PeekabooWin 的 `screen capture` 能截取最小化的窗口吗？

**不能。** `screen capture` 截取的是屏幕上的可见内容。微信窗口必须至少在桌面上可见（不需要在最前面，但不能最小化到任务栏）。

### Q: PeekabooWin 和 macOS Peekaboo 的命令一样吗？

**不一样。** PeekabooWin 是独立项目，命令语法不同。但功能类似：截图、点击、输入、窗口管理。

### Q: 可以用 PeekabooWin 的 MCP Server 吗？

可以，PeekabooWin 内置 MCP Server。但本 skill 的监控脚本使用的是 CLI 方式，不依赖 MCP。

### Q: Windows 上截图文件保存到哪里？

默认保存到 `%TEMP%\wechat_mon\` 目录，即 `C:\Users\<用户名>\AppData\Local\Temp\wechat_mon\`。
