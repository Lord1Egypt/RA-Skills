---
name: ym-mediatoolkit
version: 4.3.1
description: 自然语言媒体助手 - 视频压缩、MP4/MOV 封面提取、音频转换、字幕识别
author: your_name
tags:
  - video
  - compression
  - thumbnail
  - audio
  - streaming
  - ffmpeg
categories:
  - media
  - utility
clawhub:
  entrypoint: python run.py
  runtime: python3
  http_port: 8080
---

# YM MediaToolkit

自然语言媒体助手，支持从远程视频 URL、当前工作目录内的本地视频文件、或配置过 `media_roots` 的本地媒体目录直接处理：

- 自然语言调用
- 视频压缩
- MP4/MOV 封面提取
- 音频提取与转换：MP3 / WAV / AAC / M4A
- OCR / ASR 字幕识别
- emlet 字幕二次分句
- 批量处理
- JSON 驱动媒体流水线

## 依赖

```bash
pip install -r requirements.txt
```

系统需要安装：

```bash
ffmpeg
ffprobe
```

字幕识别依赖已内置在 `requirements.txt`，包括 `faster-whisper`、`paddlepaddle`、`paddleocr`。

## 维护

维护、发布、测试和排障流程见 [MAINTENANCE.md](./MAINTENANCE.md)。

## 命令行

```bash
python run.py -a <action> -i '<json>'
```

也可以从 JSON 文件读取参数：

```bash
python run.py -i params.json
```

## HTTP 服务

```bash
python run.py --serve
```

默认监听 `127.0.0.1:8080`。

健康检查：

```http
GET /health
```

异步长任务：

```http
POST /skill/jobs
GET /skill/jobs/<job_id>
GET /skill/jobs
```

## 功能

输入源字段可使用 `video_url`、`url` 或 `source`，三者等价。远程输入仅支持 `http/https`，本地输入默认限制在当前工作目录内；需要访问绝对路径时，通过请求参数 `media_roots` 或环境变量 `YM_MEDIA_ROOTS` 配置允许的媒体根目录。

## 返回协议

从 `4.1.0` 开始，所有 action 都会返回稳定协议字段：

| 字段 | 说明 |
|------|------|
| `status` | `success` / `partial` / `skipped` / `error` |
| `code` | 稳定机器码，例如 `ok`、`missing_source`、`output_exists`、`parse_failed` |
| `reply` | 适合聊天展示的简短中文回复 |
| `hint` | 面向调用方或用户的下一步建议 |

原有业务字段会继续保留，例如 `output_path`、`saved_path`、`outputPath`、`manifest_path`、`info`、`captions`、`result`。

默认输出目录：

| 类型 | 默认目录 |
|------|----------|
| 压缩视频 | `output/videos` |
| 音频 | `output/audio` |
| 封面 | `output/thumbs` |

所有会写文件的接口都支持 `overwrite`，默认 `true`。设置为 `false` 时，如果输出文件已存在会直接返回错误。

## 3.0.3 更新

- 支持当前工作目录内的本地视频文件输入。
- 统一 `video_url` / `url` / `source` 三种输入字段。
- 增加默认输出目录：`output/videos`、`output/audio`、`output/thumbs`。
- 增加 `overwrite` 覆盖策略，避免误覆盖已有文件。

## 4.0.0 更新

- 新增自然语言入口 `chat`，适合 Claw 直接转发用户聊天文本。
- 新增 `media_roots` 白名单，支持处理授权目录内的绝对路径文件。
- 自然语言命令支持提取音频、提取封面、压缩、查看信息、JSON 流水线。
- `chat` 返回 `reply` 和结构化 `result`，同时兼顾聊天展示和自动化消费。

## 4.0.1 更新

- 新增 `subtitle` 推荐入口，支持 `asr` / `ocr` / `fusion` 模式。
- 新增 `asr` 和 `ocr` 单独调试入口。
- 字幕统一输出 SRT-like JSON：`captionTxt`、`startTimeUs`、`endTimeUs`、`source`、`confidence`。
- `chat` 支持“识别字幕 / 提取字幕 / 转字幕 / 生成字幕”等自然语言命令。

## 4.0.2 更新

- 将 `faster-whisper`、`paddlepaddle`、`paddleocr` 纳入默认 `requirements.txt`。
- 字幕识别从“可选依赖”调整为默认安装能力。
- 运行时仍保留缺依赖 JSON error，方便定位未重新安装依赖的环境。

## 4.1.0 更新

