---
name: voscript-api
description: |
  VoScript self-hosted speech transcription API skill. Covers the full workflow:
  submit audio, poll job status, fetch results, export subtitles (SRT/TXT/JSON),
  manage voiceprints, assign speakers, and rebuild AS-norm cohorts.
  Works with Claude Code, OpenClaw, Hermes, Codex, Gemini CLI, Trae, Cursor,
  Cline, Roo Code, CodeBuddy, Qwen Code, and any agent with a skills directory.
license: SEE LICENSE IN LICENSE
metadata:
  author: MapleEve
  version: 1.1.1
  homepage: https://github.com/MapleEve/voscript-skills
  tags:
    - transcription
    - speech-to-text
    - voiceprint
    - audio
    - subtitles
    - self-hosted
    - voscript
  category: productivity
  platforms:
    - macOS
    - Linux
    - Windows
  compatibility:
    env:
      - VOSCRIPT_URL
      - VOSCRIPT_API_KEY
  triggers:
    - voscript
    - VoScript
    - voscript api
    - 提交转写
    - submit transcription
    - 上传音频
    - 查询任务
    - poll job
    - job status
    - 转写结果
    - get transcript
    - transcription result
    - 导出字幕
    - export transcript
    - export srt
    - 注册声纹
    - enroll voiceprint
    - speaker enrollment
    - 声纹列表
    - list speakers
    - voiceprint list
    - 分配说话人
    - assign speaker
    - 重建声纹库
    - rebuild cohort
---

# VoScript API 技能包

VoScript 是一个自托管的语音转写服务，支持多说话人分离、声纹识别、降噪、
多格式导出。本技能包封装了其 REST API 的全部主要工作流。

> 重要：本技能与代理无关（agent-agnostic），同等适用于 Claude、Codex、
> Trae、Hermes、OpenClaw 等任何 AI 代理，不依赖任何厂商专属特性。

## 1. 配置说明

VoScript 通过两个参数进行访问配置：

- `VOSCRIPT_URL`：服务地址，例如 `http://localhost:7880`
- `VOSCRIPT_API_KEY`：调用 API 所需的鉴权密钥

推荐通过环境变量设置，所有脚本也支持 `--url` / `--api-key` 命令行参数覆盖。

**当 `VOSCRIPT_URL` 或 `VOSCRIPT_API_KEY` 未配置时，代理必须：**

1. 先向用户索要服务地址与 API Key；
2. 告知用户配置方式：
   - 环境变量：`export VOSCRIPT_URL=...` / `export VOSCRIPT_API_KEY=...`
   - 或使用脚本的 `--url <URL>` / `--api-key <KEY>` 参数。

详见 `${SKILL_PATH}/references/configuration.md`。

## 2. 提交音频转写

上传音频文件并创建转写任务。

**接口：** `POST /api/transcribe`（`multipart/form-data`）

**请求参数：**

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `file` | file | 是 | — | 待转写音频文件 |
| `language` | string | 否 | 自动 | 语言代码，如 `zh` / `en` |
| `min_speakers` | int | 否 | `1` | 最少说话人数 |
| `max_speakers` | int | 否 | `10` | 最多说话人数 |
| `denoise_model` | string | 否 | `none` | 可选 `none` / `deepfilternet` / `noisereduce` |
| `snr_threshold` | float | 否 | `10.0` | 信噪比阈值 |
| `no_repeat_ngram_size` | int | 否 | `0` | 解码时抑制 n-gram 重复 |

```bash
curl -X POST "$VOSCRIPT_URL/api/transcribe" \
  -H "X-API-Key: $VOSCRIPT_API_KEY" \
  -F "file=@/path/to/audio.wav" \
  -F "language=zh" \
  -F "min_speakers=1" \
  -F "max_speakers=10"
```

**响应字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 任务 / 转写 ID（形如 `tr_xxx`），后续接口均以此为主键 |
| `status` | string | 初始状态，一般为 `queued`；若命中去重则为 `completed` |
| `deduplicated` | bool | 可选字段，出现且为 `true` 表示命中 SHA-256 去重，直接返回既有结果 |

> ❗ `deduplicated: true` 不是错误，是正常响应。VoScript 对音频内容计算 SHA-256，
> 若已处理过相同文件，直接返回已有结果。此时 `status` 为 `"completed"`，
> 无需再次轮询，直接用返回的 `id` 获取结果。

**错误响应表：**

| HTTP | 含义 | 排查 |
|------|------|------|
| 401 | API Key 无效 | 检查 VOSCRIPT_API_KEY 是否正确、有无多余空格 |
| 413 | 文件过大 | 超过服务端 MAX_UPLOAD_BYTES 限制（默认 2 GiB） |
| 422 | 参数校验失败 | 检查 min_speakers/max_speakers/denoise_model 值是否合法 |
| 500 | 服务端错误 | 查看容器日志 `docker logs voscript` |

