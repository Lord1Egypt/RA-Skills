---
name: 微信 PC 端自动控制
description: 打开微信桌面端，向指定联系人发送消息、图片、文件等内容。触发词：给某人发微信、打开微信发消息、微信发送、通过微信发给。也支持被其他
  Skill 调用，实现自动化推送。
version: 1.1.0
author: 微光浮影
homepage: https://skillhub.cn/skills/wechat-desktop-claw-automatic-control
license: Apache-2.0
tags:
  - wechat
  - automation
  - pywinauto
  - windows
---

# 微信 PC 端自动控制 v1.1.0

通过 `pywinauto` 自动化操作微信 Windows 桌面端，实现消息/图片/文件的自动发送。

**本 Skill 完全开源，源代码公开，采用 Apache-2.0 协议。**

## 更新日志 v1.0.1

- 🔓 **源代码完全公开**，Apache-2.0 协议
- 添加 LICENSE 文件
- 添加 README.md（含完整源码说明）
- SKILL.md 补充 homepage / license / tags 字段
- 修复：脚本编码声明修正为完整 emacs 格式

## 更新日志 v1.1.0（针对自主 Agent 驱动适配）

- 🆕 **批次模式 `--manifest`**：一条命令、单个进程处理多个群聊 + 多张图，杜绝 Agent 在多次调用之间误关微信
- 🆕 **截图校验 `--screenshot`**：不关闭微信即可把聊天窗口存成 PNG，供 Agent 肉眼核验发送结果
- 🆕 **托盘 / 最小化自动恢复**：即使微信被收进托盘，也会自动 `ShowWindow(SW_RESTORE)` + 置前台还原，无需人工重开
- 🆕 **结构化输出**：`[SENT_OK]` / `[SENT_FAIL]` / `[RESULT]` 标记，便于 Agent 解析成败，不必靠关窗判断
- 🔒 **脚本绝不关闭微信**：任何路径都不会退出微信进程

## 功能

- 打开微信桌面端（如未运行则自动启动）
- 搜索并定位联系人（支持群聊）
- 发送文本消息（支持长文本从文件读取）
- 发送图片（通过剪贴板 BMP 格式）
- 发送文件（通过 Ctrl+Alt+F 快捷键）

## 环境要求

- Windows 系统
- 微信桌面端已安装
- Python3.7+
- 依赖库：`pywinauto`, `pyperclip`, `pillow`, `pywin32`

## 安装依赖

```bash
pip install pywinauto pyperclip pillow pywin32
```

## 微信路径配置

默认路径：`C:\Program Files (x86)\Tencent\WeChat\WeChat.exe`

常见安装路径也可能为 `D:\Tencent\WeiXin\WeiXin.exe`（注意拼写是 WeiXin 不是 WeChat）。

修改脚本第 33 行 `WECHAT_PATH` 变量即可适配你的安装路径。

## 使用方式

### 命令行直接调用

```bash
# 发送文本
python scripts/wechat_send.py --contact "好友昵称" --message "你好，这是自动发送的消息"

# 从文件读取长文本发送
python scripts/wechat_send.py --contact "好友昵称" --message-file "report.txt"

# 发送图片
python scripts/wechat_send.py --contact "好友昵称" --image "C:\path\to\image.png"

# 发送文件
python scripts/wechat_send.py --contact "好友昵称" --file "C:\path\to\file.pdf"

# 仅启动微信
python scripts/wechat_send.py --launch-only
```

### 被其他 Skill 调用

其他 Skill 可以通过以下方式调用本 Skill 发送消息：

```python
import subprocess
subprocess.run([
    "python",
    "scripts/wechat_send.py",
    "--contact", "好友昵称",
    "--message", "消息内容"
])
```

## ⚠️ 自主 Agent（Codex / WorkBuddy 等）驱动适配（v1.1.0 新增）

本 Skill 常被 Codex、WorkBuddy 等自主 Agent 通过命令行驱动。以下是针对这类场景的关键约定，**务必遵守，否则会出现“发完一个群微信就被关进托盘、需手动重开”的死循环**：

### 1. 脚本绝不关闭微信
`wechat_send.py` 在任何情况下都不会关闭 / 退出微信。微信由脚本启动时即作为独立进程常驻，脚本进程结束也不杀它。**Agent 在批次任务中也严禁主动关闭 / 最小化微信窗口**——微信的 `×` 按钮和 `Alt+F4` 默认只是“最小化到系统托盘”，不是真退出，关了反而会把下一次操作卡死。