- 所有 action 统一补齐 `code`、`reply`、`hint`，方便 Claw 和后续渠道适配。
- 增加稳定错误码：`missing_source`、`source_not_allowed`、`output_exists`、`parse_failed`、`missing_steps`、`unsupported_action`、`ffmpeg_failed`、`missing_asr_dependency`、`missing_ocr_dependency`。
- 保持旧字段兼容，不改变现有 action 名称、HTTP endpoint 和底层媒体处理逻辑。

## 4.1.1 更新

- 新增 `caption_segment`，用于 emlet 字幕二次分句。
- 默认每句最多 `12` 个字符，按强标点、弱标点、连接词和长度切分。
- 新增 `protected_terms` 和 `protected_terms_path`，用于保护品牌词、产品名、人名、术语不被拆开。
- `pipeline` 支持 `subtitle -> caption_segment` 串联；分句步骤未传 `caption_path` 时会自动使用上一步字幕 JSON。

## 4.2.0 更新

- 新增 HTTP 异步长任务接口 `/skill/jobs`，适合压缩、ASR/OCR、字幕和 pipeline 等耗时 action。
- 任务状态持久化到 `output/jobs/<job_id>/job.json`，支持提交、轮询和列表查询。
- 现有 `/skill/<action>` 同步接口保持不变；CLI 仍保持同步执行。

## 4.3.0 更新

- `chat` 增加 HTTP 异步闭环：`async=true` 会把识别出的 action 提交为 job。
- `async="auto"` 会自动将 `audio`、`compress`、`asr`、`ocr`、`subtitle`、`caption_segment`、`batch`、`pipeline` 作为异步长任务执行；`info`、`audio_info`、`thumbnail` 保持同步返回。
- job 快照新增 `created_by`、`intent`、`source`、`metadata`，方便 Claw 按聊天上下文展示结果。
- HTTP 服务启动时会清理过旧终态 job，默认保留 7 天且最多 200 条。

## 4.3.1 更新

- 修正 HTTP chat 短等待行为：job 在 `wait_timeout_sec` 内完成时返回 `200` 和最终结果；仍在排队或运行时返回 `202`。
- `/skill/jobs` 严格要求 `params` 为 JSON object；缺省或 `null` 使用 `{}`，数组、字符串等返回 `invalid_params`。
- `async` 仅接受 JSON boolean 或 `"auto"`；`wait_timeout_sec` 必须是 `0-30` 秒数字。
- 异步结果中的 `output_paths` 会按首次出现顺序去重。

### 自然语言调用

Action: `chat`

Claw 推荐优先调用 `chat`。普通短命令可同步调用；压缩、字幕、pipeline 等长任务推荐 HTTP 调用时传入 `async:"auto"`。复杂、确定性要求高的多步骤流程继续使用 `pipeline`。

```bash
python run.py -a chat -i '{"message":"将 \"sample.mp4\" 提取音频"}'
python run.py -a chat -i '{"message":"给 \"sample.mp4\" 提取第 3 秒封面"}'
python run.py -a chat -i '{"message":"压缩 \"sample.mp4\""}'
python run.py -a chat -i '{"message":"查看 \"sample.mp4\" 信息"}'
python run.py -a chat -i '{"message":"识别 \"sample.mp4\" 的字幕"}'
```

HTTP / Claw 长任务推荐：

```bash
curl -X POST http://127.0.0.1:8080/skill/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"识别 \"sample.mp4\" 的字幕","async":"auto"}'
```

返回会包含 `job_id`、`poll_url`、`job_path`，随后轮询 `poll_url` 获取 `reply`、`result` 和 `output_paths`。如需全部自然语言命令都进入 job，可传 `async:true`；如需短等待，可传 `wait_timeout_sec`。排队或运行中的异步响应返回 HTTP `202`，短等待内已完成的异步响应返回 HTTP `200`。

处理绝对路径时需要配置媒体根目录：

```bash
python run.py -a chat -i '{"message":"将 \"D:/AA.MP4\" 提取音频","media_roots":["D:/"]}'
```

返回包含：

| 字段 | 说明 |
|------|------|
| `reply` | 可直接展示给用户的聊天回复 |
| `intent` | 识别出的意图 |
| `action` | 实际调用的 action |
| `params` | 传给底层 action 的参数 |
| `result` | 底层 action 原始结果 |
| `output_paths` | 本次生成的输出路径列表 |
| `job_id` | 异步提交时的任务 id |
| `poll_url` | 异步提交后的轮询地址 |

### HTTP 异步长任务

Action 可以继续同步调用，也可以通过 job API 异步执行。推荐对 `compress`、`asr`、`ocr`、`subtitle`、`pipeline` 等长任务使用异步接口。

提交任务：