执行脚本：

```bash
python ${SKILL_PATH}/scripts/submit_audio.py \
  --file <PATH> \
  [--language zh] \
  [--min-speakers 1] \
  [--max-speakers 10]
```

## 3. 轮询任务状态

**接口：** `GET /api/jobs/{job_id}`

```bash
curl -X GET "$VOSCRIPT_URL/api/jobs/tr_xxx" \
  -H "X-API-Key: $VOSCRIPT_API_KEY"
```

**状态机：** `queued → converting → denoising → transcribing → identifying → completed | failed`

**状态含义与典型耗时：**

| 状态 | 含义 | 典型耗时 |
|------|------|---------|
| queued | 等待 GPU 资源 | 即时～数秒 |
| converting | ffmpeg 格式转换 | 数秒 |
| denoising | DeepFilterNet 降噪 | 10-30 秒（可选步骤） |
| transcribing | Whisper + pyannote 转写 | 音频时长的 20-50% |
| identifying | 声纹匹配 | 数秒 |
| completed | 完成 | — |
| failed | 失败 | 查看 error 字段 |

> ⚠️ 轮询建议间隔 5 秒，首次加载模型需 2-5 分钟（仅首次），
> 轮询超时不代表失败，可继续等待或检查 `/healthz`。

**常见错误：**

| HTTP | 含义 | 排查 |
|------|------|------|
| 401 | API Key 无效 | 检查 `VOSCRIPT_API_KEY` |
| 404 | job_id 不存在 | 确认 ID 拼写，或任务可能已被清理 |

执行脚本：

```bash
python ${SKILL_PATH}/scripts/poll_job.py --job-id tr_xxx
```

详细状态机与阶段耗时：`${SKILL_PATH}/references/job-lifecycle.md`

## 4. 获取转写结果

**接口：** `GET /api/transcriptions/{tr_id}`

```bash
curl -X GET "$VOSCRIPT_URL/api/transcriptions/tr_xxx" \
  -H "X-API-Key: $VOSCRIPT_API_KEY"
```

返回内容包括：`segments`、`speaker_map`、`params` 等完整结果。

**Segment 字段表：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 片段序号 |
| `start` / `end` | float | 起止时间（秒） |
| `text` | string | 转写文本 |
| `speaker_label` | string | pyannote 原始标签（如 `SPEAKER_00`），注册声纹时使用此值 |
| `speaker_id` | string\|null | 已绑定的声纹 ID，null 表示未注册 |
| `speaker_name` | string | 显示名（已注册则为姓名，否则同 speaker_label） |
| `similarity` | float\|int | **AS-norm z-score，非概率**，典型范围 -1 到 2，匹配阈值 ~0.5 |
| `words` | array\|null | 词级对齐（强制对齐成功时存在） |

> ❗ `similarity` 是 AS-norm 归一化的 z-score，**不是 [0,1] 之间的概率**。
> 值可能超过 1.0（最高观测值约 1.79）。若用 `similarity > 0.5` 判断是否匹配，
> 这是合理的经验值，但不能理解为"50% 置信度"。

**常见错误：**

| HTTP | 含义 | 排查 |
|------|------|------|
| 404 | tr_id 不存在 | 核对 ID；确认任务已 `completed` |
| 409 | 任务尚未完成 | 先通过 `/api/jobs/{id}` 轮询到 `completed` |

执行脚本：

```bash
python ${SKILL_PATH}/scripts/fetch_result.py --tr-id tr_xxx
```

## 5. 导出转写

**接口：** `GET /api/export/{tr_id}?format=srt|txt|json`

```bash
curl -X GET "$VOSCRIPT_URL/api/export/tr_xxx?format=srt" \
  -H "X-API-Key: $VOSCRIPT_API_KEY" \
  -o transcript.srt
```

**支持格式：**

| format | 用途 | MIME |
|--------|------|------|
| `srt` | 标准字幕文件，带时间轴 | `application/x-subrip` |
| `txt` | 带说话人前缀的纯文本 | `text/plain` |
| `json` | 完整结构化数据（segments + speaker_map） | `application/json` |

**常见错误：**

| HTTP | 含义 | 排查 |
|------|------|------|
| 404 | tr_id 不存在 | 核对 ID |
| 422 | format 参数非法 | 只能是 `srt` / `txt` / `json` |

格式细节：`${SKILL_PATH}/references/export-formats.md`

执行脚本：

```bash
python ${SKILL_PATH}/scripts/export_transcript.py --tr-id tr_xxx --format srt
```

## 6. 转写列表

**接口：** `GET /api/transcriptions`

