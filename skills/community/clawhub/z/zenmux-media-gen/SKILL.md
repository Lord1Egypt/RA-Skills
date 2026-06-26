---
name: zenmux-media-gen
description: "Generate images & videos with ZenMux. Support multiple image models (Gemini, Qwen, Hunyuan, etc.) and video models (Veo, Seedance) via one API key."
homepage: https://zenmux.ai
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["python3","curl"],"env":["ZENMUX_API_KEY"]},"primaryEnv":"ZENMUX_API_KEY"}}
---

# ZenMux Media Gen 🎬

用 ZenMux API 一把钥匙生成**图片**与**视频**：

支持的图片模型：
- `google/gemini-3-pro-image-preview`（Gemini 3 Pro Image， 高质量）
- `google/gemini-2.5-flash-image`（Gemini 2.5 Flash Image，性价比高）
- `qwen/qwen-image-2.0`（通义万相 Image 2.0）
- `tencent/hunyuan-image3`（腾讯混元 Image 3）
- `openai/gpt-image-1.5`（OpenAI GPT Image）

支持的视频模型：
- `google/veo-3.1-generate-001`（Google Veo 3.1，高质量）
- `volcengine/doubao-seedance-1.5-pro`（字节Seedance）

## 🔥 你可以做什么

### 图片生成
```
"生成一张赛博朋克风格的城市夜景，霓虹灯，雨夜，电影感"
```

### 视频生成（Veo 3.1）
```
"生成5秒视频：一个宇航员在火星上漫步，日落，电影感"
```

## Quick Start

```bash
export ZENMUX_API_KEY="your-key"
```

---

## 🖼️ Image Generation

### Endpoint

- Base URL: `https://api.zenmux.ai/v1`
- `POST /chat/completions`（OpenAI兼容格式）

### curl 示例

```bash
curl -X POST "https://api.zenmux.ai/v1/chat/completions" \
  -H "Authorization: Bearer $ZENMUX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.5-flash-image",
    "messages": [{"role": "user", "content": "A cute red panda, ultra-detailed, cinematic lighting"}],
    "modalities": ["image"]
  }'
```

### 可用图片模型

| 模型ID | 描述 | 价格 |
|--------|------|------|
| `google/gemini-3-pro-image-preview` | Gemini 3 Pro Image，高质量 | $12-18/M |
| `google/gemini-2.5-flash-image` | Gemini 2.5 Flash，性价比高 | $2.5/M |
| `google/gemini-3.1-flash-image-preview` | Gemini 3.1 Flash | $3/M |
| `qwen/qwen-image-2.0` | 通义万相 Image 2.0 | - |
| `qwen/qwen-image-2.0-pro` | 通义万相 Image 2.0 Pro | - |
| `tencent/hunyuan-image3` | 腾讯混元 Image 3 | - |
| `openai/gpt-image-1.5` | OpenAI GPT Image 1.5 | $10/M |
| `volcengine/doubao-seedream-5.0-lite` | 字节Seedream 5.0 | $0.032/counts |
| `z-ai/glm-image` | 智谱GLM Image | - |
| `klingai/kling-v2` | 可灵AI | $0.014/counts |

---

## 🎞️ Video Generation (Veo 3.1)

### Create Task

- Base URL: `https://api.zenmux.ai/v1`
- `POST /images/generations`（Google Veo 使用 Image Generation API）

```bash
curl -X POST "https://api.zenmux.ai/v1/images/generations" \
  -H "Authorization: Bearer $ZENMUX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/veo-3.1-generate-001",
    "prompt": "A astronaut walking on Mars, sunset, cinematic",
    "parameters": {
      "duration": 8,
      "resolution": "720p"
    }
  }'
```

### Poll Task

```bash
curl "https://api.zenmux.ai/v1/images/generations/{task_id}" \
  -H "Authorization: Bearer $ZENMUX_API_KEY"
```

### 可用视频模型

| 模型ID | 描述 | 价格 |
|--------|------|------|
| `google/veo-3.1-generate-001` | Google Veo 3.1，8秒高质量视频 | $0.4-0.6/秒 |
| `volcengine/doubao-seedance-1.5-pro` | 字节Seedance 1.5 Pro，音视频同步 | $2.33/M |

---

## Python Client

```bash
# 生成图片（默认使用 Gemini 3 Pro Image）
python3 {baseDir}/scripts/zenmux_media_client.py image \
  --prompt "A cute red panda, cinematic lighting" \
  --out "out.png"

# 生成视频任务（Veo 3.1）
python3 {baseDir}/scripts/zenmux_media_client.py video-create \
  --model "google/veo-3.1-generate-001" \
  --prompt "A astronaut walking on Mars, sunset" \
  --duration 8

# 轮询任务状态
python3 {baseDir}/scripts/zenmux_media_client.py video-status --task-id YOUR_TASK_ID

# 等待直到成功并自动下载
python3 {baseDir}/scripts/zenmux_media_client.py video-wait --task-id YOUR_TASK_ID --download --out out.mp4
```

---

## 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `ZENMUX_API_KEY` | ✅ | ZenMux API Key，从 https://zenmux.ai 获取 |

---

## 配置示例

### 使用 Gemini 3 Pro（高质量，默认）
```bash
export ZENMUX_API_KEY="your-key"
python3 scripts/zenmux_media_client.py image \
  --prompt "高清电影质感海报" \
  --out movie_poster.png
```

### 使用 Veo 3.1（视频）
```bash
python3 scripts/zenmux_media_client.py video-create \
  --model "google/veo-3.1-generate-001" \
  --prompt "宇航员在火星漫步" \
  --duration 8
```