```bash
curl -X POST http://127.0.0.1:8080/skill/jobs \
  -H 'Content-Type: application/json' \
  -d '{"action":"pipeline","params":{"source":"sample.mp4","steps":[{"id":"metadata","action":"info","enabled":true}]}}'
```

`params` 必须是 JSON object；不传或传 `null` 时按 `{}` 处理。

返回：

```json
{
  "status": "queued",
  "code": "ok",
  "reply": "任务已提交：<job_id>",
  "job_id": "<job_id>",
  "job_path": "output/jobs/<job_id>/job.json",
  "poll_url": "/skill/jobs/<job_id>"
}
```

轮询任务：

```bash
curl http://127.0.0.1:8080/skill/jobs/<job_id>
```

任务状态包括：`queued`、`running`、`success`、`partial`、`skipped`、`error`。任务结果保存在 `result`，产物路径汇总在 `output_paths`。

查询任务列表：

```bash
curl 'http://127.0.0.1:8080/skill/jobs?status=success&limit=50'
```

任务文件存储在 `output/jobs/<job_id>/job.json`。服务重启后，已完成任务仍可查询；未完成的 `queued` / `running` 任务会标记为 `error`，`code=job_interrupted`。

### 字幕识别

Action: `subtitle`

推荐使用 `subtitle`，默认 `mode=fusion`：ASR 负责主要时间轴和文本，OCR 做画面字幕校正。识别依赖随 `requirements.txt` 安装；如果环境未重新安装依赖，会返回 JSON error，不会抛未捕获异常。

```bash
python run.py -a subtitle -i '{"source":"sample.mp4","mode":"fusion"}'
python run.py -a subtitle -i '{"source":"sample.mp4","mode":"asr","language":"zh"}'
python run.py -a subtitle -i '{"source":"sample.mp4","mode":"ocr","sample_interval_sec":1}'
```

参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video_url` / `url` / `source` | string | 必填 | 远程 URL 或本地文件 |
| `mode` | string | fusion | `asr` / `ocr` / `fusion` |
| `language` | string | auto | ASR 语言，例：`zh` / `en` |
| `model_size` | string | base | faster-whisper 模型规格 |
| `sample_interval_sec` | number | 1.0 | OCR 抽帧间隔 |
| `crop_bottom_ratio` | number | 0.35 | OCR 默认扫描画面下方比例 |
| `output_path` | string | `output/subtitles/...` | 字幕 JSON 输出路径 |
| `overwrite` | boolean | true | 是否覆盖已有文件 |

字幕条目格式：

```json
{
  "captionTxt": "识别到的字幕文本",
  "startTimeUs": 1000000,
  "endTimeUs": 2000000,
  "source": "asr",
  "confidence": 0.92
}
```

底层调试入口：

```bash
python run.py -a asr -i '{"source":"sample.mp4","language":"zh"}'
python run.py -a ocr -i '{"source":"sample.mp4"}'
```

### 字幕二次分句

Action: `caption_segment`

`caption_segment` 是 emlet 字幕分句器：它不重新识别字幕，只处理已有 captions。默认 `max_chars=12`，输出仍是 SRT-like captions JSON。

```bash
python run.py -a caption_segment -i '{
  "caption_path":"output/subtitles/sample.captions.json",
  "max_chars":12,
  "protected_terms":["苹果","华为","吉利"]
}'
```

也可以直接传 captions：

```bash
python run.py -a caption_segment -i '{
  "captions":[
    {"captionTxt":"今天我们聊苹果华为和吉利的新产品","startTimeUs":0,"endTimeUs":3000000}
  ],
  "max_chars":12,
  "protected_terms":"苹果,华为,吉利"
}'
```

长期词库可以放在 JSON 文件中：

```json
{
  "brands": ["苹果", "华为", "吉利"],
  "products": ["小米汽车", "Model Y", "ChatGPT"]
}
```

参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `caption_path` / `input_path` | string | - | 已有 captions JSON 文件 |
| `captions` | array | - | 直接传入字幕条目 |
| `max_chars` | integer | 12 | 单条字幕最大字符数 |
| `protected_terms` | array/string | [] | 不拆开的品牌词、产品名、人名、术语 |
| `protected_terms_path` | string | - | 当前工作目录内的保护词 JSON 文件 |
| `auto_protect_ascii` | boolean | true | 自动保护英文、数字、型号、URL、路径 |
| `output_path` | string | `output/subtitles/...` | 分句后字幕 JSON 输出路径 |
| `overwrite` | boolean | true | 是否覆盖已有文件 |

### 压缩视频

Action: `compress`

```bash
python run.py -a compress -i '{"source":"sample.mp4","target_ratio":0.1}'
```

参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video_url` / `url` / `source` | string | 必填 | 远程 URL 或本地文件 |
| `target_ratio` | number | 0.1 | 目标体积比例 |
| `adaptive` | boolean | true | 是否自动尝试不同 CRF |
| `crf` | integer | 24 | 非 adaptive 模式下使用 |
| `preset` | string | veryfast | ffmpeg 编码预设 |
| `output_path` | string | `output/videos/...` | 输出路径 |
| `overwrite` | boolean | true | 是否覆盖已有文件 |