```bash
curl -X GET "$VOSCRIPT_URL/api/transcriptions" \
  -H "X-API-Key: $VOSCRIPT_API_KEY"
```

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 转写 ID |
| `filename` | string | 原始文件名 |
| `created_at` | string | ISO 8601 创建时间 |
| `segment_count` | int | 片段数量 |
| `speaker_count` | int | 说话人数量 |

执行脚本：

```bash
python ${SKILL_PATH}/scripts/list_transcriptions.py
```

## 7. 注册声纹

从已有转写中抽取某个 `speaker_label` 对应片段作为样本，注册或更新声纹。

**接口：** `POST /api/voiceprints/enroll`

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tr_id` | string | 是 | 来源转写 ID |
| `speaker_label` | string | 是 | **pyannote 原始标签**，如 `SPEAKER_00`（不是显示名！） |
| `speaker_name` | string | 是 | 说话人姓名（显示用） |
| `speaker_id` | string | 否 | 传入已有声纹 ID 则更新该声纹 |

```bash
curl -X POST "$VOSCRIPT_URL/api/voiceprints/enroll" \
  -H "X-API-Key: $VOSCRIPT_API_KEY" \
  -F "tr_id=tr_xxx" \
  -F "speaker_label=SPEAKER_00" \
  -F "speaker_name=张三"
```

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `action` | string | `created`（新建）或 `updated`（更新已有声纹） |
| `speaker_id` | string | 声纹 ID，后续可用于绑定 |

> ❗ **最常见错误：`speaker_label` 填写了显示名而非原始标签**
>
> - ✗ 错误：`--speaker-label "张三"`
> - ✓ 正确：`--speaker-label "SPEAKER_00"`
>
> `speaker_label` 必须是 pyannote 的原始标签（`SPEAKER_00`, `SPEAKER_01` 等），
> 来自转写结果的 `segment.speaker_label` 字段。
>
> 注册成功后，后续转写中识别出的同一说话人会自动匹配到 `speaker_name`。

**错误响应表：**

| HTTP | 含义 | 排查 |
|------|------|------|
| 404 | Embedding not found for this speaker label | `speaker_label` 在该转写中不存在。检查大小写、确认使用的是 `SPEAKER_XX` 格式 |
| 422 | 参数缺失 | 确认 tr_id、speaker_label、speaker_name 均已提供 |
| 401 | API Key 无效 | 检查 `VOSCRIPT_API_KEY` |

执行脚本：

```bash
python ${SKILL_PATH}/scripts/enroll_voiceprint.py \
  --tr-id tr_xxx \
  --speaker-label SPEAKER_00 \
  --speaker-name "张三"
```

## 8. 声纹列表

**接口：** `GET /api/voiceprints`

```bash
curl -X GET "$VOSCRIPT_URL/api/voiceprints" \
  -H "X-API-Key: $VOSCRIPT_API_KEY"
```

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 声纹 ID |
| `name` | string | 显示姓名 |
| `sample_count` | int | 已累积的样本数量 |
| `sample_spread` | float\|null | 样本间余弦相似度的标准差；单样本时为 `null`；数值越小表示样本一致性越高 |
| `created_at` | string | ISO 8601 创建时间 |
| `updated_at` | string | ISO 8601 最后更新时间 |

> ⚠️ `sample_spread` 偏大（例如 > 0.3）说明样本之间差异大，可能混入了错误片段，
> 建议通过 `manage_voiceprint.py --action get` 查看详情并考虑清理。

执行脚本：

```bash
python ${SKILL_PATH}/scripts/list_voiceprints.py
```

## 9. 分配说话人

手动为某个 segment 指定说话人（用于纠正分离错误或补齐未识别片段）。

**接口：** `PUT /api/transcriptions/{tr_id}/segments/{seg_id}/speaker`

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `speaker_name` | string | 是 | 新的说话人显示名 |
| `speaker_id` | string | 否 | 若要绑定已注册声纹，传入声纹 ID |

```bash
curl -X PUT "$VOSCRIPT_URL/api/transcriptions/tr_xxx/segments/5/speaker" \
  -H "X-API-Key: $VOSCRIPT_API_KEY" \
  -F "speaker_name=李四"
```

> 💡 当你发现某个片段的说话人识别有误，或想手动覆盖自动识别结果时使用。
> 手动分配不影响声纹库，仅修改该片段的显示名。

**常见错误：**

| HTTP | 含义 | 排查 |
|------|------|------|
| 404 | tr_id 或 seg_id 不存在 | 核对 ID；seg_id 为 segment 在该转写中的序号 |
| 422 | 参数缺失 | 至少提供 `speaker_name` |

执行脚本：

```bash
python ${SKILL_PATH}/scripts/assign_speaker.py \
  --tr-id tr_xxx \
  --seg-id 5 \
  --speaker-name "李四"
