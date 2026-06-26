---
name: wan-video-gen-edit-2.7
description: Video Generation and Editing with Wan 2.7 series models. Supports text2video, image2video (first-frame, first+last-frame, video-continuation), reference2video, and video-editing capabilities.
homepage: https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["python3","requests"],"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY"},"author":"KrisYe"}
---

# Wan 2.7 Video Models

Wan 2.7 Video Models, created by Alibaba Group, are the latest generation of video generation and editing models. This skill integrates with Wan 2.7 Model APIs on ModelStudio (Bailian-Alibaba Model Service Platform).

## Model Overview

| Model | Capabilities | Resolution | Duration |
| --- | --- | --- | --- |
| wan2.7-t2v | Text to Video, Multi-shot narrative, Auto audio | 720P, 1080P | 2-15s |
| wan2.7-i2v | First-frame, First+Last-frame, Video continuation | 720P, 1080P | 2-15s |
| wan2.7-r2v | Reference images/videos to video, Multi-character | 720P, 1080P | 2-10s |
| wan2.7-videoedit | Video editing, Style transfer, Reference-based edit | 720P, 1080P | 2-10s |

## Text to Video Generation (wan2.7-t2v)

Generate videos from text prompts with optional audio.

### text2video task-submit
```bash
python3 {baseDir}/scripts/wan27-magic.py text2video-gen --prompt "一只小猫在月光下奔跑" --resolution "1080P" --ratio "16:9" --duration 5
python3 {baseDir}/scripts/wan27-magic.py text2video-gen --prompt "一段紧张刺激的侦探追查故事，展现电影级叙事能力。第1个镜头[0-3秒] 全景:雨夜的纽约街头，霓虹灯闪烁，一位身穿黑色⻛衣的侦探快步行走。 第2个镜头[3-6秒] 中景:侦探进入一栋老旧建筑，雨水打湿了他的外套，⻔在他身后缓缓关闭。 第3个镜头[6-9秒] 特写:侦探的眼神坚毅专注，远处传来警 笛声，他微微皱眉思考。 第4个镜头[9-12秒] 中景:侦探在昏暗走廊中小心前行，手电筒照亮前方。 第5个镜头[12-15秒] 特写:侦探发现关键线索，脸上露出恍然大悟的表情。" --resolution "720P" --ratio "16:9" --duration 15
python3 {baseDir}/scripts/wan27-magic.py text2video-gen --prompt "一幅史诗级可爱的场景，一只小猫将军站在悬崖上" --audio-url "https://example.com/audio.mp3" --duration 10
```

### Options
- `--prompt`: Text prompt for video generation (required, max 5000 chars)
- `--negative-prompt`: Content to avoid in the video (optional, max 500 chars)
- `--resolution`: Video resolution - `720P` or `1080P` (default: 1080P)
- `--ratio`: Aspect ratio - `16:9`, `9:16`, `1:1`, `4:3`, `3:4` (default: 16:9)
- `--duration`: Video duration in seconds, 2-15 (default: 5)
- `--audio-url`: Custom audio URL for video (optional, wav/mp3, 2-30s)
- `--prompt-extend`: Enable intelligent prompt rewriting (default: enabled)
- `--no-prompt-extend`: Disable intelligent prompt rewriting
- `--watermark`: Add "AI Generated" watermark (default: disabled)

### text2video tasks-get (round-robin)
```bash
python3 {baseDir}/scripts/wan27-magic.py text2video-get --task-id "<TASK_ID_FROM_VIDEO_GEN>"
```

## Image to Video Generation (wan2.7-i2v)

Generate video from image(s) with support for first-frame, first+last-frame, and video continuation.

### First-frame to Video
```bash
python3 {baseDir}/scripts/wan27-magic.py image2video-gen --prompt "一幅都市奇幻艺术的场景" --first-frame "https://example.com/first.png" --resolution "720P" --duration 10
python3 {baseDir}/scripts/wan27-magic.py image2video-gen --prompt "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。" --first-frame "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png" --driving-audio "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3" --duration 10
```

