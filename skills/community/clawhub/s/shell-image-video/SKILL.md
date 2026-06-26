---
name: shell-image-video
description: "RunningHub AI 工作流集成 — 图片换脸、Wan2.2 动作迁移、动作迁移升级版、150帧高清舞蹈视频。Use when asked about face swap, motion transfer, dance video generation, or RunningHub workflows."
---

# Shell Image & Video Skill

RunningHub AI 工作流集成 - 图片换脸 + 视频动作迁移

## 工具位置
`~/.openclaw/workspace/Shell-openclaw-image-video-skill/`

## 4个工作流

### 1. 图片换脸
```bash
cd ~/.openclaw/workspace/Shell-openclaw-image-video-skill
node scripts/runninghub-face-swap.js --face=./photo.jpg --prompt="场景描述"
# 或用URL
node scripts/runninghub-face-swap.js --faceUrl="https://..." --prompt="场景描述"
```
- 生成时间：~3分钟
- 输出：output/ 目录下 JSON（含图片URL）

### 2. Wan2.2 动作迁移
```bash
node scripts/wan22-animate.js --video=drive.mp4 --reference=face.jpg
```
可选参数：`--fps=30 --width=720 --height=1280 --elasticity=0.6`
生成时间：10-15分钟

### 3. 动作迁移升级版（表情+动作）
```bash
node scripts/motion-pro.js --video=dance.mp4 --reference=target.jpg
```
可选参数：`--duration=5 --skipSeconds=0 --fps=30 --width=928 --height=1664`
生成时间：15-20分钟

### 4. 150帧高清舞蹈
```bash
node scripts/dance-150.js --video=dance.mp4 --reference=dancer.jpg
```
可选参数：`--faceEnhance=2 --duration=5 --skipSeconds=2 --fps=30 --intensity=1`
生成时间：20-25分钟

## Workflow API 工作流（5个数字人/对比工作流）

以下工作流使用 Workflow API（`/openapi/v2/run/workflow/`），需要 `instanceType=plus`。

### 5. 图片对比 GIF/视频
```bash
node scripts/image-compare.js --image1=before.jpg --image2=after.jpg
```
生成时间：2-5分钟

### 6. InfiniteTalk 数字人口播
```bash
node scripts/infinitetalk.js --image=portrait.jpg
node scripts/infinitetalk.js --image=portrait.jpg --audio=speech.mp3
```
生成时间：5-15分钟

### 7. HeyGem + TTS 数字人视频
```bash
node scripts/heygem-tts.js --image=face.jpg --audio=voice.mp3 --text="你好，欢迎来到我的频道"
```
需要：人像 + 5-10秒语音样本 + 文案（中/英/日）
生成时间：10-20分钟

### 8. 单人数字人生成
```bash
node scripts/single-digital-human.js --image=person.jpg --audio=audio.mp3
```
生成时间：~5分钟

### 9. 口播加长版（无限时长）
```bash
node scripts/lipsync-extended.js --image=portrait.jpg --audio=long-speech.mp3
```
人和动物都可以口播，无时长限制
生成时间：10-30分钟

## API Key
已预配置：`7192bd7ed2654d1dbfa24ef0c8576705`

## 注意
- 视频素材建议 720p+
- 视频时长建议 5-10秒（太长容易崩）
- 费用：图片约0.05-0.1元/次，视频约0.5-2元/次


## 常见错误与处理

| 错误 | 原因 | 处理 |
|------|------|------|
| `task_id not found` | RunningHub 任务超时或不存在 | 等待 30s 后重试，最多 3 次 |
| `image too large` | 输入图片超过 10MB | 用 `convert` 压缩到 5MB 以内 |
| `workflow not available` | 工作流离线/排队 | 提示用户稍后重试 |
| HTTP 429 | API 限流 | 等 60s 后重试 |

## 使用示例

### 图片换脸
```
用户: "把这张照片换成 xxx 的脸"
→ 上传图片 → 调用 face-swap 工作流 → 返回结果图
```

### 动作迁移
```
用户: "把这个舞蹈动作迁移到另一个人身上"
→ 上传参考视频 + 目标图片 → motion-transfer 工作流 → 返回视频
```

## 依赖
- RunningHub API Token（环境变量 `RUNNINGHUB_API_KEY`）
- ffmpeg（视频处理）
- ImageMagick（图片压缩）
