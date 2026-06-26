---
name: generate-ai-video
description: "提交异步文生视频/图生视频任务并自动轮询结果，支持多模型（veo3.1、veo3.1-pro、seedance-1.5-pro、grok-video-3）与草稿衔接参数。用户提到“AI 生成视频”“文生视频”“图生视频”“首尾帧视频”“参考图生成视频”“生成 broll 背景视频”时必须使用本技能。"
---

# Generate AI Video Skill

用于调用 VectCut 视频生成聚合接口，发起异步任务并轮询结果，支持把生成结果直接用于后续剪辑（如 `human-pip` 的背景视频）。

接口依据：(https://docs.vectcut.com/403445863e0)

## 何时使用

- 用户要文生视频或图生视频
- 用户要指定模型、分辨率、时长、是否带音频
- 用户要生成 broll 再用于口播/带货画中画背景
- 用户要异步提交并拿 `video_url`、`draft_id`、`draft_url`

## 鉴权前置（必须）

- 先检查 `VECTCUT_API_KEY`
- 缺失或失效时，先调用 `vectcut-login`

## 模型能力规则

能力表统一维护在：
- `references/model_capabilities.json`

脚本会按能力表校验：
- `model`、`resolution` 是否匹配
- `images` 数量与模型限制
- `gen_duration` 是否被模型支持，且值是否合法
- `generate_audio` 是否被模型支持

## 执行方式

先准备 payload（示例：`/tmp/generate_ai_video_payload.json`）：

```json
{
  "model": "seedance-1.5-pro",
  "prompt": "一位主播在桌前讲解护肤品卖点，镜头平稳推进，背景干净高级",
  "resolution": "1080x1920",
  "gen_duration": 6,
  "generate_audio": true
}
```

执行：

```bash
python <skill-path>/scripts/generate_ai_video_async.py \
  "/tmp/generate_ai_video_payload.json" \
  --output "./generated_ai_video_result.json"
```

可选参数：
- `--poll-interval`：轮询间隔，默认 `2.0`
- `--timeout`：总超时秒数，默认 `1800`
- `--capabilities`：模型能力配置路径

## 输出结果

默认输出 `generated_ai_video_result.json`，核心字段：
- `meta.task_id`
- `meta.final_status`
- `result.video_url`
- `result.draft_id`
- `result.draft_url`
- `result.raw_result`

## 与 human-pip 的联动

- 先用本技能生成背景视频 `video_url`
- 再把该 URL 作为 `human-pip` 的 `background_video_url`
- 可形成“人物讲解 + AI broll 背景”流程
