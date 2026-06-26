---
name: winmsg-tts
description: Windows本地TTS朗读技能。通过WM_COPYDATA消息把AI回复实时发送到迷你窗口朗读，支持中英文标点分割、队列顺序播放、语速音量滑块调节，零token消耗，完全本地运行。
version: 1.3.0
metadata:
  openclaw:
    emoji: "🔊"
    homepage: https://github.com/512548510/openclaw-skills
  tags:
    - tts
    - voice
    - windows
    - speech
---

# winmsg-tts

Windows 本地 TTS 朗读技能。通过 WM_COPYDATA 消息把 AI 回复实时发送到迷你窗口朗读，支持中英文标点分割、队列顺序播放、语速音量滑块调节，零 token 消耗，完全本地运行。

## 核心规则（重要！）

### 开启朗读模式
- 用户说"开启朗读模式"时 → 自动启动 TTS 迷你窗口
- 启动后第一条消息要说点自然的、有上下文的话，不要说通用测试句
- 把 HWND 和启动成功状态告诉用户

### 朗读中（每次回复必须执行！）
**TTS 模式下，AI 的每一条用户可见回复，都必须同步调用 sendmsg_hwnd.py 发送到小窗口朗读。不得遗漏。不得只发文字不转发音频。**

流程：
1. 收到用户消息
2. 生成回复文字
3. 调用 sendmsg_hwnd.py：`python sendmsg_hwnd.py <回复内容>`
4. 把同一回复文字也发给用户（webchat）

### 关闭朗读模式
- 用户说"关闭朗读模式"时 → 发送精确退出命令：`python sendmsg_hwnd.py --quit`
- 只关闭自己的 TTS 窗口，不会影响其他进程
- 关闭后告知用户

### 规则要点
- 只把用户看得见的回复发给 TTS 窗口，不要发内部推理
- 开启时说自然的话，不要每次都说"这是一条测试消息"
- 滑块调节实时生效，无需重启

## 技术特性

- **自动分句**：按中英文标点（`。` `；` `：` `！` `？` `……` `.` `,` `;` `:` `!` `?`）分割句子，保留标点到句尾
- **队列播放**：多句按顺序排队播放，不重叠，不打断
- **label 同步**：窗口文字随播放进度同步更新，每播一句更新一句
- **无弹窗**：使用 CREATE_NO_WINDOW (0x08000000) + Base64 编码，彻底解决 PowerShell 窗口问题
- **配置持久化**：语速/音量保存到配置文件，断电重启后恢复上次设置
- **精确关闭**：通过 `__QUIT__` 命令关闭自己的窗口，不杀其他进程

## 文件说明

- `scripts/wmserver_20260327.py` — TTS 接收端，320×90像素迷你窗口，无边框右下角永远置顶
- `scripts/sendmsg_hwnd.py` — 发送端，通过 WM_COPYDATA 发送字符串；支持 `--quit` 精确关闭
- `config/tts_speed.txt` — 语速配置（-10 到 +10）
- `config/volume.txt` — 音量配置（0-100）
- `config/wmserver_hwnd.txt` — 当前窗口 HWND（运行时生成）

## 使用方法

1. 安装依赖：`pip install pywin32`
2. 启动 TTS：`python scripts/wmserver_20260327.py`
3. 发送信息：`python scripts/sendmsg_hwnd.py <消息内容>`
4. 关闭 TTS：`python scripts/sendmsg_hwnd.py --quit`

## 技术原理

- WM_COPYDATA = 0x004A + COPYDATASTRUCT 结构，跨进程传字符串
- PowerShell `System.Speech.Synthesis.SpeechSynthesizer` TTS 引擎
- Base64 编码命令避免中文和长度限制
- 消息队列顺序播放，不重叠
- tkinter 做 UI，overrideredirect(True) 无边框窗口
- CREATE_NO_WINDOW 禁止 PowerShell 弹窗
- `__QUIT__` 命令通过窗口类名精确关闭窗口，不影响其他进程
- 配置持久化到文本文件，断电重启后恢复上次设置

## UI 布局（320×90）

```
[白色文字显示区域（当前播放的句子）]
[慢]━━━●━━━━━━━━[快]   ← 语速滑块
[小]━━━●━━━━━━━━[大]   ← 音量滑块
```

- 背景：深灰色 #2d2d2d
- 文字：白色 #FFFFFF，微软雅黑 10pt 粗体
- 滑块轨道：灰色 #555555
- 滑块把手：白色 oval

## 系统要求

- Windows 系统
- Python 3.8+
- pywin32