### First + Last Frame to Video
```bash
python3 {baseDir}/scripts/wan27-magic.py image2video-gen --prompt "写实⻛格,一只小黑猫好奇地仰望天空,镜头从平视角度逐渐升高,最后以俯视角度捕捉到它好奇的眼神。" --first-frame "https://wanx.alicdn.com/material/20250318/first_frame.png" --last-frame "https://wanx.alicdn.com/material/20250318/last_frame.png" --no-prompt-extend --resolution "720P" --duration 10
```

### Video Continuation(First Clip + prompt or First Clip + Last Frame)
```bash
python3 {baseDir}/scripts/wan27-magic.py image2video-gen --prompt "一只戴着墨镜的狗在街道上滑滑板" --first-clip "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4" --no-prompt-extend --resolution "720P" --duration 15
python3 {baseDir}/scripts/wan27-magic.py image2video-gen --prompt "继续之前的场景" --first-clip "https://example.com/video.mp4" --last-frame "https://example.com/end.png" --duration 10
```

### Options
- `--prompt`: Text prompt (optional but recommended, max 5000 chars)
- `--negative-prompt`: Content to avoid (optional, max 500 chars)
- `--first-frame`: First frame image URL (required for first-frame mode)
- `--last-frame`: Last frame image URL (optional, for first+last-frame mode)
- `--first-clip`: First video clip URL (required for video continuation, 2-10s)
- `--driving-audio`: Audio URL to drive the video (optional, wav/mp3, 2-30s)
- `--resolution`: Video resolution - `720P` or `1080P` (default: 1080P)
- `--duration`: Video duration 2-15s (default: 5)
- `--prompt-extend`: Enable intelligent prompt rewriting (default: enabled)
- `--no-prompt-extend`: Disable intelligent prompt rewriting
- `--watermark`: Add watermark (default: disabled)

### image2video tasks-get (round-robin)
```bash
python3 {baseDir}/scripts/wan27-magic.py image2video-get --task-id "<TASK_ID_FROM_VIDEO_GEN>"
```

## Reference to Video Generation (wan2.7-r2v)

Generate video using reference images and videos as character/scene sources.

### Multi-character Reference
```bash
python3 {baseDir}/scripts/wan27-magic.py reference2video-gen --prompt "视频1在沙发上看电影，图片1在旁边唱歌" --reference-videos "https://example.com/person.mp4" --reference-images "https://example.com/singer.png" --resolution "720P" --duration 10
python3 {baseDir}/scripts/wan27-magic.py reference2video-gen --prompt "视频1对视频2说：听起来不错" --reference-videos "https://example.com/role1.mp4" "https://example.com/role2.mp4" --resolution "1080P" --ratio "16:9" --duration 10
python3 {baseDir}/scripts/wan27-magic.py reference2video-gen --prompt "视频1一边喝奶茶，一边随着音乐即兴跳舞" --reference-videos "https://cdn.wanx.aliyuncs.com/static/demo-wan26/vace.mp4" --resolution "720P" --duration 10
python3 {baseDir}/scripts/wan27-magic.py reference2video-gen --prompt "视频2中的角色坐在靠窗的椅子上，手持图片1，在图片2旁演奏一首舒缓的美国乡村民谣。视频1的角色对视频2角色开口说道：“听起来不错”" --reference-videos "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4" "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4" --reference-images "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png" "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png" --resolution "1080P" --duration 10
python3 {baseDir}/scripts/wan27-magic.py reference2video-gen --prompt "视频1对接镜头唱起了rap嘻哈音乐" --reference-videos "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4" --reference-voice "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3" --resolution "720P" --duration 10
```

### With First Frame Control
```bash
python3 {baseDir}/scripts/wan27-magic.py reference2video-gen --prompt "图片1在海边散步" --reference-images "https://example.com/person.png" --first-frame "https://example.com/beach.png" --resolution "720P" --duration 5
python3 {baseDir}/scripts/wan27-magic.py reference2video-gen --prompt "视频1戴着一副头戴式耳机，似乎在听着非常有节奏的音乐，非常快乐，走进这家咖啡厅，拿起桌上的报纸看起来" --reference-videos "https://cdn.wanx.aliyuncs.com/static/demo-wan26/vace.mp4" --first-frame "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png" --resolution "720P" --duration 10
```