### 提取封面

Action: `thumbnail`

当前支持 MP4/MOV 容器，主要适用于 H.264/H.265 视频轨道。

```bash
python run.py -a thumbnail -i '{"source":"sample.mp4","time_seconds":5}'
```

参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video_url` / `url` / `source` | string | 必填 | 远程 URL 或本地文件 |
| `time_seconds` | number | 0 | 按时间点提取 |
| `frame_number` | integer | - | 按帧号提取，优先于 `time_seconds` |
| `save_path` | string | `output/thumbs/...` | 保存路径 |
| `resize_width` | integer | - | 输出宽度 |
| `quality` | integer | 85 | JPEG 质量 |
| `overwrite` | boolean | true | 是否覆盖已有文件 |

### 提取音频

Action: `audio`

```bash
python run.py -a audio -i '{"source":"sample.mp4","format":"mp3"}'
```

参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video_url` / `url` / `source` | string | 必填 | 远程 URL 或本地文件 |
| `format` | string | mp3 | mp3 / wav / aac / m4a |
| `bitrate` | string | 128k | 音频比特率 |
| `sample_rate` | integer | 44100 | 采样率 |
| `channels` | integer | 2 | 声道数 |
| `start_time` | number | - | 开始时间，秒 |
| `duration` | number | - | 截取时长，秒 |
| `output_path` | string | `output/audio/...` | 输出路径 |
| `overwrite` | boolean | true | 是否覆盖已有文件 |

### 批量音频

Action: `audio_batch`

```bash
python run.py -a audio_batch -i '{
  "videos":[
    {"source":"sample1.mp4","name":"video1"},
    {"url":"https://example.com/2.mp4","name":"video2"}
  ],
  "output_dir":"output/audio",
  "format":"mp3"
}'
```

### 批量处理

Action: `batch`

```bash
python run.py -a batch -i '{
  "action":"thumbnail",
  "videos":[
    {"source":"sample1.mp4","time_seconds":5},
    {"url":"https://example.com/2.mp4","time_seconds":10}
  ]
}'
```

`action` 支持：`compress`、`thumbnail`、`audio`。

### JSON 流水线

Action: `pipeline`

`steps` 是唯一流程控制入口，没有写进 `steps` 的动作不会执行。支持的 step action：`info`、`thumbnail`、`audio`、`compress`、`audio_info`、`asr`、`ocr`、`subtitle`、`caption_segment`。

```bash
python run.py -a pipeline -i '{
  "source":"sample.mp4",
  "name":"sample",
  "output_dir":"output/pipeline/sample",
  "overwrite":true,
  "steps":[
    {"id":"metadata","action":"info","enabled":true},
    {
      "id":"cover",
      "action":"thumbnail",
      "enabled":true,
      "params":{"time_seconds":3,"resize_width":720}
    },
    {
      "id":"audio_mp3",
      "action":"audio",
      "enabled":false,
      "params":{"format":"mp3","bitrate":"128k"}
    }
  ]
}'
```

规则：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video_url` / `url` / `source` | string | 必填 | 远程 URL 或本地文件 |
| `name` | string | 输入文件名 | 流水线名称 |
| `output_dir` | string | `output/pipeline/<name>` | manifest 和默认产物目录 |
| `overwrite` | boolean | true | 是否覆盖已有产物 |
| `steps` | array | 必填 | 按 JSON 顺序执行的步骤 |

每个 step 需要 `id`、`action`、`enabled`。`enabled=false` 会记录为 `skipped`。每次执行都会生成 `manifest.json`。

### 获取信息

```bash
python run.py -a info -i '{"source":"sample.mp4"}'
python run.py -a audio_info -i '{"source":"sample.mp4"}'
```

## 注意

- 远程输入仅支持 `http` / `https`。
- 本地输入路径默认限制在当前工作目录内；通过 `media_roots` / `YM_MEDIA_ROOTS` 可授权额外媒体根目录。
- 输出路径限制在当前工作目录内。
- HTTP 服务默认只绑定本机地址。
