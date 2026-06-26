---
name: human-pip
description: "提交异步人物抠像画中画任务（人像前景 + 背景图/视频）并轮询结果，自动生成可继续编辑草稿。用户提到“人物抠像”“画中画口播”“带货视频人物叠加”“主播叠加 broll 丰富画面”“把人像放到角落讲解”时必须使用本技能；背景素材不足时优先联动 generate-ai-image 或 generate-ai-video。若用户提供图片/视频 b-roll 素材，必须先用 add_image/add_video 按时间窗对齐写回草稿，再执行 human-pip。"
---

# Human PIP Skill

用于调用 VectCut 人物抠像画中画异步接口，把人物从原视频中抠出并叠加到背景素材（图片或视频）中，常用于带货口播、知识讲解、解说类视频的画面丰富化。

接口依据：(https://docs.vectcut.com/444064295e0)

## 何时使用

- 用户要求“人物抠像 + 画中画”
- 用户要把口播人物叠加到 broll/背景图上
- 用户已有人像视频，但需要更丰富背景或动态背景
- 用户要把画中画插入到已有草稿某时间点

## 鉴权前置（必须）

- 先检查 `VECTCUT_API_KEY`
- 缺失或疑似失效时，先调用 `vectcut-login`

## 输入要求

- 必填：
  - `video_url`：人物视频 URL（建议 <= 120 秒）
  - `template`：画中画模板
- 背景二选一（必须且只能传一个）：
  - `background_image_url`
  - `background_video_url`
- 常用可选：
  - `draft_id`、`target_start`、`speed`
  - `background_volume`（背景视频静音可传 `-100`）

模板枚举：
- `left_down`
- `left_up`
- `right_up`
- `right_down`
- `fixed_left_down`
- `fixed_left_up`
- `fixed_right_up`
- `fixed_right_down`

## 背景素材联动策略

- 没有背景图：先调用 `generate-ai-image` 生成 `background_image_url`
- 没有背景视频：先调用 `generate-ai-video` 生成 `background_video_url`
- 若用户已有真实素材 URL，直接使用即可
- 若用户提供 b-roll 素材（图片或视频），优先使用这些素材，不要默认退回主口播视频充当背景

## B-roll 入草稿约束（必须）

- 图片 b-roll：先调用 `add_image` 写回草稿
  - `start` / `end` 必须与 `human-pip` 的开始/结束时间一致
  - 推荐写入 `track_name=video_main`，并保证该段与人像画中画同窗对齐
- 视频 b-roll：先调用 `add_video` 写回草稿
  - `start` / `end` 表示从原 b-roll 视频截取的片段区间
  - 截取时长必须等于 `human-pip` 持续时长
  - `target_start` 必须等于 `human-pip` 的开始时间
  - `volume=-100`（背景静音）
- 若 b-roll 不足以覆盖 `human-pip` 时间窗，再联动 `generate-ai-image` 或 `generate-ai-video` 补足

## 执行方式


```json
{
  "video_url": "https://player.install-ai-guider.top/example/example_pip.mp4",
  "background_video_url": "https://player.install-ai-guider.top/example/broll_real_2.mp4",
  "template": "right_down",
  "target_start": 4,
  "speed": 1.0,
  "background_volume": -100
}
```

执行：

```bash
python <skill-path>/scripts/human_pip_async.py \
  "/tmp/human_pip_payload.json" \
  --output "./human_pip_result.json"
```

可选参数：
- `--poll-interval`：轮询间隔，默认 `2.0`
- `--timeout`：超时秒数，默认 `900`
- `--status-path`：任务状态接口路径，默认 `/process/remove_bg/submit_task/task_status`

## 输出结果

默认输出 `human_pip_result.json`，核心字段：
- `meta.task_id`
- `meta.final_status`
- `result.draft_id`
- `result.draft_url`
- `result.video_url`
- `result.raw_result`

## 与 asr-vad 的衔接建议

- 在 `asr-vad` 清洗字幕后，优先挑选“产品展示/卖点解释/对比说明”片段插入画中画
- 按建议片段的 `target_start` 逐段调用本技能，形成“主讲 + broll”节奏
- 执行后可用 `query-draft` 检查是否与字幕节奏对齐