### Options
- `--prompt`: Text prompt with character references (required, max 5000 chars). Use "视频1/视频2" to reference videos, "图片1/图片2" to reference images.
- `--negative-prompt`: Content to avoid (optional, max 500 chars)
- `--reference-videos`: Reference video URLs (max 3 videos). Referenced as "视频1", "视频2", etc. in prompt.
- `--reference-images`: Reference image URLs (max 5 images). Referenced as "图片1", "图片2", etc. in prompt.
- `--first-frame`: First frame image URL (optional)
- `--reference-voice`: Audio URL for voice of a specific character (optional, wav/mp3, 1-10s)
- `--resolution`: Video resolution - `720P` or `1080P` (default: 1080P)
- `--ratio`: Aspect ratio - `16:9`, `9:16`, `1:1`, `4:3`, `3:4` (default: 16:9). Ignored if first-frame provided.
- `--duration`: Video duration 2-10s (default: 5)
- `--watermark`: Add watermark (default: disabled)

Note: At least one of `--reference-videos` or `--reference-images` is required. 

### reference2video tasks-get (round-robin)
```bash
python3 {baseDir}/scripts/wan27-magic.py reference2video-get --task-id "<TASK_ID_FROM_VIDEO_GEN>"
```

## Video Editing (wan2.7-videoedit)

Edit existing videos with text instructions and optional reference images.

### Instruction-based Editing
```bash
python3 {baseDir}/scripts/wan27-magic.py video-edit --prompt "为人物换上酷闪的衣服" --video "https://example.com/original.mp4" --resolution "720P"
python3 {baseDir}/scripts/wan27-magic.py video-edit --prompt "将场景变成夜晚，添加霓虹灯效果" --video "https://example.com/video.mp4"
```

### Reference Image-based Editing
```bash
python3 {baseDir}/scripts/wan27-magic.py video-edit --prompt "为人物换上参考图里的帽子" --video "https://example.com/video.mp4" --reference-images "https://example.com/hat.png"
python3 {baseDir}/scripts/wan27-magic.py video-edit --prompt "参考视频运镜和动作，用一个卡通小狗形象实现类似效果" --video "https://example.com/video.mp4" --reference-images "https://example.com/dog.png"
```

### Options
- `--prompt`: Editing instruction (optional but recommended, max 5000 chars)
- `--negative-prompt`: Content to avoid (optional, max 500 chars)
- `--video`: Input video URL to edit (required, mp4/mov, 2-10s)
- `--reference-images`: Reference image URLs for editing (optional, max 3 images)
- `--resolution`: Output resolution - `720P` or `1080P` (default: 1080P)
- `--ratio`: Aspect ratio (optional). If not set, uses input video ratio.
- `--duration`: Output duration (optional, 0 = same as input video, range 2-10s)
- `--audio-setting`: Audio handling - `auto` (default) or `origin` (keep original audio)
- `--watermark`: Add watermark (default: disabled)

Note: `--prompt-extend` is not supported for wan2.7-videoedit.

### video-edit tasks-get (round-robin)
```bash
python3 {baseDir}/scripts/wan27-magic.py video-edit-get --task-id "<TASK_ID_FROM_VIDEO_EDIT>"
```

## Resolution and Aspect Ratio Reference

| Resolution | Aspect Ratio | Output Size (W*H) |
| --- | --- | --- |
| 720P | 16:9 | 1280*720 |
| 720P | 9:16 | 720*1280 |
| 720P | 1:1 | 960*960 |
| 720P | 4:3 | 1104*832 |
| 720P | 3:4 | 832*1104 |
| 1080P | 16:9 | 1920*1080 |
| 1080P | 9:16 | 1080*1920 |
| 1080P | 1:1 | 1440*1440 |
| 1080P | 4:3 | 1648*1248 |
| 1080P | 3:4 | 1248*1648 |

## Important Notes

- **Task ID Validity**: Task IDs are valid for 24 hours
- **Video URL Validity**: Generated video URLs are valid for 24 hours, download immediately
- **Content Review**: Both input and output are subject to content safety review
- **Billing**: Based on resolution (1080P > 720P) × duration (seconds)
- **Multi-shot Narrative**: Use natural language in prompt to describe shots (e.g., "第1个镜头[0-3秒]...")
- **Migration from wan2.6**: wan2.7 uses `resolution` + `ratio` instead of `size`, and `shot_type` parameter is deprecated (use prompt instead)