### 2. 多群 / 多图任务一律用批次模式（`--manifest`）
不要为每个群各跑一次脚本（那样 Agent 容易在两次调用之间手滑关微信）。改为**一条命令、一个进程**处理全部：

```bash
python scripts/wechat_send.py --manifest send_plan.json
```

`send_plan.json` 示例（两张图发两个群，且每张图前先发通用文本）：

```json
[
  {
    "contact": "群聊A",
    "message": "xxx",
    "images": ["D:/pics/a.png"]
  },
  {
    "contact": "群聊B",
    "message": "xxx",
    "images": ["D:/pics/b.png"]
  }
]
```

字段：`contact`（必填，群名/昵称）、`message` / `message_file`（文本）、`images`（图片数组）、`files`（文件数组）。整个批次在单个进程内顺序完成，微信全程不关。脚本结尾输出 `[RESULT] total=N ok=M fail=K` 供 Agent 解析。

### 3. 校验请用截图，别关窗
旧版“只发送不读取”，Agent 没法确认成败，往往靠“关了重开再瞅”来核验——这正是 issues 里“不断关闭微信”的来源。v1.1.0 新增：

```bash
python scripts/wechat_send.py --manifest send_plan.json --screenshot D:/verify.png
```

脚本把微信窗口存成 PNG（**不关闭微信**），Agent 直接读图核验。每组发送都会打 `[SENT_OK]` / `[SENT_FAIL]` 标记，无需关窗判断。

### 4. 已被收进托盘？自动恢复，无需手动重开
若微信不慎被收进托盘，重跑脚本即可：`launch_wechat()` 会按标题匹配隐藏窗口，`get_main_window()` 会 `ShowWindow(SW_RESTORE)` + 置前台自动还原。批次中每组操作前也都会 `ensure_window()` 确认窗口在前台。

## 技术说明

### 窗口连接

使用 `pywinauto` 的 `uia` 后端连接微信窗口，**窗口标题必须为"微信"**（不是 "WeChat"）。

```python
app = Application(backend='uia').connect(title_re="微信", timeout=10)
window = app.window(title_re="微信")
```

### 中文输入

所有文本输入均通过 **剪贴板 + Ctrl+V** 实现，避免 `pywinauto` 直接键入中文的编码问题。

```python
pyperclip.copy(text)
send_keys("^v")  # Ctrl+V 粘贴
```

### 图片发送原理

将图片转为 BMP 格式（去掉文件头 14 字节，取 DIB 数据），直接写入 Windows 剪贴板 `CF_DIB` 格式，在聊天框 Ctrl+V 粘贴即发送。

```python
# 详见 scripts/wechat_send.py send_image() 函数
win32clipboard.SetClipboardData(win32con.CF_DIB, data)
```

### 发送快捷键

- 发送消息：`Enter` 键（微信默认设置）
- 打开搜索：`Ctrl+F`
- 打开文件选择：`Ctrl+Alt+F`

## 限制与注意事项

1. **微信窗口必须可见（已支持托盘自动恢复）**：自动化需要窗口在前台。v1.1.0 起，即使微信被收进托盘，脚本也会自动 `ShowWindow` 还原到前台，无需手动重开。但仍建议 Agent 批次任务中**不要主动关闭 / 最小化**微信（`×`/`Alt+F4` 仅最小化到托盘，关了反而卡死后续操作）。
2. **登录状态**：通常自动登录，偶尔需要扫码（脚本会提示）
3. **联系人名称**：必须精确匹配搜索结果第一名
4. **UI 依赖**：依赖微信 Windows 版 UI 结构，微信版本更新可能导致失效
5. **不能读取消息**：本 Skill 只发送，不读取微信消息内容

## 源代码结构

```
wechat-desktop-claw-automatic-control/
├── SKILL.md              # Skill 定义文件（本文件）
├── scripts/
│   └── wechat_send.py    # 核心自动化脚本（完整源码见下方）
├── LICENSE               # Apache-2.0 开源协议
└── README.md            # 说明文档
```

## 完整源码

### `scripts/wechat_send.py`

> 完整源码已随 Skill 打包，路径：`scripts/wechat_send.py`

（源码内容较长，见 `scripts/wechat_send.py` 文件）

## 报告问题

SkillHub 评论区：https://skillhub.cn/skills/wechat-desktop-claw-automatic-control
