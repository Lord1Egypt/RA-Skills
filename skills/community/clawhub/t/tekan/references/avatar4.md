# Avatar4 模块

从一张照片生成逼真的数字人口播视频。

## 使用场景

当你需要从一张人像照片创建口播视频时 — 适用于营销、教育、产品演示或社交媒体内容。

## 子命令

| 子命令 | 使用场景 | 轮询？ |
|------------|-------------|--------|
| `run` | **默认。** 新请求，从提交到完成 | 是 — 等待至完成 |
| `submit` | 批量：提交多个任务不等待 | 否 — 立即退出 |
| `query` | 恢复：对已有的 `taskId` 继续轮询 | 是 — 等待至完成 |
| `list-captions` | 查看可用的字幕样式，用于 `--caption` | 否 |

## 用法

```bash
python {baseDir}/scripts/avatar4.py <subcommand> [options]
```

## 示例

### `run` — 完整流程（默认）

```bash
python {baseDir}/scripts/avatar4.py run \
  --image <fileId> \
  --text "大家好，欢迎来到我的频道！" \
  --voice <voiceId>
```

本地图片（自动上传）：

```bash
python {baseDir}/scripts/avatar4.py run \
  --image /path/to/photo.png \
  --text "欢迎使用特看视频。" \
  --voice LaaHTrXZCVOQmB1wZUhnwmbPTAWDFtW6
```

音频驱动模式：

```bash
python {baseDir}/scripts/avatar4.py run \
  --image /path/to/photo.png \
  --audio /path/to/recording.mp3
```

下载结果：

```bash
python {baseDir}/scripts/avatar4.py run \
  --image <fileId> --text "你好！" --voice <voiceId> \
  --output result.mp4
```

### `submit` — 批量

```bash
T1=$(python {baseDir}/scripts/avatar4.py submit \
  --image img1.png --text "第一段口播内容" --voice <id> -q)
T2=$(python {baseDir}/scripts/avatar4.py submit \
  --image img2.png --text "第二段口播内容" --voice <id> -q)

python {baseDir}/scripts/avatar4.py query --task-id "$T1"
python {baseDir}/scripts/avatar4.py query --task-id "$T2"
```

### `query` — 恢复

```bash
python {baseDir}/scripts/avatar4.py query --task-id <taskId> --timeout 1200
```

## 选项

### `run` 和 `submit`

| 选项 | 说明 |
|--------|-------------|
| `--image ID` | 图片 fileId 或本地文件路径（必需） |
| `--text TEXT` | 数字人朗读的 TTS 文本（与 `--voice` 配合使用） |
| `--voice ID` | 声音 ID（使用 `--text` 时必需） |
| `--audio ID` | 音频 fileId 或本地路径，用于音频驱动模式（`--text` 的替代方案） |
| `--mode MODE` | `avatar4`（默认）或 `avatar4Fast` |
| `--motion TEXT` | 自定义动作描述（最多 600 字符） |
| `--caption ID` | 字幕样式 ID |
| `--save-avatar` | 将该图片保存为可复用的自定义数字人 |
| `--notice-url URL` | 完成通知的 Webhook URL |

### 轮询（`run` 和 `query`）

| 选项 | 说明 |
|--------|-------------|
| `--timeout SECS` | 最大轮询时间，单位秒（默认：600） |
| `--interval SECS` | 轮询间隔，单位秒（默认：5） |

### 全局

| 选项 | 说明 |
|--------|-------------|
| `--output FILE` | 将结果视频下载到本地路径 |
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制 stderr 状态消息 |

## 模式对比

| 模式 | 最大时长 | 速度 | 画质 |
|------|-------------|-------|---------|
| `avatar4` | 120 秒 | 慢 | 最佳 |
| `avatar4Fast` | 120 秒 | 快 | 良好 |

## 字幕样式发现

使用 `list-captions` 查找可用的字幕样式，然后将 `captionId` 传给 `--caption`：

```bash
# 列出所有字幕样式
python {baseDir}/scripts/avatar4.py list-captions

# 在生成任务中使用 captionId
python {baseDir}/scripts/avatar4.py run \
  --image photo.png --text "你好！" --voice <voiceId> \
  --caption <captionId>
```

每个字幕条目包含一个 `thumbnail` URL 用于视觉预览。

## 输出

`run` 和 `query` 输出视频 URL。配合 `--json` 可获取完整 API 响应。
