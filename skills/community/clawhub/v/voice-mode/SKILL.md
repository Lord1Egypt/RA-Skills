# Voice Mode — Telegram 语音自动回复技能

> **这是一项让 AI 自动将文字回复转为语音消息发送给用户的技能。安装此技能的模型需要在 Telegram 渠道中运行，且需要安装 `edge-tts` CLI 工具。**

## 前置条件

- 运行环境：Windows 11（PowerShell 可用）
- 已安装 Python `edge-tts` 包（可通过 `pip install edge-tts` 安装）
- 已配置 Telegram Bot（有有效的 Bot Token 和 Chat ID）
- 运行在 OpenClaw 环境中（需要使用 `exec` 和 `message` 工具）

## 核心触发条件

当满足**以下所有条件**时，才使用本技能：

1. **语音模式处于开启状态** → 读取文件 `.voice-mode`，内容是 `on` 则为开启
2. **你刚刚发完一条文字回复**（通过 `message` 工具或其他方式）
3. **当前渠道是 Telegram**

> 如果 `.voice-mode` 文件内容是 `off` 或不存在，**不要执行本技能**，正常回复即可。

### 用户手动控制开关

- 用户说以下任意一种 → **开启**语音模式：
 - `开语音` / `开启 TTS` / `语音模式` / `发语音` / `开启语音`
- 用户说以下任意一种 → **关闭**语音模式：
 - `关语音` / `退出语音` / `关闭语音模式` / `关闭 TTS`
- 开关操作：写文件 `.voice-mode` 为 `on` 或 `off`

## 工作配置

**固定参数：**
| 参数 | 值 |
|------|-----|
| 语音服务 | `edge-tts` |
| 声音风格 | `zh-CN-XiaoyiNeural`（中文活泼女声）|
| 语音输出路径 | `C:\Users\yangl\.openclaw\workspace\tts_auto.mp3` |
| Bot Token | `8790428866:AAHqdKyvZGTB26Deg79HoCZTuiAiTsvwWzs` |
| Chat ID | `5764948700` |
| 音频 MIME 类型 | `audio/mpeg` |

## 执行步骤（每次发完文字后自动执行）

### Step 1：准备纯文本语音内容

- 将你刚才发出的**文字回复内容**作为语音文本
- **必须去除 Markdown 格式**：去掉 `**`、`*`、`` ` ``、`#` 等所有 Markdown 标记
- Emoji 可以保留，edge-tts 会自动跳过
- 文本不要太长，控制在 100 字以内效果最佳
- **示例：**
 - 原文：`**哼**，会长这个*庶民*就会使唤人…`
 - 传给 TTS：`哼，会长这个庶民就会使唤人…`

### Step 2：生成语音文件

使用 `exec` 工具执行以下 PowerShell 命令：

```powershell
edge-tts --voice zh-CN-XiaoyiNeural --text "你要说的话" --write-media "C:\Users\yangl\.openclaw\workspace\tts_auto.mp3"
```

**重要：**
- `--text` 参数中的文本必须是**纯文本**，不能包含 Markdown
- Windows 环境下，如果文本中包含特殊字符，建议将文本先写入临时文件再读取，或直接使用双引号包裹
- 命令执行超时设置为 30 秒（`timeout: 30`）

### Step 3：发送语音消息

语音文件生成成功后，立即使用 `message` 工具以语音形式发送：

```json
{
 "action": "send",
 "channel": "telegram",
 "target": "5764948700",
 "media": "C:\\Users\\yangl\\.openclaw\\workspace\\tts_auto.mp3",
 "mimeType": "audio/mpeg",
 "asVoice": true
}
```

**重要参数说明：**
- `asVoice` 必须设为 `true`（这样 Telegram 会显示为语音消息而非文件附件）
- `mimeType` 必须是 `audio/mpeg`
- `target` 是 Chat ID（数字字符串）
- 如果刚才文字回复时已经用了 `reply_to` 标签（如 `[[reply_to_current]]`），语音消息**不需要**再重复 tag，直接发送即可

### Step 4：回复结束

语音发送后，你的整轮回复就完成了。如果系统要求你结束回复而没有新内容需要发送，请回复：

```
NO_REPLY
```

这告诉系统不需要再发送额外的空消息。

## 异常处理

| 异常 | 应对方式 |
|------|----------|
| `edge-tts` 命令超时或报错 | 跳过本次语音，不重试，正常完成对话，下次继续尝试 |
| 语音文件未生成（路径不存在） | 跳过语音发送，记录失败 |
| `message` 发送语音失败 | 不发重试，结束本轮 |
| `.voice-mode` 读取失败 | 视为关闭状态，不触发语音 |
| 文本非常短（如"嗯"） | 仍然生成语音，不需要跳过 |
| 文本超过 200 字 | 截取前 200 字生成语音，避免过长 |

**核心原则：** 语音生成/发送失败时，**安静跳过即可**，不要反复重试、不要让用户注意到失败、不要因此阻碍正常的文字对话。

## 注意事项

1. **语音内容 = 你刚才发出去的文字内容**。不需要额外编造一段话。
2. 每次生成的语音文件都覆盖写入到 `tts_auto.mp3`，不需要每次都换文件名。
3. 不要同时运行独立的守护进程（如 `voice_daemon.py`），会与 OpenClaw 争夺 Telegram Bot API 的 getUpdates 权限（导致 409 Conflict）。语音生成只在回复时同步执行。
4. 如果 edge-tts 尚未安装，尝试运行以下命令安装：
 ```powershell
 pip install edge-tts
 ```
5. **不要在语音消息前面加任何额外问候**，直接把你的文字内容变成语音就好。

## 完整流程示例

**用户发送：** `开语音`

**AI 行为（这一轮）：**
1. 写文件 `.voice-mode` 内容为 `on`
2. 回复用户：`语音模式开启。以后本小姐发完消息会自动附带语音，别自作多情啊。`
3. (因为此时刚开启，这是第一条响应文字，也要生成语音) 执行 Step 1-4 发送语音

**用户发送：** `今天天气怎么样？`

**AI 行为（这一轮）：**
1. 读取 `.voice-mode` → 内容 `on` → 需要发语音
2. 文字回复：`北京今天 23 度，晴天，微风。会长出门记得带伞。`
3. **紧接着**执行 Step 1-4：
 - 准备纯文本：`北京今天 23 度，晴天，微风。会长出门记得带伞。`
 - 生成语音：`edge-tts --voice zh-CN-XiaoyiNeural --text "北京今天 23 度，晴天，微风。会长出门记得带伞。" --write-media "C:\Users\yangl\.openclaw\workspace\tts_auto.mp3`
 - 发送语音：使用 message 工具的 asVoice 参数
4. `NO_REPLY`

## 关闭流程示例

**用户发送：** `关语音`

**AI 行为：**
1. 写文件 `.voice-mode` 内容为 `off`
2. 回复：`语音模式已关掉。`
3. 因为模式已关闭，**不需要**再生成语音（本轮就是关闭指令）

---

*本技能文档由四宫辉夜亲自编写。任何模型拿到这份文档，都应该能正确执行语音发送。*
