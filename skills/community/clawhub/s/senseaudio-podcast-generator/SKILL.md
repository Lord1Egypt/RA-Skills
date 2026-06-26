---
name: podcast-generator
description: 双主播播客生成器 - 输入话题自动生成播客音频，支持LLM智能生成脚本、克隆音色、文字生成音色、自定义语速语调、多种音色可选
homepage: https://senseaudio.cn
metadata:
  audioclaw:
    homepage: https://senseaudio.cn
    requires:
      bins:
        - ffmpeg
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
---

# Podcast Generator Skill

双主播播客生成器 - 将话题文本转换为播客音频

---

## 🚀 怎么用

### 方式一：启动 Web 页面

在 OpenClaw 聊天中说：

```
启动播客生成器
```

Agent 会自动启动 Web 服务并打开浏览器页面 http://localhost:5000，你可以在页面中可视化操作。

### 方式二：直接生成播客

在 OpenClaw 聊天中说：

```
播客生成器帮我生成以下话题：人工智能的未来发展
```

或发送完整文案：

```
播客生成器帮我生成以下文案：
[你的播客脚本内容]
```

Agent 会自动生成 MP3 音频并发送给你。

---

## 🎯 两种调用模式（按渠道自动选择）

### ⚠️ 重要提示：根据使用场景选择正确模式！

| 使用场景 | 正确模式 | 原因 |
|---------|---------|------|
| **本地终端**（直接在电脑上用 OpenClaw） | 模式 A | Web 页面可直接打开浏览器 |
| **IM 渠道**（飞书/Telegram/Discord等） | **模式 B** | Web 页面无法远程访问，只能聊天生成 |

**❌ 常见错误**：在飞书里说 "生成播客"，期望打开 Web 页面
- **原因**：Web 页面只运行在本地服务器，IM 用户无法访问
- **正确做法**：在 IM 里直接发送文案，使用模式 B

---

### 模式 A：Web 页面模式（仅限本地终端）

**适用场景**：用户在本地电脑直接使用 OpenClaw（非 IM 渠道）

**触发关键词**：
- "生成播客"
- "播客"
- "启动播客"

**流程**：
1. 启动 Flask Web 服务（端口 5000）
2. 自动打开浏览器访问 http://localhost:5000
3. 用户在 Web 页面操作

**优势**：
- 可视化界面，操作直观
- 支持实时试听、参数调整
- 可查看历史生成记录

**⚠️ 限制**：仅限本地访问，IM 渠道无法使用！

---

### 模式 B：聊天生成模式（IM 渠道默认）⭐

**适用场景**：通过飞书、Telegram、Discord 等 IM 渠道发送消息

**触发关键词**：
- "生成播客"（IM 渠道自动识别）
- "直接生成播客"
- 或用户直接提供播客文案

**流程**：
1. Agent 检测到 IM 渠道 → 自动使用模式 B
2. 发送生成信息卡片，告知默认配置
3. 用户回复播客文案（如果尚未提供）
4. Agent 调用 API 生成音频
5. 根据渠道发送结果

**默认配置**：
- 男声：male_0004_a（青树）
- 女声：female_0001_a（之心）
- 语速：1.0
- 语调：男声 0，女声 2

---

## 渠道自动识别规则

**Agent 应根据 `inbound_meta.chat_type` 或 `channel` 自动选择模式：**

| 渠道类型 | 选择模式 | 判断条件 |
|---------|---------|----------|
| **飞书（feishu）** | 模式 B | `channel: "feishu"` |
| **Telegram** | 模式 B | `channel: "telegram"` |
| **Discord** | 模式 B | `channel: "discord"` |
| **Signal** | 模式 B | `channel: "signal"` |
| **本地终端** | 模式 A | 无 channel 信息或 `chat_type: "terminal"` |

**判断逻辑**：

```python
# Agent 检测渠道
if inbound_meta.get("channel") in ["feishu", "telegram", "discord", "signal"]:
    # IM 渠道 → 模式 B（聊天生成）
    use_chat_mode()
else:
    # 本地终端 → 模式 A（Web 页面）
    start_web_server()
```

---

## 触发后的详细交互流程

### 模式 A（Web 页面）- 仅限本地终端

**触发条件**：用户在本地终端运行 OpenClaw

用户说："生成播客"

**Agent 执行**：

```bash
# 1. 启动 Web 服务（后台运行）
python3 app.py &

# 2. 打开浏览器
xdg-open http://localhost:5000
```

