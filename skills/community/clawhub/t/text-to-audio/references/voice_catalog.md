# edge-tts 语音目录（中文 + 英文）

> 运行 `python -m edge_tts --list-voices` 获取最新完整列表

## 标准普通话语音

| 别名 | 语音 ID | 性别 | 风格标签 | 气质描述 |
|------|---------|------|----------|----------|
| xiaoxiao | zh-CN-XiaoxiaoNeural | 女 | News, Novel | 温暖，推荐朗读课文/故事 |
| xiaoyi | zh-CN-XiaoyiNeural | 女 | Cartoon, Novel | 活泼，适合儿童故事 |
| yunxi | zh-CN-YunxiNeural | 男 | Novel | 阳光，适合叙事 |
| yunjian | zh-CN-YunjianNeural | 男 | Sports, Novel | 激情，适合朗诵 |
| yunyang | zh-CN-YunyangNeural | 男 | News | 专业，适合新闻/说明文 |
| yunxia | zh-CN-YunxiaNeural | 男 | Cartoon, Novel | 可爱，适合对话 |

## 方言语音

| 别名 | 语音 ID | 性别 | 方言 | 气质 |
|------|---------|------|------|------|
| xiaobei | zh-CN-liaoning-XiaobeiNeural | 女 | 东北话 | 幽默 |
| xiaoni | zh-CN-shaanxi-XiaoniNeural | 女 | 陕西话 | 明亮 |

## 英文语音（en-US）

| 别名 | 语音 ID | 性别 | 风格标签 | 气质描述 |
|------|---------|------|----------|----------|
| jenny | en-US-JennyNeural | 女 | General | 温暖自然，推荐朗读（默认英文） |
| aria | en-US-AriaNeural | 女 | News, Novel | 自信，适合新闻/叙述 |
| emma | en-US-EmmaNeural | 女 | Conversation, Copilot | 活泼，适合对话/讲解 |
| guy | en-US-GuyNeural | 男 | News, Novel | 激情，适合朗诵/叙事 |
| christopher | en-US-ChristopherNeural | 男 | News, Novel | 权威，适合新闻/分析 |
| michelle | en-US-MichelleNeural | 女 | News, Novel | 亲切，适合日常叙述 |

> 💡 **语言与语音匹配提示**：中文语音读英文会有口音，英文语音读中文效果也差。请根据文本语言选择对应语音组。
> 以上语音 ID 均经过实际测试验证可用（2026-04-29）。

## 语速参数说明

edge-tts 的 `rate` 参数格式为百分比字符串：

| 参数值 | 效果 | 推荐场景 |
|--------|------|----------|
| `-30%` | 很慢 | 低年级慢速朗读 |
| `-20%` | 偏慢 | 课文跟读 |
| `-10%` | 略慢 | 日常朗读（推荐默认） |
| `+0%` | 正常 | 正常语速 |
| `+10%` | 略快 | 快速浏览 |
| `+20%` | 偏快 | 不推荐 |
| `+50%` | 很快 | 不推荐 |

**小学课文朗读推荐**：`rate="-10%"` 配合 `voice="xiaoxiao"`

## 风格说明

edge-tts 部分语音支持风格标签（如 News、Novel），目前通过 edge-tts Python 包调用时，风格为自动选择，暂不支持手动指定。

如需更精细的情感控制（如 [whispers]、[laughs]），考虑使用 ElevenLabs TTS Skill。
