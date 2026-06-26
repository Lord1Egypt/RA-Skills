---
name: Seedance Video
description: Generate AI videos with ByteDance Seedance (豆包/火山方舟) via Ark API. Supports text-to-video and image-to-video using model endpoint doubao-seedance-1-5-pro-251215. Use when the user wants to create videos from text or from an image, or mentions 火山、豆包、Seedance or AI video generation.
read_when:
  - Generating video from text prompts
  - Creating video from an image (image-to-video, 图生视频)
  - 火山模型、豆包、Ark、Seedance video generation
metadata: {"clawdbot":{"emoji":"🎬","requires":{"env":["ARK_API_KEY"]}}}
allowed-tools: Bash(curl:*)
---

# 视频生成：火山方舟 Seedance（豆包 Ark API）

## 概述

通过**火山引擎方舟（Ark）**的 REST API 调用豆包 Seedance 视频生成模型，支持：

- **文生视频**：仅传入文本描述生成视频。
- **图生视频**：传入一张图片 + 动作/场景描述，生成视频。
- **模型**：使用推理接入点（Endpoint）ID，例如 `doubao-seedance-1-5-pro-251215`。提示词中可用参数控制时长、比例、镜头、水印等。

Base URL：`https://ark.cn-beijing.volces.com`。所有请求需在 Header 中携带：`Authorization: Bearer $ARK_API_KEY`。

## 准备

