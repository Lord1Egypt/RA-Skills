# 微信 PC 端自动控制 Skill

> 本 Skill 是 OpenClaw / WorkBuddy 的插件，通过 `pywinauto` 自动化操作微信 Windows 桌面端。采用 Apache-2.0 协议开源。

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 打开微信 | 如未运行自动启动，已运行则直接连接 |
| 搜索联系人 | 支持昵称、备注名、群名 |
| 发送文本 | 支持长文本（从文件读取） |
| 发送图片 | 通过剪贴板 DIB 格式直接粘贴 |
| 发送文件 | 通过微信文件选择对话框 |
| 被其他 Skill 调用 | 可作为自动化推送通道 |

## 📦 安装

### 方式一：SkillHub（推荐）

```bash
skillhub install wechat-desktop-claw-automatic-control
```

### 方式二：手动安装

将本 Skill 目录复制到 OpenClaw / WorkBuddy 的 skills 目录：

```bash
cp -r wechat-desktop-claw-automatic-control ~/.openclaw/workspace/skills/
# 或 WorkBuddy: 复制到 用户目录/.workbuddy/skills/
```

## 🔧 依赖安装

```bash
pip install pywinauto pyperclip pillow pywin32
```

## ⚙️ 配置

编辑 `scripts/wechat_send.py` 第 33 行，修改微信安装路径：

```python
WECHAT_PATH = "C:/Program Files (x86)/Tencent/WeChat/WeChat.exe"  # 改为你的实际路径
```

常见路径：
- `C:\Program Files (x86)\Tencent\WeChat\WeChat.exe`
- `D:\Tencent\WeiXin\WeiXin.exe`（注意拼写是 WeiXin，非 WeChat）

## 🚀 使用方法

### 命令行直接调用

```bash
# 发送文本
python scripts/wechat_send.py --contact "好友昵称" --message "你好！"

# 从文件读取长文本发送（适合报告/长消息）
python scripts/wechat_send.py --contact "好友昵称" --message-file "report.txt"

# 发送图片
python scripts/wechat_send.py --contact "好友昵称" --image "C:\screenshot.png"

# 发送文件
python scripts/wechat_send.py --contact "好友昵称" --file "C:\document.pdf"

# 仅启动微信（不发送）
python scripts/wechat_send.py --launch-only
```

### 批次模式（推荐 Agent 多群 / 多图任务）

> v1.1.0 新增。一条命令、单个进程处理多个群聊 + 多张图，**微信全程不关**，避免自主 Agent 在多次调用之间误关微信。

```bash
# 先准备 send_plan.json
python scripts/wechat_send.py --manifest send_plan.json

# 想顺手把窗口截图存下来核验（不关闭微信）
python scripts/wechat_send.py --manifest send_plan.json --screenshot D:/verify.png
```

`send_plan.json` 示例（两张图发两个群，每张图前先发通用文本）：

```json
[
  { "contact": "群聊A", "message": "xxx", "images": ["D:/pics/a.png"] },
  { "contact": "群聊B", "message": "xxx", "images": ["D:/pics/b.png"] }
]
```

字段：`contact`（必填）、`message` / `message_file`、`images`（数组）、`files`（数组）。脚本结尾输出 `[RESULT] total=N ok=M fail=K`，每组打 `[SENT_OK]` / `[SENT_FAIL]`。

### 在 OpenClaw / WorkBuddy 中触发

对话中说出以下触发词即可：

- "给 XXX 发微信：消息内容"
- "打开微信发消息给 XXX"
- "通过微信发给 XXX：内容"
- "微信发送 XXX"

### 被其他 Skill 调用

```python
import subprocess

subprocess.run([
    "python",
    "scripts/wechat_send.py",
    "--contact", "好友昵称",
    "--message", "B站播报内容..."
])
```

## 🔬 技术原理

### 窗口连接

使用 `pywinauto` 的 `uia` 后端，窗口标题必须为**中文"微信"**（不是 "WeChat"）：

```python
app = Application(backend='uia').connect(title_re="微信", timeout=10)
```

### 中文输入方案

直接键入中文会出现编码问题，统一采用 **剪贴板 + Ctrl+V** 方案：

```python
pyperclip.copy(text)
send_keys("^v")  # Ctrl+V 粘贴
```

### 图片发送原理

将图片转为 BMP 格式，去掉前 14 字节文件头（保留 DIB 数据），写入 Windows 剪贴板 `CF_DIB` 格式，在聊天框 Ctrl+V 即可发送图片。

```python
# 核心代码（详见 scripts/wechat_send.py）
output = io.BytesIO()
img.convert("RGB").save(output, "BMP")
data = output.getvalue()[14:]  # 去掉 BMP 文件头
win32clipboard.SetClipboardData(win32con.CF_DIB, data)
```

## ⚠️ 注意事项

1. **微信窗口必须可见（已支持托盘自动恢复）**：v1.1.0 起即使被收进托盘也会自动还原前台；但 Agent 批次任务中请勿主动关闭 / 最小化微信（`×`/`Alt+F4` 仅最小化到托盘，关了会卡死后续）。
2. **登录状态**：通常自动登录，偶尔需要扫码确认
3. **联系人名称**：搜索精确匹配第一个结果
4. **UI 依赖**：依赖微信 Windows 版 UI 结构，版本更新可能失效
5. **仅发送，不读取**：本 Skill 不读取微信消息内容

## 📁 文件结构

```
wechat-desktop-claw-automatic-control/
├── SKILL.md              # Skill 定义（OpenClaw / WorkBuddy 识别用）
├── scripts/
│   └── wechat_send.py    # 核心自动化脚本
├── LICENSE               # Apache-2.0 开源协议
└── README.md            # 本文件
```

## 🤖 自主 Agent（Codex 等）驱动须知

- **脚本绝不关闭微信**；Agent 也不要主动关 / 最小化微信窗口。
- **多群多图请用 `--manifest` 批次模式**，一条命令干完全部，从根上消除“多次调用间误关微信”。
- **校验用 `--screenshot` 截图**，别靠“关了重开再瞅”——旧版无读取能力才会逼出这种笨办法，v1.1.0 已解决。
- 若微信被收进托盘，直接重跑脚本即可自动还原，无需人工重开。

## 🐛 问题反馈

- SkillHub 评论区：https://skillhub.cn/skills/wechat-desktop-claw-automatic-control
- 或联系作者：微光浮影

## 📄 协议

Apache License 2.0 — 自由使用、修改、分发。详见 [LICENSE](LICENSE) 文件。
