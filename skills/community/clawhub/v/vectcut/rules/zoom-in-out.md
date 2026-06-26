---
name: zoom-in-out
description: "对重点片段执行“开头缩放+结尾反向缩放”的强调动效。用户提到“突出重点”“强调某句/某个画面”“做放大缩小节奏”“zoom in/out”“镜头呼吸感”时必须使用本技能。"
---

# Zoom In Out Skill

用于给指定视频片段做“开头一组关键帧 + 结尾一组关键帧”的缩放强调效果。

固定流程：
1. 先调用 `split-video` 逻辑切出目标片段
2. 用 `add_video` 把切片加进草稿
3. 用 `add_video_keyframe` 添加两组间隔 `0.2s` 的关键帧
4. 用 `query-draft` 校验视频和关键帧是否写入草稿

官方接口文档：
- split-video 提交任务：https://docs.vectcut.com/444634731e0
- split-video 状态查询：https://docs.vectcut.com/444634732e0
- add_video：https://docs.vectcut.com/321243745e0
- add_video_keyframe：https://docs.vectcut.com/321244301e0
- query_script：https://docs.vectcut.com/386764616e0

## 何时使用

- 用户要“强调某段内容”
- 用户要“开头放大、结尾缩回”
- 用户要“开头缩小、结尾放大”
- 用户说“zoom in / zoom out / 缩放强调 / 镜头呼吸感”

## 鉴权前置（必须）

- 检查 `VECTCUT_API_KEY`
- 缺失或疑似失效时，先调用 `vectcut-login`

## 缩放规则（按你给的规范）

默认关键帧间隔 `0.2s`，缩放属性使用 `uniform_scale`。

- 模式 A：`in-out`（默认）
  - 片段开始：`start_time -> start_time + 0.2`
  - 值：`1.0 -> 1.1`（放大）
  - 片段结束：`end_time - 0.2 -> end_time`
  - 值：`1.1 -> 1.0`（缩小）

- 模式 B：`out-in`
  - 片段开始：`1.1 -> 1.0`（缩小）
  - 片段结束：`1.0 -> 1.1`（放大）

## 输入参数

- 必填：
  - `video_url`：原始视频 URL
  - `clip_start`：切片开始（秒或 `HH:MM:SS(.ms)`）
  - `clip_end`：切片结束（秒或 `HH:MM:SS(.ms)`）
- 可选：
  - `draft_id`：已有草稿 ID（不传则由 add_video 创建）
  - `target_start`：切片放入时间线的起点，默认 `0.0`
  - `track_name`：默认 `zoom_video`
  - `width`：默认 `1080`
  - `height`：默认 `1920`
  - `mode`：`in-out` 或 `out-in`，默认 `in-out`
  - `interval_seconds`：默认 `0.2`
  - `scale_normal`：默认 `1.0`
  - `scale_emphasis`：默认 `1.1`
  - `poll_interval`：split-video 轮询间隔，默认 `2.0`
  - `poll_timeout`：split-video 轮询超时，默认 `600`

## 执行方式

准备请求 JSON：

```json
{
  "video_url": "https://example.com/source.mp4",
  "clip_start": 5.0,
  "clip_end": 8.2,
  "target_start": 1.0,
  "mode": "in-out"
}
```

执行：

```bash
python <skill-path>/scripts/zoom_in_out.py \
  "/tmp/zoom_in_out_payload.json" \
  --output "./zoom_in_out_result.json"
```

## 输出结果

默认输出 `zoom_in_out_result.json`，核心字段：
- `split.clip_url`
- `add_video.draft_id`
- `keyframes.start_pair`
- `keyframes.end_pair`
- `verification.track_found`
- `verification.video_segment_count`

## 失败处理建议

- `clip_end <= clip_start`：修正切片区间
- 片段时长太短：保证 `clip_end - clip_start > 2 * interval_seconds`
- add_video 失败：检查 `video_url` 可访问性和 `draft_id`
- keyframe 失败：确认 `track_name` 与 add_video 使用一致
- 校验失败：开启 `query_script` 的 `force_update` 并重试
