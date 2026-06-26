# SuperX AI 绘画 API Skills 文档

> 基础地址：`https://superx.chat/art/imgapi`
> 图片 CDN 前缀：`https://oc.superx.chat`
> 鉴权方式：`Authorization: <your-api-key>`（放在请求 Header 中）

---

## 通用说明

### 鉴权

所有接口都需要在 HTTP Header 中传入 API Key：

```
Authorization: your_api_key_here
```

API Key 在 SuperX 平台的个人设置中获取。所有操作消耗点数，请确保账户余额充足。

### 响应格式

**普通接口**返回 JSON：

```json
{ "code": 0, "message": "success", "data": { ... } }
```

**流式接口**返回 chunked JSON，每行是一个独立 JSON 对象，通过 `progress` 字段跟踪进度，最终结果包含 `code: 0`。

### 图片 URL 拼接

返回的 `img_url` 通常是相对路径（如 `/gpt-4o-img/xxx.png`），完整访问地址为：

```
https://oc.superx.chat/gpt-4o-img/xxx.png
```

---

## 1. 查询余额

查询当前 API Key 对应的账户点数余额。

- **URL**: `GET /balance`
- **消耗**: 0 点

**curl 示例**:

```bash
curl -X GET 'https://superx.chat/art/imgapi/balance' \
  -H 'Authorization: your_api_key'
```

**返回**:

```json
{ "code": 0, "message": "success", "data": { "balance": 1000 } }
```

---

## 2. GPT-4o 图像生成

使用 GPT-4o（gpt-image-1）生成或编辑图片。支持文生图和图编辑。

- **URL**: `POST /gpt4o-image`
- **消耗**: 8 点/张
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 提示词，最长 32000 字符 |
| n | number | 否 | 生成数量，1-10，默认 1 |
| size | string | 否 | `auto`/`1024x1024`/`1536x1024`/`1024x1536`，默认 `auto` |
| images | string[] | 否 | 参考图 URL 数组（传入则走编辑模式），最多 10 张 |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/gpt4o-image' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "一只穿着宇航服的猫咪在月球上散步",
    "n": 1,
    "size": "1024x1024"
  }'
```

**图片编辑示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/gpt4o-image' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "把背景改成海边日落",
    "images": ["https://oc.superx.chat/gpt-4o-img/original.png"],
    "n": 1
  }'
```

**流式返回**（每行一个 JSON）:

```json
{"ps":""}
{"ps":""}
{"progress":"100%","code":0,"message":"success","data":{"result":[{"img_url":"/gpt-4o-img/20250501105657.png","id":12345}],"cost":8}}
```

---

## 3. Midjourney 绘画（imagine）

使用 Midjourney 根据提示词生成图片。

- **URL**: `POST /imagine`
- **消耗**: 8 点
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 英文提示词，最多 800 个单词。支持 `--v 6` 等 MJ 参数 |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/imagine' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{ "prompt": "a futuristic city at sunset --v 6 --ar 16:9" }'
```

**流式返回**:

```json
{"uri":"","progress":"0%"}
{"uri":"https://cdn.discordapp.com/...","progress":"40%"}
{"uri":"https://cdn.discordapp.com/...","progress":"100%","id":"task_id_xxx","content":"..."}
```

---

## 4. Midjourney Variation（变体）

对已生成的 MJ 图片生成变体。

- **URL**: `POST /variation`
- **消耗**: 8 点
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| index | number | 是 | 变体索引（1-4） |
| imgId | string | 是 | imagine 返回的图片任务 ID |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/variation' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{ "index": 1, "imgId": "task_id_xxx" }'
```

---

## 5. Midjourney Upscale（放大）

放大 MJ 四宫格中的某一张图片。

