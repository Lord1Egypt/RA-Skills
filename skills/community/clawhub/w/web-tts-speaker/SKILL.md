---
name: web-tts-speaker
version: 3.2.1
description: "网页一键朗读：URL/文本 → TTS语音 → 多渠道自动匹配（飞书语音条 / 微信/TG/Discord MP3）"
metadata:
  openclaw:
    requires: { bins: ["python3"] }
    install:
      - id: python
        kind: pip
        package: "-r requirements.txt"
---

# web-tts-speaker v3.2.1

**网页/文字 → TTS语音 → 多渠道自动匹配推送**

> 📢 替代 [web-reader-tts](https://clawhub.ai/packages/web-reader-tts) — 所有功能由本项目统一覆盖。

## 一句话用法

```bash
python cli.py --url https://example.com/article
python cli.py --text "你好世界"
```

默认 `--channel auto`，生成所有格式，Agent 按来源渠道自动取用。

---

## 🧠 Agent 工具定义

当用户希望**朗读网页**或**将文字转为语音**时，按以下流程操作。

### 触发条件

用户消息中出现以下意图之一：
- "朗读 / 读一下 / 帮我读 / 听一下" + **URL**
- "朗读 / 读一下 / 帮我读 / 听一下" + **文本内容**
- 直接发了一个 **URL**（自动朗读）
- "转语音 / 生成语音 / TTS"

### 执行流程

#### Step 1：提取目标文本

```
用户说 "朗读 https://abc.com/article"  → 取 URL
用户说 "帮我读一下这段：你好世界"      → 取文本
用户直接发一个 URL                     → 取 URL
```

#### Step 2：获取来源渠道

从当前消息的 `inbound context` 中读取 `channel` 字段：

```json
// inbound metadata 示例
{ "channel": "openclaw-weixin" }   // 微信
{ "channel": "feishu" }           // 飞书
{ "channel": "telegram" }         // Telegram
{ "channel": "discord" }          // Discord
```

#### Step 3：调用 CLI

```bash
cd C:\Users\www\.openclaw\agents\tech\workspace\skills\web-tts-speaker

# 朗读网页（自动模式）
python cli.py --url "https://example.com/article"

# 文字转语音（自动模式）
python cli.py --text "你好世界"
```

使用 **exec 工具** 执行，并捕获 stdout。

#### Step 4：解析输出标记

CLI 输出多个渠道标记。根据来源渠道选取对应的那个：

| 来源 channel | 取用标记 | 发送文件 |
|-------------|---------|---------|
| `openclaw-weixin` | `[WECHAT_VOICE]` | `file=xxx.mp3` |
| `feishu` | `[FEISHU_VOICE]` | `file=xxx.opus` |
| `telegram` | `[TELEGRAM_VOICE]` | `file=xxx.mp3` |
| `discord` | `[DISCORD_VOICE]` | `file=xxx.mp3` |

#### Step 5：发送语音

用 `message` 工具发送，channel 和 file 从所选标记中提取：

**微信：**
```python
message(
    action: "send",
    channel: "openclaw-weixin",
    media: "/path/to/voice.mp3"
)
```

**飞书：**
```python
message(
    action: "send",
    channel: "feishu",
    asVoice: true,
    filePath: "/path/to/voice.opus"
)
```

**Telegram / Discord：**
```python
message(
    action: "send",
    channel: "telegram",   # 或 "discord"
    media: "/path/to/voice.mp3"
)
```

---

## 完整调用示例（给 Agent 参考）

```
用户: 朗读 https://zshttp.com/2981.html

→ 检测来源: inbound metadata.channel = "openclaw-weixin"
→ 执行: exec(command="cd C:\\Users\\www\\.openclaw\\workspace\\skills\\web-tts-speaker && python cli.py --url https://zshttp.com/2981.html", timeout=300)
→ 解析输出:
   找到 [WECHAT_VOICE] 标记
   file=C:\xxx\voice_195836.mp3
→ 发送:
   message(action="send", channel="openclaw-weixin", media="C:\xxx\voice_195836.mp3")
→ 回复用户: "语音已发到微信"
```

```
用户: 帮我读一下这篇文章的摘要：今天天气真好...

→ 检测来源: inbound metadata.channel = "feishu"
→ 执行: exec(command="cd C:\\Users\\www\\.openclaw\\workspace\\skills\\web-tts-speaker && python cli.py --text '今天天气真好...'")
→ 解析输出:
   找到 [FEISHU_VOICE] 标记
   file=C:\xxx\voice_xxxxxx.opus
→ 发送:
   message(action="send", channel="feishu", asVoice=true, filePath="C:\xxx\voice_xxxxxx.opus")
→ 回复用户: "语音条已发到飞书"
```

---

## 快速命令

```bash
# 自动模式（推荐）：一次性生成所有格式
python cli.py --url https://example.com/article
python cli.py --text "你好世界"

# 指定单渠道
python cli.py --channel feishu --text "你好"
python cli.py -c wechat --text "你好"
```

## 支持渠道

| 渠道 | 格式 | 发送方式 |
|------|------|---------|
| **feishu** | `.opus` (16kHz) | `asVoice=true` |
| **wechat** | `.mp3` (24kHz) | `media=xxx` |
| **telegram** | `.mp3` (24kHz) | `media=xxx` |
| **discord** | `.mp3` (24kHz) | `media=xxx` |

> ⚠️ **微信说明**：`openclaw-weixin` 插件暂未实现原生语音气泡发送（[GH#61031](https://github.com/openclaw/openclaw/issues/61031)），当前以 MP3 文件形式发送。

## 长文本支持

自动分块 + 拼接，不限长度。

## 语音角色

```bash
python cli.py --text "你好" --voice zh-CN-YunxiNeural
```

常用中文语音：
- `zh-CN-XiaoxiaoNeural` — 晓晓（女声，默认）
- `zh-CN-YunxiNeural` — 云希（男声，活泼）
- `zh-CN-YunyangNeural` — 云扬（男声，新闻）
- `zh-CN-XiaoyiNeural` — 晓伊（女声，柔和）

## 依赖

```bash
pip install edge-tts beautifulsoup4 requests
```

也依赖系统安装的 **FFmpeg**。
