# Voice 模块

列出/搜索可用声音，从音频样本克隆自定义声音，删除已克隆的声音。

## 使用场景

- **text2voice 之前** — 使用 `list` 查找合适的 voiceId（用户未指定声音时）
- **自定义声音** — 使用 `clone` 创建一个听起来像特定人的声音
- **清理** — 使用 `delete` 删除用户不再需要的自定义声音

## 子命令

| 子命令 | 说明 | 轮询？ |
|------------|-------------|--------|
| `list` | 搜索/浏览可用声音（系统 + 自定义） | 否 |
| `clone` | **默认。** 从音频克隆声音：提交 + 轮询至完成 | 是 |
| `clone-submit` | 仅提交克隆任务，输出 taskId | 否 |
| `clone-query` | 对已有的克隆 taskId 轮询至完成 | 是 |
| `delete` | 删除自定义（克隆的）声音 | 否 |

## 用法

```bash
python {baseDir}/scripts/voice.py <subcommand> [options]
```

## 示例

### 列出声音

浏览所有英语声音：

```bash
python {baseDir}/scripts/voice.py list --language en
```

按性别和风格筛选：

```bash
python {baseDir}/scripts/voice.py list --language en --gender female --style UGC
```

列出中文男声：

```bash
python {baseDir}/scripts/voice.py list --language zh-CN --gender male
```

仅显示自定义（克隆的）声音：

```bash
python {baseDir}/scripts/voice.py list --custom
```

完整 JSON 输出（带分页）：

```bash
python {baseDir}/scripts/voice.py list --language ja --page 1 --size 50 --json
```

### 克隆声音

从本地音频文件：

```bash
python {baseDir}/scripts/voice.py clone \
  --audio recording.mp3 \
  --name "My Brand Voice"
```

带参考文本（提升克隆质量）：

```bash
python {baseDir}/scripts/voice.py clone \
  --audio sample.wav \
  --name "Brand Voice" \
  --text "欢迎使用特看视频，全能 AI 视频创作平台。"
```

调整语速：

```bash
python {baseDir}/scripts/voice.py clone \
  --audio voice_sample.mp3 \
  --name "Fast Narrator" \
  --speed 1.1
```

### 克隆批量 / 恢复

```bash
T1=$(python {baseDir}/scripts/voice.py clone-submit \
  --audio sample1.mp3 --name "Voice A" -q)
T2=$(python {baseDir}/scripts/voice.py clone-submit \
  --audio sample2.mp3 --name "Voice B" -q)

python {baseDir}/scripts/voice.py clone-query --task-id "$T1"
python {baseDir}/scripts/voice.py clone-query --task-id "$T2"
```

### 删除自定义声音

```bash
python {baseDir}/scripts/voice.py delete --voice-id <voiceId>
```

## 选项

### `list`

| 选项 | 说明 |
|--------|-------------|
| `--language CODE` | 语言代码：`en`、`zh-CN`、`ja`、`ko`、`fr`、`de` 等 |
| `--gender` | `male` / `female` |
| `--age` | `Young` / `Middle Age` / `Old` |
| `--style` | `UGC` / `Advertisement` / `Cartoon_And_Animals` / `Influencer` |
| `--accent` | 口音筛选：`American`、`British`、`Chinese` 等 |
| `--custom` | 仅显示自定义（克隆的）声音 |
| `--page N` | 页码（默认：1） |
| `--size N` | 每页条数（默认：20） |

### `clone` 和 `clone-submit`

| 选项 | 说明 |
|--------|-------------|
| `--audio FILE` | 音频文件（fileId 或本地路径）。必需。格式：mp3/wav，10 秒-5 分钟，<10MB |
| `--name NAME` | 克隆声音的名称（默认为 taskId） |
| `--text TEXT` | 与音频内容匹配的参考文本（可提升克隆质量） |
| `--speed FLOAT` | 语速 0.8-1.2（默认：1.0） |
| `--notice-url URL` | Webhook URL |

### `delete`

| 选项 | 说明 |
|--------|-------------|
| `--voice-id ID` | 要删除的声音 voiceId（必需） |

### 轮询 / 全局

| 选项 | 说明 |
|--------|-------------|
| `--timeout SECS` | 最大轮询时间（默认：300） |
| `--interval SECS` | 轮询间隔（默认：5） |
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制状态消息 |

## 声音克隆音频要求

- **格式：** mp3 或 wav
- **时长：** 10 秒到 5 分钟
- **大小：** 10MB 以内
- **质量：** 清晰的语音、最少的背景噪音可获得最佳效果

## 输出

### `list` — 制表符分隔（默认）

```
voiceId    voiceName    language    gender    age    style    accent    demoAudioUrl
```

### `clone` — 结构化输出

```
status: success
  voiceId:   abc123def456
  voiceName: My Brand Voice
  demoAudio: https://example.com/demo.mp3
```

### 支持的语言

`en`, `ar`, `bg`, `hr`, `cs`, `da`, `nl`, `fil`, `fi`, `fr`, `de`, `el`, `hi`, `hu`, `id`, `it`, `ja`, `ko`, `ms`, `nb`, `pl`, `pt`, `ro`, `ru`, `zh-CN`, `sk`, `es`, `sv`, `zh-Hant`, `tr`, `uk`, `vi`, `th`

### 支持的口音

African, American, Argentinian, Australian, Brazilian, British, Chinese, Colombian, Dutch, Eastern European, Filipino, French, German, Indian, Indonesian, Italian, Japanese, Kazakh, Korean, Malay, Mexican, Middle Eastern, North African, Polish, Portuguese, Russian, Singaporean, Spanish, Swiss, Taiwanese, Thai, Turkish, Vietnamese