**Agent 发送消息**：
```
🎙️ 播客生成器已启动！

🌐 Web 页面已打开：http://localhost:5000

在页面中你可以：
• 输入话题，AI 自动生成播客脚本
• 选择音色（支持克隆音色、文字生成音色）
• 调整语速、语调
• 实时试听效果
```

**⚠️ 注意**：此模式仅限本地访问，IM 渠道无法打开浏览器！

---

### 模式 B（聊天生成）- IM 渠道默认 ⭐

**触发条件**：用户通过飞书/Telegram/Discord 等 IM 渠道发送消息

用户说："生成播客"（Agent 自动识别 IM 渠道）

**Agent 发送配置卡片**：
```
🎙️ 聊天生成播客

⚠️ 你正在通过 IM 渠道使用，Web 页面无法远程访问。
当前使用聊天生成模式。

📋 默认配置：
• 男声：青树（male_0004_a）
• 女声：之心（female_0001_a）
• 语速：1.0 倍
• 语调：男声 0，女声 2

✏️ 请发送你想生成的播客文案或话题：

💡 提示：直接发送文案即可，例如：
"生成播客，话题是人工智能的未来发展"
```

用户回复文案后：

**Agent 执行**：
```bash
python3 scripts/generate.py --topic "用户提供的文案"
```

**Agent 发送结果**：
- **飞书渠道**：上传云盘 + 发送链接
- **其他渠道**（Telegram/Discord/Signal）：直接发送 MP3 文件

---

## ⚠️ 飞书渠道重要说明

**飞书不支持直接发送音频文件到对话窗口！**

解决方案：上传到云盘，发送云盘链接给用户。

### 飞书云盘上传流程

**步骤 1：获取 Folder Token**

从飞书云盘文件夹 URL 直接复制 token 部分（URL 最后一段）。

**步骤 2：上传到云盘**

```python
url = 'https://open.feishu.cn/open-apis/drive/v1/files/upload_all'
form = {
    'file_name': '播客_话题.mp3',
    'parent_type': 'explorer',
    'parent_node': folder_token,
    'size': file_size,
    'file': mp3_data
}
```

**步骤 3：发送链接**

```
🎙️ 播客已上传到云盘！

**链接**: https://my.feishu.cn/drive/file/{file_token}

点击链接即可播放！
```

---

## 其他 IM 渠道

| 渠道 | 发送方式 | 说明 |
|------|----------|------|
| **飞书** | 云盘上传 + 链接 | 无法直接发音频 |
| **Telegram** | 直接发送 MP3 | ✅ 支持 |
| **Discord** | 直接发送 MP3 | ✅ 支持 |
| **Signal** | 直接发送 MP3 | ✅ 支持 |

Agent 会根据渠道自动选择正确的发送方式。

---

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--topic` | 必填 | 话题内容（建议 50-200 字） |
| `--speed` | 1.0 | 语速（0.5-2.0） |
| `--pitch-male` | 0 | 男声语调（-12~12） |
| `--pitch-female` | 2 | 女声语调（-12~12） |
| `--male-voice` | male_0004_a | 男声音色 ID |
| `--female-voice` | female_0001_a | 女声音色 ID |
| `--output` | 自动生成 | 输出文件路径 |

---

## 可选音色

### 免费音色（默认）

| 音色 ID | 名称 | 特点 |
|---------|------|------|
| male_0004_a | 青树 | 沉稳大气 |
| female_0001_a | 之心 | 亲切自然 |

### 付费音色（SVIP 限免）

| 音色 ID | 名称 | 特点 |
|---------|------|------|
| male_0028_d | 激昂解说 | 充满激情 |
| female_0035_d | 甜美解说 | 活泼可爱 |

### 特色功能（SenseAudio 平台）

- 🔊 **克隆音色**：上传音频样本克隆你的声音
- ✨ **文字生成音色**：用文字描述生成专属音色

---

## 项目依赖

| 依赖 | 说明 |
|------|------|
| Flask 服务 | 端口 5000 |
| FFmpeg | 音频合并（已安装） |
| SenseAudio TTS | 语音合成 |
| qwen3.5-plus | LLM 脚本生成 |

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 服务未启动 | Flask 未运行 | `python3 app.py` |
| API Key 无效 | SENSEAUDIO_API_KEY 错误 | 检查 openclaw.json |
| 云盘上传 forbidden | folder_token 错误 | 使用正确的云盘 URL |
| 生成失败 | TTS API 错误 | 检查积分余额 |

---

## 详细文档

完整 API 文档见：`references/AGENT.md`