- **URL**: `POST /upscale`
- **消耗**: 2 点
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| index | number | 是 | 图片索引（1-4） |
| imgId | string | 是 | imagine 返回的图片任务 ID |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/upscale' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{ "index": 2, "imgId": "task_id_xxx" }'
```

---

## 6. Midjourney 按钮动作

执行 MJ 的扩展操作按钮（如 Pan、Zoom、Vary 等）。

- **URL**: `POST /do-button-click`
- **消耗**: 视按钮类型而定（2-16 点）
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| buttonId | string | 是 | 按钮 ID（从任务详情的 buttons 列表获取） |
| imgId | string | 是 | 图片任务 ID |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/do-button-click' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{ "buttonId": "MJ::JOB::pan_left::1", "imgId": "task_id_xxx" }'
```

---

## 7. Midjourney 图片融合（Blend）

将 2-5 张图片融合为一张。

- **URL**: `POST /blend`
- **消耗**: 8 点
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| imgs | string[] | 是 | 图片 URL 数组，2-5 张 |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/blend' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "imgs": [
      "https://example.com/img1.png",
      "https://example.com/img2.png"
    ]
  }'
```

---

## 8. Midjourney 区域重绘（Submit Modal）

提交区域蒙版和新提示词，对图片局部重新生成。

- **URL**: `POST /submit-modal`
- **消耗**: 8 点
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| taskId | string | 是 | 图片任务 ID |
| maskBase64 | string | 是 | 蒙版图片的 Base64 编码 |
| prompt | string | 是 | 新的提示词 |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/submit-modal' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "taskId": "task_id_xxx",
    "maskBase64": "iVBORw0KGgo...",
    "prompt": "a red sports car"
  }'
```

---

## 9. Midjourney Describe（以图生文）

上传图片，让 MJ 生成描述提示词。

- **URL**: `POST /img-describe-mj`
- **消耗**: 2 点

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| imgUrl | string | 是 | 图片 URL |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/img-describe-mj' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{ "imgUrl": "https://example.com/photo.jpg" }'
```

**返回**:

```json
{ "code": 0, "data": { "prompt": "a serene landscape with...", "cost": 2 } }
```

---

## 10. Midjourney Get Seed

获取已生成图片的 seed 值，用于复现。

- **URL**: `GET /get-seed?taskId=xxx`
- **消耗**: 2 点（未获取到 seed 则不扣费）

**curl 示例**:

```bash
curl -X GET 'https://superx.chat/art/imgapi/get-seed?taskId=task_id_xxx' \
  -H 'Authorization: your_api_key'
```

**返回**:

```json
{ "code": 0, "data": { "seed": "1234567890", "cost": 2 } }
```

---

## 11. OpenAI DALL-E 绘画

使用 DALL-E 2 或 DALL-E 3 生成图片。

- **URL**: `POST /openai-dalle-painting`
- **消耗**: DALL-E 2 为 4 点；DALL-E 3 为 8 点（大尺寸/HD 翻倍）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 提示词（或 `caption`），最长 1000 字符 |
| model | string | 否 | `dall-e-2`（默认）或 `dall-e-3` |
| size | string | 否 | `1024x1024`/`1792x1024`/`1024x1792`（DALL-E 3） |
| quality | string | 否 | `standard`/`hd`（仅 DALL-E 3） |
| style | string | 否 | `vivid`/`natural`（仅 DALL-E 3） |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/openai-dalle-painting' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "一幅水彩风格的田园风光",
    "model": "dall-e-3",
    "size": "1792x1024",
    "quality": "hd"
  }'
```

**返回**:

```json
{ "code": 0, "data": { "id": 12345, "img_url": "/dalleprodsec/private/dalle3/xxx.png", "prompt": "...", "revised_prompt": "..." } }
```

---

## 12. Stable Diffusion 绘画

使用 Stable Diffusion 引擎进行文生图或图生图。

