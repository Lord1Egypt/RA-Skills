---
name: text-background
description: "提交异步“字在人后”任务（人物抠像+文字置于人物后方）并轮询完成，自动返回可编辑草稿。用户提到“字在人后”“文字在人物后面”“口播高级感字幕”“带货口播层次感”“人像前景+后方文字特效”时必须使用本技能。"
---

# Text Background Skill

用于调用 VectCut 的“字在人后”异步接口，把文字放在人物后方，形成明显的前后景层次，常用于口播剪辑、带货视频、知识讲解等场景。

官方接口文档：
- https://docs.vectcut.com/444268907e0

## 何时使用

- 用户明确要求“字在人后 / 文字在人后”
- 用户希望口播画面更有层次感、提升高级感
- 用户要做人像前景与文字背景分层效果
- 用户需要把该效果插入已有草稿的指定时间点

## 鉴权前置（必须）

- 检查 `VECTCUT_API_KEY` 是否存在且可用
- 缺失、为空或疑似失效时，先调用 `vectcut-login`

## 输入要求

- 必填：
  - `video_url`：人像视频 URL（建议 <= 120 秒）
  - `text`：要展示在人物后方的文案
- 常用可选：
  - `text_preset_id`：文字预设模板 ID（不传时默认 `fc6982de-c94e-447a-82d0-ab361cb27217`）
  - `draft_id`、`target_start`：插入已有草稿与落点时间（秒）
  - 轨道和层级控制：`track_name`、`relative_index`、`text_track_name`、`text_relative_index`
  - 底层视频控制：`base_video_track_name`、`base_video_relative_index`、`base_video_volume`
  - 音量：`volume`

官方示例模板（12 个，按字数匹配）：
- `9af810fd-87bf-467b-a555-7432608c3eff` 4字
- `26e31159-a4b0-4f10-804d-f74e10d3de96` 4字
- `360c97f1-4fa9-4482-9479-5acd7ad7c1f0` 4字
- `922145d1-8c60-4f4a-86c2-9146205c4ba6` 3字
- `a387a588-2ad0-4664-9411-fbe5a673fef9` 2字
- `21dc3080-b9ba-4654-a3c0-cfa6ac6348b5` 3字
- `ca710ef2-10f8-4c6a-98b4-92603c6dbacf` 3字
- `f0427d4d-d91e-4317-b437-6156fa26915a` 4字
- `02cd94b5-e03f-43a4-b201-22fc80ce3109` 4字
- `9d2b987d-ec4d-4cdc-b73c-c5c48034a4c4` 4字
- `8ed6367d-4d63-4cad-84a2-086ea5b12fe2` 3字
- `3b9b6e10-1be0-447c-a5af-5d39aec500a8` 3字

## 执行方式

先准备请求 JSON，例如：

```json
{
  "video_url": "https://player.install-ai-guider.top/example/pip_text_background.mp4",
  "text": "重启人生",
  "text_preset_id": "9af810fd-87bf-467b-a555-7432608c3eff",
  "target_start": 0
}
```

执行：

```bash
python <skill-path>/scripts/text_background_async.py \
  "/tmp/text_background_payload.json" \
  --output "./text_background_result.json"
```

可选参数：
- `--poll-interval`：轮询间隔秒数，默认 `2.0`
- `--timeout`：轮询超时秒数，默认 `900`
- `--status-path`：任务状态接口路径，默认 `/process/remove_bg/submit_task/task_status`

## 处理流程

1. `POST /process/remove_bg/submit_task/submit_remove_bg_text_behind_task` 提交任务，得到 `task_id`
2. `GET /process/remove_bg/submit_task/task_status?task_id=...` 轮询进度
3. 状态为 `success` 后读取结果中的 `draft_id / draft_url`
4. 输出标准化 JSON，供后续 `query-draft` 或 `cloud-render` 使用

## 输出结果

默认输出 `text_background_result.json`，核心字段：
- `meta.task_id`
- `meta.final_status`
- `result.draft_id`
- `result.draft_url`
- `result.mask_url`
- `result.inverted_mask_url`
- `result.raw_result`

## 失败处理建议

- `400` 参数错误：检查 `video_url/text/text_preset_id`
- `404` 任务不存在或过期：重新提交任务
- 轮询超时：延长 `--timeout`，并检查源视频可访问性
