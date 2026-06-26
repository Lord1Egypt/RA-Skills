---
name: split-video
description: "提交异步视频分割任务并轮询结果，按时间区间从原视频截取片段并返回可访问片段 URL。用户提到“截取视频片段”“先切一段再处理”“只处理某个时间区间”“给 human-pip 或 text-background 提前裁片”时必须使用本技能。"
---

# Split Video Skill

用于调用 VectCut 分割视频异步接口，先从长视频裁出目标片段，再把片段 URL 交给后续技能处理。

这通常是 `human-pip`、`text-background` 的前置步骤，因为这两个技能只需要目标片段，不需要整段原视频。

## 接口依据

- 官方文档：https://docs.vectcut.com/444634731e0
- 提交任务：`/process/split_video/submit_task/submit_split_video_task`
- 查询状态：`/process/split_video/submit_task/task_status`

## 何时使用

- 用户要“截取某段视频”或“按时间区间切片”
- 用户说先做片段预处理，再做抠像/字在人后
- 用户只想处理长视频中的重点片段
- 用户需要批量提交切片任务（异步）

## 鉴权前置（必须）

- 检查 `VECTCUT_API_KEY`
- 缺失或疑似失效时，先调用 `vectcut-login`

## 输入要求

- 必填：
  - `video_url`：待切割视频 URL
  - `start`：开始时间（支持秒数或 `HH:MM:SS(.ms)`）
  - `end`：结束时间（支持秒数或 `HH:MM:SS(.ms)`，且必须大于 `start`）

## 执行方式

先准备请求 JSON，例如：

```json
{
  "video_url": "https://player.install-ai-guider.top/example/koubo_source.mp4",
  "start": "00:00:03.200",
  "end": "00:00:05.100"
}
```

执行：

```bash
python <skill-path>/scripts/split_video_async.py \
  "/tmp/split_video_payload.json" \
  --output "./split_video_result.json"
```

可选参数：
- `--poll-interval`：轮询间隔秒数，默认 `2.0`
- `--timeout`：轮询超时秒数，默认 `600`
- `--status-path`：任务状态接口路径，默认 `/process/split_video/submit_task/task_status`

## 处理流程

1. `POST /process/split_video/submit_task/submit_split_video_task` 提交任务，得到 `task_id`
2. `GET /process/split_video/submit_task/task_status?task_id=...` 轮询任务状态
3. 状态为 `success` 后读取 `result.public_url`
4. 把 `public_url` 作为后续技能输入（如 `human-pip`、`text-background`）

## 输出结果

默认输出 `split_video_result.json`，核心字段：
- `meta.task_id`
- `meta.final_status`
- `clip.public_url`
- `clip.start`
- `clip.end`
- `clip.raw_result`

## 与其他技能的推荐串联

- 场景 1：先 `split-video`，再 `human-pip`
  - 对一个长口播视频先截出 5~12 秒卖点片段
  - 将 `clip.public_url` 传给 `human-pip.video_url`
- 场景 2：先 `split-video`，再 `text-background`
  - 先截出重点句时间段，减少不必要处理时长
  - 将 `clip.public_url` 传给 `text-background.video_url`

## 失败处理建议

- `400` 参数错误：检查 `video_url/start/end` 格式与逻辑
- `404` 任务不存在或过期：重新提交任务
- 轮询超时：延长 `--timeout` 并检查源视频可访问性
