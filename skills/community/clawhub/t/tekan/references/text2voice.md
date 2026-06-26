# Text2Voice 模块

将文字转换为语音音频，支持自定义声音、语速、情绪和发音规则。

## 使用场景

当你需要从文字生成语音音频 — 用于配音、旁白、TTS 预览，或作为 avatar4 视频生成的音频输入。

## 子命令

| 子命令 | 使用场景 | 轮询？ |
|------------|-------------|--------|
| `run` | **默认。** 新请求，从提交到完成 | 是 — 等待至完成 |
| `submit` | 批量：提交多个任务不等待 | 否 — 立即退出 |
| `query` | 恢复：对已有的 `taskId` 继续轮询 | 是 — 等待至完成 |

## 用法

```bash
python {baseDir}/scripts/text2voice.py <subcommand> [options]
```

## 示例

### 基础用法

```bash
python {baseDir}/scripts/text2voice.py run \
  --text "你好，欢迎使用文本转音频功能。" \
  --voice-id voice-888
```

### 调整语速和情绪

```bash
python {baseDir}/scripts/text2voice.py run \
  --text "今天天气真好！" \
  --voice-id voice-888 \
  --speed 1.2 \
  --emotion happy
```

### 使用发音规则

```bash
python {baseDir}/scripts/text2voice.py run \
  --text "行不行？你行行行。" \
  --voice-id voice-888 \
  --pron-rules '[{"oldStr":"行","newStr":"xing"}]'
```

### 下载音频

```bash
python {baseDir}/scripts/text2voice.py run \
  --text "你好，欢迎收看！" \
  --voice-id voice-888 \
  --output result.mp3
```

### 批量

```bash
T1=$(python {baseDir}/scripts/text2voice.py submit \
  --text "第一段内容" --voice-id voice-888 -q)
T2=$(python {baseDir}/scripts/text2voice.py submit \
  --text "第二段内容" --voice-id voice-888 -q)

python {baseDir}/scripts/text2voice.py query --task-id "$T1"
python {baseDir}/scripts/text2voice.py query --task-id "$T2"
```

## 选项

### `run` 和 `submit`

| 选项 | 说明 |
|--------|-------------|
| `--text TEXT` | 要转换的文字（必需） |
| `--voice-id ID` | 声音 ID（必需） |
| `--name NAME` | 声音名称标签 |
| `--speed FLOAT` | 语速（1.0 = 正常） |
| `--emotion NAME` | 情绪：`happy`、`sad`、`angry` 等 |
| `--origin-voice-file ID` | 原始声音文件 fileId 或本地路径 |
| `--pron-rules JSON` | 发音规则：`[{"oldStr":"行","newStr":"xing"}]` |
| `--board-id ID` | 看板 ID |
| `--notice-url URL` | Webhook URL |

### 轮询 / 全局

| 选项 | 说明 |
|--------|-------------|
| `--timeout SECS` | 最大轮询时间（默认：300） |
| `--interval SECS` | 轮询间隔（默认：3） |
| `--output FILE` | 将音频下载到本地路径 |
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制状态消息 |

## 费用

固定：每任务 **0.1 积分**。失败的任务会退还积分。

## 输出

```
status: success  cost: 0.1 credits  duration: 12.5s
  audio: https://example.com/audio.mp3
```

配合 `--json` 可获取声音元数据（语言、性别、年龄、口音、时长）。