- **URL**: `POST /sd-painting`
- **消耗**: 按分辨率和步数动态计算（约 1-30 点）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 提示词 |
| engineId | string | 是 | 引擎 ID，如 `stable-diffusion-512-v2-1` |
| width | number | 否 | 图片宽度（64 的倍数） |
| height | number | 否 | 图片高度（64 的倍数） |
| steps | number | 否 | 生成步数（15-150） |
| samples | number | 否 | 生成张数 |
| cfg_scale | number | 否 | 提示词权重，默认 7 |
| style_preset | string | 否 | 风格预设 |
| seed | number | 否 | 随机种子 |
| image_url | string | 否 | 参考图 URL（传入则走图生图） |
| image_strength | number | 否 | 参考图权重，默认 0.5 |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/sd-painting' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "a fantasy castle on a mountain",
    "engineId": "stable-diffusion-512-v2-1",
    "width": 768,
    "height": 512,
    "steps": 30,
    "samples": 1
  }'
```

---

## 13. AI 视频生成

使用豆包 Seedance 模型生成视频。

- **URL**: `POST /ai-video-generate`
- **消耗**: 视频数量 x 时长(秒) x 每秒点数
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | `doubao-seedance-1-0-pro-250528` |
| prompt | string | 是 | 提示词，最长 50000 字符 |
| n | number | 否 | 视频数量，1-5，默认 1 |
| duration | number | 否 | 时长（秒），默认 6 |
| ratio | string | 否 | 画面比例：`16:9`/`9:16`/`1:1`/`4:3`/`3:4`/`21:9`，默认 `16:9` |
| image | string | 否 | 参考图 URL（传入时不使用 ratio） |
| seed | number | 否 | 随机种子 |
| resolution | string | 否 | 分辨率，默认 `1080p` |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/ai-video-generate' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "doubao-seedance-1-0-pro-250528",
    "prompt": "一只金毛犬在沙滩上奔跑，慢动作，电影感",
    "duration": 6,
    "ratio": "16:9"
  }'
```

**流式返回**:

```json
{"progress":"0%"}
{"progress":"25%","status":"视频生成中..."}
{"progress":"90%","status":"视频上传中..."}
{"progress":"100%","code":0,"data":{"result":[{"video_url":"/ai-videos/xxx.mp4","id":12345,"duration":6,"cost":60}],"total_cost":60}}
```

---

## 14. 即梦 4.0 图片生成

使用豆包 Seedream 4.5 模型生成图片，支持单图、组图和故事书模式。

- **URL**: `POST /jimeng4-generate`
- **消耗**: 每张图片固定点数（按实际生成数量计费）
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 提示词，最长 50000 字符 |
| size | string | 是 | 尺寸：`2k`/`2048x2048`/`2304x1728`/`1728x2304`/`2560x1440`/`1440x2560`/`2496x1664`/`1664x2496`/`3024x1296` |
| mode | string | 是 | `single`（单图）/`group`（组图）/`story`（故事书） |
| count | number | 否 | 组图/故事书模式的图片数量，1-15 |
| image | string | 否 | 参考图 URL |
| target_audience | string | 否 | 故事书读者群，默认`全年龄` |
| watermark | boolean | 否 | 是否添加水印 |

**单图示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/jimeng4-generate' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "一只穿着汉服的猫咪在赏花",
    "size": "2048x2048",
    "mode": "single"
  }'
```

**故事书示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/jimeng4-generate' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "龟兔赛跑的故事，现代版",
    "size": "2304x1728",
    "mode": "story",
    "count": 5,
    "target_audience": "儿童"
  }'
```

**流式返回（故事书模式会附带文案）**:

```json
{"progress":"10%","status":"正在创作故事..."}
{"progress":"30%","status":"故事创作完成，开始生成6张配图（包含1张封面）..."}
{"progress":"40%","status":"已生成1/6张图片（包含封面）...","image_url":"/jimeng4-images/xxx.png","image_index":0,"text":"封面文案"}
{"progress":"100%","code":0,"data":{"id":12345,"result":{"title":"书名","summary":"总结","images":[...],"texts":[...]},"cost":48}}
```

---

## 15. NanoBanana 图片生成

使用 Gemini 3 Pro 模型生成图片，支持多张参考图。

