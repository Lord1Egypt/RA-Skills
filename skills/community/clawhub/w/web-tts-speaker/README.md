# Web TTS Speaker v3.2.0

**网页/文字 → TTS语音 → 多渠道自动匹配推送**

一键朗读网页或文字，自动生成适配不同平台的语音格式。不调飞书/微信 API，Agent 负责发送，脚本只做三件事：**提取文字 → 生成语音 → 输出标准化标记**。

> 📢 **替代 [web-reader-tts](https://clawhub.ai/packages/web-reader-tts)**
> Web Reader TTS 已废弃，所有功能由本项目统一覆盖。新增多渠道支持（飞书语音条/微信 MP3/TG/Discord）、自动格式匹配、零飞书 API 依赖。

---

## 快速开始

```bash
# 安装依赖
pip install edge-tts beautifulsoup4 requests

# 自动模式：生成全部渠道格式
python cli.py --url https://example.com/article
python cli.py --text "你好世界"

# 指定单渠道
python cli.py -c feishu --text "你好世界"
python cli.py -c wechat --text "你好世界"
```

---

## 渠道支持

| 渠道 | 输出格式 | 声道/码率 | Agent 发送方式 |
|------|---------|-----------|---------------|
| `-c feishu` | `.opus` | 单声道 16kHz / 12kbps | `asVoice=true` → 飞书语音气泡 |
| `-c wechat` | `.mp3` | 单声道 24kHz / 48kbps | `media=xxx` → 微信文件消息 |
| `-c telegram` | `.mp3` | 单声道 24kHz / 48kbps | `media=xxx` → TG 文件消息 |
| `-c discord` | `.mp3` | 单声道 24kHz / 48kbps | `media=xxx` → Discord 文件消息 |
| `-c auto`（默认） | 全部 | — | Agent 按来源渠道自动取用 |

---

## 使用场景

### 朗读网页

```bash
python cli.py -c feishu --url https://example.com/article
```

自动提取正文（过滤导航/广告/页脚），支持中英文。

### 文字转语音

```bash
python cli.py -c wechat --text "会议提醒：下午3点有项目评审"
```

适合快速生成通知/提醒语音。

### 指定语音角色

```bash
python cli.py -c feishu --text "你好" --voice zh-CN-YunxiNeural
```

常用中文语音：

| 语音参数 | 角色 |
|---------|------|
| `zh-CN-XiaoxiaoNeural` | 晓晓（女声，默认） |
| `zh-CN-YunxiNeural` | 云希（男声，活泼） |
| `zh-CN-YunyangNeural` | 云扬（男声，新闻） |
| `zh-CN-XiaoyiNeural` | 晓伊（女声，柔和） |

### 自定义输出

```bash
python cli.py -c wechat --text "通知" -o notice.mp3
```

---

## 输出标记（Agent 读取）

自动模式输出标准化标记块，Agent 根据请求来源渠道自动选取对应文件：

```text
[FEISHU_VOICE]
channel=feishu
file=/path/to/voice.opus
text=会议提醒：下午3点有项目评审...
dur=15
size=22124
full=飞书语音气泡
[/FEISHU_VOICE]

[WECHAT_VOICE]
channel=wechat
file=/path/to/voice.mp3
text=会议提醒：下午3点有项目评审...
dur=15
size=88560
full=微信文件消息
[/WECHAT_VOICE]
```

---

## 架构

```
URL/文本
    │
    ▼
网页提取正文 ──→ Edge TTS 分块合成 ──→ 合并 WAV ──→ 多渠道转码
    │                                                    │
    │                                         ┌──────────┼──────────┐
    │                                         ▼          ▼          ▼
    │                                     feishu     wechat     telegram/discord
    │                                    (.opus)    (.mp3)       (.mp3)
    │                                         │          │            │
    └───输出标准化标记供 Agent 解析 ──────────┘──────────┘────────────┘
                                                    │
                                                    ▼
                                           message() → 渠道语音发送
```

---

## 依赖

| 依赖 | 用途 | 安装 |
|------|------|------|
| Python 3.8+ | 运行环境 | — |
| edge-tts | 微软 Edge 神经网络 TTS（免费，无需 API Key） | `pip install edge-tts` |
| beautifulsoup4 | 网页正文提取 | `pip install beautifulsoup4` |
| requests | 网页抓取 | `pip install requests` |
| FFmpeg | 音频转码 | [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) / `brew install ffmpeg` / `apt install ffmpeg` |

---

## 与 web-reader-tts 对比

| 特性 | web-reader-tts（已废弃） | web-tts-speaker ✅ |
|------|------------------------|-------------------|
| 飞书语音条 | ❌ 需直调 API | ✅ 生成 Opus，asVoice 发送 |
| 微信支持 | ❌ | ✅ MP3 文件消息 |
| TG/Discord 支持 | ❌ | ✅ |
| 自动渠道匹配 | ❌ | ✅ `--channel auto` |
| 飞书 API 依赖 | ✅ 需 OAuth | ❌ 零依赖 |
| 本地 TTS | ✅ (pyttsx3) | ❌（Edge TTS 质量更高） |

---

## 版本

**v3.2.0** — 简化重构版，砍掉所有飞书 API 直调代码，新增多渠道支持