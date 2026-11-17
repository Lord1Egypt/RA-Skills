# 视频生成与轮询

## 创建任务

- 文生视频：`POST /api/v1/spark-media/video`
- 图生视频：`POST /api/v1/spark-media/video/image`

JSON 参数：

| 字段 | 约束 |
|---|---|
| `prompt` | 必填，最多 8000 字符 |
| `duration` | 可选，`5` 或 `10` 秒 |
| `resolution` | 可选；当前 Seedance 2.0 Fast/Mini 仅 `480p`、`720p`；支持的其他模型可选 `1080p`，以平台 OpenAPI 为准 |
| `ratio` | 可选，`16:9`、`9:16` 或 `1:1` |
| `watermark` | 可选，布尔值 |
| `image` / `images` | 仅图生视频必填其一，且互斥；`image` 为兼容单图，`images` 为 1–9 张有序 PNG/JPEG/WebP `data:` URL 数组 |

每张解码后最大 5 MB（5242880 bytes）、16777216 像素，总计最大 20 MB（20971520 bytes）。单图沿用视频首帧行为；多图使用模型原生参考图能力，共同生成同一段视频，可用“图 1 人物、图 2 商品、图 3 背景”说明用途。多图参考不代表首尾帧模式，也不逐张生成视频。当前视频模型未确认支持多图参考时，平台返回 422，不创建任务或扣费。

视频按现有 token 用量规则结算，多图可能影响实际用量。重试必须使用原幂等键并保持图片内容、顺序及参数一致；更换或重排图片属于不同输入。

两个创建接口都要求 `Idempotency-Key`，成功返回 HTTP 202、`task_id` 和初始 `status`。
平台同一用户同一时刻只允许一个活跃视频任务；HTTP 409
`video_task_in_progress`（视频任务处理中）表示应继续查询已有任务，不要创建并行任务。

## 查询任务

`GET /api/v1/spark-media/video/{task_id}`

每 5–10 秒轮询一次并限制总时长。`pending`（等待中）、`submitted`（已提交）、`queued`（已排队）、`running`（运行中）等状态
视为进行中；`succeeded`（成功）为成功；`failed`（失败）、`error`、`cancelled`（已取消）、`canceled`（已取消）为终态失败。
成功后读取响应中的 `video_url` 或 `result` 并立即保存需要的内容。

`refunded: true` 表示失败任务的本次费用已退回。不要仅凭失败文本自行宣称退款；以该字段
及账单记录为准。失败状态不能当作可无限重试的理由，新任务必须由用户意图或明确恢复策略
驱动。


## 上游协议依据

火山方舟 [Seedance 2.0 系列教程](https://docs.volcengine.com/docs/ark/seedance-2-0?lang=zh) 确认 Fast 模型支持图片参考；[创建视频生成任务 API](https://docs.volcengine.com/docs/ark/create-video-generation-task-api?lang=zh) 规定该系列最多 9 张参考图，各图共同作为参考素材。调用方仍只发送本页的平台参数，由平台负责适配上游协议。上游图片还需满足宽高 300–6000 像素及宽高比 0.4–2.5；实际模型对输入的完整校验仍由上游执行。

5 MB 单张及 20 MB 总量是平台限制，9 张图片也必须满足此总量；不会按参考图数量拆分任务。