```

## 10. 管理声纹

| 操作 | 端点 | 参数 |
|------|------|------|
| 查看详情 | `GET /api/voiceprints/{speaker_id}` | — |
| 重命名 | `PUT /api/voiceprints/{speaker_id}/name` | 表单字段 `name` |
| 删除 | `DELETE /api/voiceprints/{speaker_id}` | — |

```bash
curl -X GET "$VOSCRIPT_URL/api/voiceprints/<SPEAKER_ID>" \
  -H "X-API-Key: $VOSCRIPT_API_KEY"
```

**常见错误：**

| HTTP | 含义 | 排查 |
|------|------|------|
| 404 | speaker_id 不存在 | 通过 `/api/voiceprints` 确认 ID |
| 422 | 重命名时缺少 `name` 字段 | 提供表单字段 `name` |

执行脚本：

```bash
python ${SKILL_PATH}/scripts/manage_voiceprint.py \
  --action [get|rename|delete] \
  --speaker-id xxx \
  [--name "新名字"]
```

## 11. 重建声纹 cohort

AS-norm 评分依赖 cohort（对比样本集）。

**接口：** `POST /api/voiceprints/rebuild-cohort`

```bash
curl -X POST "$VOSCRIPT_URL/api/voiceprints/rebuild-cohort" \
  -H "X-API-Key: $VOSCRIPT_API_KEY"
```

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `cohort_size` | int | 重建后 cohort 内样本数量 |
| `skipped` | int | 被跳过的样本数（质量不达标或重复） |
| `saved_to` | string | cohort 文件保存路径 |

> 💡 **何时执行重建：**
> - 注册满 10 个说话人后首次执行
> - 每新增 10-20 个说话人后更新一次
> - cohort 大小 ≥ 50 时 AS-norm 评分最为稳定
>
> 重建前无需停止服务，操作为后台非阻塞任务。

执行脚本：

```bash
python ${SKILL_PATH}/scripts/rebuild_cohort.py
```

声纹完整工作流与阈值说明见 `${SKILL_PATH}/references/voiceprint-guide.md`。

## 错误响应规范

VoScript 返回标准 HTTP 状态码，代理在处理响应时应按下表做分支：

| 状态码 | 含义                   | 处理建议                                         |
| ------ | ---------------------- | ------------------------------------------------ |
| 200    | 成功                   | 正常解析响应                                     |
| 401    | API Key 无效           | 提示用户检查 `VOSCRIPT_API_KEY`                  |
| 404    | 资源不存在             | 核对 `tr_id` / `speaker_id` / `job_id`           |
| 409    | 资源状态冲突           | 例如任务尚未 completed 就请求结果                |
| 413    | 文件过大               | 检查服务端 `MAX_UPLOAD_BYTES`（默认 2 GiB）       |
| 422    | 请求参数校验失败       | 根据返回 `detail` 字段检查参数，常见于缺少 `file` |
| 500    | 服务端错误             | 收集 `error` 字段，必要时检查服务端日志          |

## 诊断检查清单

遇到问题时，按以下顺序排查：

1. **服务可达性**：`curl $VOSCRIPT_URL/healthz` 是否 200
2. **鉴权**：`X-API-Key` 是否与容器环境变量 `VOSCRIPT_API_KEY` 一致，有无多余空格
3. **任务状态**：先通过 `/api/jobs/{id}` 确认 `completed`，再拉结果
4. **声纹标签**：注册声纹时使用 `SPEAKER_XX` 原始标签，不是显示名
5. **similarity 语义**：不是概率，是 AS-norm z-score，阈值 ~0.5 为经验值
6. **去重响应**：`deduplicated: true` 是正常返回，不是错误
7. **首次冷启动**：模型加载耗时 2-5 分钟，轮询超时不等于失败
8. **容器日志**：`docker logs voscript` 查看详细栈回溯

## 典型使用序列

1. 配置 `VOSCRIPT_URL` / `VOSCRIPT_API_KEY`。
2. `submit_audio.py` 上传音频，拿到 `tr_id`。
3. `poll_job.py` 轮询到 `completed`。
4. `fetch_result.py` 获取 segments，审阅 speaker 分离结果。
5. 对每个 `SPEAKER_xx` 调用 `enroll_voiceprint.py` 注册真实姓名。
6. 累计 10+ 声纹后运行 `rebuild_cohort.py` 刷新 AS-norm 基线。
7. 后续新音频转写会自动识别已注册说话人。
8. 需要字幕文件时使用 `export_transcript.py` 导出 SRT/TXT/JSON。

## 参考文档

- `${SKILL_PATH}/references/configuration.md` —— 配置与鉴权
- `${SKILL_PATH}/references/job-lifecycle.md` —— 任务状态机
- `${SKILL_PATH}/references/voiceprint-guide.md` —— 声纹与 AS-norm
- `${SKILL_PATH}/references/export-formats.md` —— 导出格式
