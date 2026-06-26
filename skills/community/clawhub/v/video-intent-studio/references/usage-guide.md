# Usage Guide

This file is the quick tutorial for using the skill in a ClawHub-style workflow.

## 1. What this skill does

Turn one rough idea into a staged video generation flow:

1. Understand intent
2. Offer 3 to 5 video type options
3. Let the user pick a type
4. Tune key parameters
5. Show the full prompt and ask for confirmation
6. Generate through the bundled HTTP + polling script

## 2. Folder layout

```text
video-intent-studio/
|- SKILL.md
|- agents/openai.yaml
|- references/
|  |- usage-guide.md
|  `- video-types.md
`- scripts/
   |- generate_ark_video.py
   `- video_agent_backend.py
```

## 3. Environment setup

Set the API key before generation.

```powershell
$env:ARK_API_KEY="your-volcengine-ark-key"
```

Optional model override:

```powershell
$env:ARK_VIDEO_MODEL="doubao-seedance-1-5-pro-251215"
```

## 4. Suggested interaction pattern

### Step A: rank video types

```powershell
python "<skill-dir>/scripts/video_agent_backend.py" suggest --input "一个治愈的海边日落视频"
```

Use the result to answer in a style like:

```text
我先给你 4 个更贴近这个需求的视频方向，请选编号：
1. 唯美风景/氛围片：更适合海边、日落、治愈感，默认 12 秒，16:9
2. 电影感剧情短片：如果你想要更强叙事和情绪推进，默认 10 秒，16:9
3. 竖屏短视频爆款：如果你想发短视频平台，默认 6 秒，9:16
4. 抽象艺术/实验风：如果你想做更梦幻、更超现实的画面，默认 10 秒，16:9
```

### Step B: build a prompt preview after the user picks a type

```powershell
python "<skill-dir>/scripts/video_agent_backend.py" build `
  --input "一个治愈的海边日落视频" `
  --type landscape-atmosphere `
  --duration 12 `
  --ratio 16:9 `
  --motion light `
  --style cinematic `
  --brightness bright `
  --dream-filter on
```

Use the result to answer in a style like:

```text
当前我帮你整理成这个方向：

Prompt 预览：
Atmospheric beauty, soft light, immersive scenery, slow cinematic drift. Core idea: 一个治愈的海边日落视频. Duration: 12s. Aspect ratio: 16:9. Camera motion: gentle drifting movement. Style: cinematic lighting and depth. Brightness: bright and airy. Dream filter: enabled for a soft poetic glow. Subtitle: no on-screen subtitle.

当前参数：
- 时长：12 秒
- 比例：16:9
- 动态：轻微运镜
- 风格：更电影感
- 亮度：更明亮
- 梦幻滤镜：开

你可以直接回复：
- 1 改成 9:16
- 2 更写实一点
- 3 时长改 8 秒
- 4 就这样生成
```

### Step C: final confirmation

Before generation, always show the full prompt and parameters once more.

Example:

```text
最终 prompt 已整理好：
[full prompt]

参数总结：
- 时长：12 秒
- 比例：16:9
- 运镜：轻微
- 风格：电影感

确认生成吗？回复 是 / Y / 生成 即可。
```

### Step D: generate

```powershell
python "<skill-dir>/scripts/generate_ark_video.py" `
  --prompt "Atmospheric beauty, soft light, immersive scenery..." `
  --output "C:\Users\WUJIEAI\Desktop\video\output\sunset.mp4"
```

The script prints JSON including:

- `task_id`
- `status`
- `output_path`
- `video_url`

## 5. Example user journeys

### Example 1: product video

User says:

```text
我想做一个手机产品展示视频，质感高级一点
```

Recommended order:

1. `commercial-product`
2. `cinematic-story`
3. `vertical-social`
4. `abstract-experimental`

### Example 2: scenic mood clip

User says:

```text
想做治愈星空和草地的感觉
```

Recommended order:

1. `landscape-atmosphere`
2. `cinematic-story`
3. `abstract-experimental`
4. `vertical-social`

### Example 3: short-form vertical clip

User says:

```text
做一个适合抖音的竖屏爆款视频，要一开始就抓人
```

Recommended order:

1. `vertical-social`
2. `commercial-product`
3. `cinematic-story`
4. `abstract-experimental`

## 6. Extension points

This skill is intentionally designed to be easy to extend.

- Add image-to-video:
  - extend `generate_ark_video.py` to accept input image fields
  - add new references and a new type or mode flag
- Add first-frame / last-frame controls:
  - keep the same staged workflow
  - add new CLI arguments and include them in prompt preview and confirmation
- Add multiple model backends:
  - expose `--model`
  - add a backend switch while keeping `suggest` and `build` unchanged

## 7. Troubleshooting

- If generation fails immediately, check `ARK_API_KEY`.
- If polling times out, retry with a longer timeout or inspect the printed task payload.
- If no video URL is returned, save the JSON output and inspect the remote response format before changing the extractor.