- **URL**: `POST /nanobanana-generate`
- **消耗**: 固定点数/张
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 提示词，最长 10000 字符 |
| image_urls | string[] | 否 | 参考图 URL 数组 |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/nanobanana-generate' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "把这张照片变成吉卜力风格的动画插画",
    "image_urls": ["https://example.com/photo.jpg"]
  }'
```

**流式返回**:

```json
{"progress":"10%","status":"开始生成图片..."}
{"progress":"50%","status":"正在生成图片..."}
{"progress":"80%","status":"正在上传图片..."}
{"progress":"100%","code":0,"data":{"img_url":"/nanobanana-images/xxx.png","id":12345,"cost":10,"retry_count":0}}
```

---

## 16. 图片放大（Super Resolution）

将图片进行 AI 超分辨率放大。

- **URL**: `POST /image-upscale`
- **消耗**: 放大倍数^2 * 5 + 10 点

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| img_url | string | 是 | 图片 URL |
| scale_num | number | 是 | 放大倍数 |
| upscaler_1 | string | 否 | 放大算法 |
| codeformer_visibility | number | 否 | 面部修复可见度 |
| codeformer_weight | number | 否 | 面部修复权重 |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/image-upscale' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "img_url": "https://example.com/small.jpg",
    "scale_num": 2
  }'
```

---

## 17. AI 换脸

将一张人脸替换到目标图片上。

- **URL**: `POST /face-swap`
- **消耗**: 60 点

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | string | 是 | 人脸源图 URL |
| target | string | 是 | 目标图 URL |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/face-swap' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "source": "https://example.com/face.jpg",
    "target": "https://example.com/target.jpg"
  }'
```

---

## 18. AI 二维码生成

使用 AI 生成艺术风格二维码。

- **URL**: `POST /qrcode-generate`
- **消耗**: 30 点
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| params | object | 是 | 二维码生成参数（含 prompt、二维码内容等） |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/qrcode-generate' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "params": {
      "prompt": "a beautiful garden with flowers",
      "qr_content": "https://superx.chat"
    }
  }'
```

---

## 19. Suno 音乐生成

使用 Suno AI 生成音乐。

- **URL**: `POST /suno-music-generate`
- **消耗**: 40 点
- **响应**: 流式（chunked）

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 音乐描述 |
| modelVersion | string | 否 | `v3`（默认）或 `v2` |

**curl 示例**:

```bash
curl -X POST 'https://superx.chat/art/imgapi/suno-music-generate' \
  -H 'Authorization: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "一首欢快的儿童歌曲，关于春天和花朵",
    "modelVersion": "v3"
  }'
```

---

## 错误码参考

| code | 含义 |
|------|------|
| 0 | 成功 |
| -1 | 通用错误 |
| 10001 | 参数错误 |
| 10002 | 未登录 / API Key 无效 |
| 10003 | 点数不足 |
| 10010 | 生成出错 |
| 10011 | 包含敏感词 |

---

## 点数费率汇总

| 功能 | 单次消耗 |
|------|----------|
| GPT-4o 图像生成 | 8 点/张 |
| Midjourney imagine | 8 点 |
| Midjourney variation | 8 点 |
| Midjourney upscale | 2 点 |
| Midjourney button 动作 | 2-16 点 |
| Midjourney blend | 8 点 |
| Midjourney describe | 2 点 |
| Midjourney get seed | 2 点 |
| DALL-E 2 | 4 点 |
| DALL-E 3 | 8-32 点 |
| Stable Diffusion | 1-30 点（按参数计算） |
| AI 视频生成 | 时长(秒) x 每秒点数 x 数量 |
| 即梦 4.0 | 按实际生成图片数量计费 |
| NanoBanana | 固定点数/张 |
| 图片放大 | 倍数² x 5 + 10 |
| 换脸 | 60 点 |
| AI 二维码 | 30 点 |
| Suno 音乐 | 40 点 |