1. 在[火山方舟](https://console.volcengine.com/ark)创建 API Key，并创建/选用已部署 **Seedance 视频生成** 的推理接入点。
2. 设置环境变量（以下示例均依赖此变量）：

```bash
export ARK_API_KEY="your_ark_api_key_here"
```

## 核心流程

1. **创建任务**：`POST /api/v3/contents/generations/tasks`，Body 中传 `model`（接入点 ID）和 `content`（见下）。响应返回任务 `id`。
2. **轮询状态**：`GET /api/v3/contents/generations/tasks/{id}`，直到 `status` 为 `succeeded` 或 `failed`。建议每 8–15 秒轮询一次。
3. **获取视频**：当 `status` 为 `succeeded` 时，从响应中的 `content` 里取 `video_url`（MP4，约 24 小时后清理，请及时下载）。

## 创建任务：请求体说明

- **model**（必填）：推理接入点 ID，需已部署视频生成模型。例如图生视频：`doubao-seedance-1-5-pro-251215`。
- **content**（必填）：数组，按顺序组合「文本」与「图片」：
  - **文生视频**：一个元素即可，`type: "text"`，`text` 为视频描述，可在同一字符串内带参数，例如：`"描述内容 --duration 5 --ratio 16:9 --camerafixed false --watermark true"`。
  - **图生视频**：先一个 `type: "text"`（描述动作/场景，可带 `--duration` 等参数），再一个 `type: "image_url"`，`image_url.url` 为图片公网 URL。

文本中的常用参数（以空格分隔，写在描述后面）：

- `--duration 5`：时长（秒）。
- `--ratio 1:1` 或 `16:9`、`9:16`：画面比例。
- `--camerafixed true/false`：是否固定镜头（减少运动模糊）。
- `--watermark true/false`：是否加水印。
- `--fps 24`：帧率（视模型支持而定）。

## 快速开始：图生视频

```bash
# 1. 创建图生视频任务
resp=$(curl -s -X POST 'https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks' \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [
      {
        "type": "text",
        "text": "无人机以极快速度穿越复杂障碍或自然奇观，带来沉浸式飞行体验  --duration 5 --camerafixed false --watermark true"
      },
      {
        "type": "image_url",
        "image_url": {
          "url": "https://your-accessible-image-url.jpg"
        }
      }
    ]
  }')

task_id=$(echo "$resp" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Task ID: $task_id"

# 2. 轮询任务状态
curl -s "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/$task_id" \
  -H "Authorization: Bearer $ARK_API_KEY"

# 3. 当 status 为 succeeded 时，从响应的 content 中取 video_url
```

## 快速开始：文生视频

```bash
curl -s -X POST 'https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks' \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [
      {
        "type": "text",
        "text": "戴着帽子的老爷爷面带微笑往前走 --ratio 1:1 --fps 24 --duration 5"
      }
    ]
  }'
```

## API 参考

### POST /api/v3/contents/generations/tasks（创建任务）

**Headers**

- `Content-Type: application/json`
- `Authorization: Bearer <ARK_API_KEY>`

**Body**

| 字段       | 类型   | 必填 | 说明 |
|------------|--------|------|------|
| `model`    | string | 是   | 推理接入点 ID（如 doubao-seedance-1-5-pro-251215） |
| `content`  | array  | 是   | 内容列表，见下 |

`content` 元素：

- `type: "text"`，`text`: 视频描述 + 可选参数（如 `--duration 5 --ratio 16:9 --camerafixed false --watermark true`）。
- `type: "image_url"`，`image_url`: `{ "url": "https://..." }`，图生视频时使用，图片需公网可访问。

**响应（200）**

```json
{
  "id": "cgt-2024****-**"
}
```

使用返回的 `id` 作为任务 ID 查询状态。

### GET /api/v3/contents/generations/tasks/{id}（查询任务）

**Headers**

- `Authorization: Bearer <ARK_API_KEY>`

**响应中的 status**

- `queued`：排队中
- `running`：生成中
- `succeeded`：成功，此时 `content` 中包含 `video_url`（MP4）
- `failed`：失败，可查看错误信息

成功时，视频地址在响应的 `content.video_url` 中（MP4）。视频链接约 24 小时后失效，请尽快下载。

## 示例

### 图生视频（你提供的写法）

```bash
curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [
      {
        "type": "text",
        "text": "无人机以极快速度穿越复杂障碍或自然奇观，带来沉浸式飞行体验  --duration 5 --camerafixed false --watermark true"
      },
      {
        "type": "image_url",
        "image_url": {
          "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/seepro_i2v.png"
        }
      }
    ]
  }'
```

### 轮询并提取视频 URL

```bash
TASK_ID="cgt-2024****-**"   # 替换为创建任务返回的 id
while true; do
  result=$(curl -s "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/$TASK_ID" \
    -H "Authorization: Bearer $ARK_API_KEY")
  status=$(echo "$result" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)
  if [ "$status" = "succeeded" ]; then
    # 根据实际响应结构调整提取方式，例如：
    video_url=$(echo "$result" | grep -o '"video_url":"[^"]*"' | cut -d'"' -f4)
    echo "Video URL: $video_url"
    break
  fi
  if [ "$status" = "failed" ]; then
    echo "Generation failed. Check response for error details."
    break
  fi
  sleep 10
done
```

### 下载视频

拿到 `video_url` 后建议用 curl 下载到本地再播放（链接带签名参数，浏览器复制时容易漏掉 `?` 后面的部分，会报 AuthorizationQueryParametersError）：

```bash
curl -o output.mp4 "这里粘贴完整 video_url，包含 ? 及后面全部参数"
```

## 故障排查

- **401**：检查 `ARK_API_KEY` 是否正确且已导出。
- **404 / 模型不可用**：确认该接入点已部署视频生成模型，且 `model` 填的是接入点 ID（如 `doubao-seedance-1-5-pro-251215`）。
- **图生视频失败**：确保 `image_url` 为公网可访问的 HTTPS 地址，避免内网或 localhost。
- **等待时间长**：视频生成通常需 1–3 分钟，建议轮询间隔 8–15 秒。
- **链接失效**：`video_url` 约 24 小时后失效，请在成功后尽快下载。
- **打开链接显示 JSON 报错**：若看到 `AuthorizationQueryParametersError` 或 “Query-string authentication version 4 requires the X-Tos-...” 说明访问时未带完整 URL（漏了 `?` 及后面的鉴权参数）。请用 `curl -o 视频.mp4 "完整URL"` 下载到本地再播放。

- API、计费、接入点：[火山方舟控制台](https://console.volcengine.com/ark)与[视频生成 API 文档](https://www.volcengine.com/docs/82379/1520757)
- 本技能文档/示例：[GitHub Issues](https://github.com/maddy-cc/seedance-video-skill/issues)
