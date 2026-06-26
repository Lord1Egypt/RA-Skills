# 【呜哩Wuli】开放平台 API 文档

### 官方skill文档
[[github链接]](https://github.com/alibaba-wuli/wuli-skill#)
[[openclaw链接]](https://clawhub.ai/sir1st-inc/wuli)
[[呜哩Wuli官方 Skill 使用指南]](https://alidocs.dingtalk.com/i/nodes/dQPGYqjpJYZnRbNYCoYejQOP8akx1Z5N?utm_scene=team_space)
[[markdown下载]](https://github.com/alibaba-wuli/wuli-skill/blob/main/references/%E3%80%90%E5%91%9C%E5%93%A9Wuli%E3%80%91%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0%20API%20%E6%96%87%E6%A1%A3.md)

## 概述

呜哩开放平台提供图片生成、视频生成等 AI 能力的 API 接口，支持通过 API Token 进行身份认证。

*   **服务地址**: https://platform.wuli.art
    
*   **认证方式**: 所有平台接口通过请求头 \`Authorization: Bearer <API Token>\` 传递 API Token 进行身份认证
    
*   **积分消耗**: API 调用正常消耗积分，积分明细中以"API调用-"为前缀标记, 注: 会员免费权益仅限在 wuli.art 网页端使用，API 调用不在权益范围内
    
*   **数据隔离**: 通过 API 提交的任务不会出现在网页端的历史记录和资源库中
    

---

## 认证

### 获取 API Token

登录 [wuli.art](https://wuli.art)，在左下角进入「API 开放平台」入口，查看或重置你的访问令牌。

> 重置后旧 Token 立即失效。

### 认证方式

在所有平台 API 请求中，通过请求头传递 Token：

```plaintext
Authorization: Bearer wuli-a1b2c3d4e5f6...
```
---

## 通用响应格式

所有接口响应均遵循以下格式：

```plaintext
{
  "success": true,
  "code": 200,
  "msg": "成功",
  "data": { ... },
  "requestId": "xxx"
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| success | boolean | 请求是否成功 |
| code | int | 状态码，200 为成功 |
| msg | string | 错误信息 |
| data | object | 响应数据 |
| requestId | string | 请求追踪 ID |

---

## 接口列表

### 1. 提交生图/视频任务

```plaintext
POST /api/v1/platform/predict/submit
```

提交一个图片或视频生成任务。任务为异步执行，提交后通过查询接口轮询结果。

#### 请求头

| Header | 必填 | 说明 |
| --- | --- | --- |
| Authorization | 是 | `Bearer <API Token>` |
| Content-Type | 是 | application/json |

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| modelName | string | 是 | 模型名称，见下方[可用模型列表](#%E5%8F%AF%E7%94%A8%E6%A8%A1%E5%9E%8B) |
| prompt | string | 是 | 提示词，最长 2000 字符 |
| mediaType | string | 否 | 媒体类型：`IMAGE` 或 `VIDEO`，不传则根据模型自动判断 |
| predictType | string | 否 | 生成类型，不传则自动推断。详见[生成类型说明](#%E7%94%9F%E6%88%90%E7%B1%BB%E5%9E%8B) |
| aspectRatio | string | 是 | 画面比例，如 `1:1`、`16:9`、`9:16` 等 |
| resolution | string | 是 | 分辨率，如 `2K`、`4K`（图片）或 `720P`、`1080P`（视频） |
| n | int | 否 | 生成数量，1-4，默认 1 |
| quality | string | 否 | 图片质量档位，仅支持的图片模型生效。可传 `low`、`medium`、`high`，或中文 `低画质`、`标准画质`、`高画质` |
| inputImageList | array | 否 | 参考图片列表，用于图生图、首帧图生视频、首尾帧图生视频、自动视频模式 |
| inputVideoList | array | 否 | 参考视频列表，用于自动视频模式 |
| videoTotalSeconds | int | 否 | 视频时长（秒），仅视频模型有效，默认 5 |
| sound | boolean | 否 | 是否开启声音，仅视频任务有效。不传按后端默认逻辑处理，当前默认 true。部分模型或模式可能忽略该字段 |
| negativePrompt | string | 否 | 反向提示词 |
| seed | int | 否 | 随机种子，默认 -1（随机） |
| optimizePrompt | boolean | 否 | 是否优化提示词，默认 true，建议开启，尤其适合较短或较泛的提示词 |

**inputImageList 中每个元素格式：**

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| imageUrl | string | 是 | 图片 URL（须通过上传接口获取） |
| width | int | **强烈建议** | 图片像素宽度。多数模型（通义万相 2.6 / 2.7、Seedream 4.x / 5.0、MiniMax Hailuo 2.3 等）在参数校验阶段直接读取此字段，缺失会触发服务端 NPE → HTTP 500「系统错误」。客户端应在上传前从本地图片解析后传入 |
| height | int | **强烈建议** | 图片像素高度，要求同 `width` |
| imageId | string | 否 | 资源系统中的图片 ID，可留空 |

**inputVideoList 中每个元素格式：**

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| imageUrl | string | 是 | 视频 URL（字段名沿用 `imageUrl`，须通过上传接口获取） |

> 视频的 duration / width / height / frameRate / fileSize 等元数据由后端通过 OSS 直接探测获取，调用方**无需**在 `inputVideoList` 中传 width / height，仅需传 `imageUrl`。

> 建议大多数场景保持 `optimizePrompt: true`，可以显著改善短提示词、口语化提示词和描述不完整提示词的生成效果。

> `sound` 仅对支持声音控制的视频模型有效。对于带参考视频的某些自动视频模式，`sound` 可能表示“是否保留原视频声音”而不是“是否重新生成声音”，以实际模型实现为准。

#### prompt 中的内联引用（`@imageN` / `@videoN`）

开放平台 API 在 `prompt`(以及 `negativePrompt`)中支持内联占位符，把一段描述绑定到某个具体的参考素材：

- `@image1`、`@image2`…… 对应 `inputImageList` 中第 1、2…… 个元素
- `@video1`、`@video2`…… 对应 `inputVideoList` 中第 1、2…… 个元素
- **不允许空格**：`@image1` ✅，`@image 1` ✗，`@ image1` ✗
- 大小写不敏感：`@Image1` / `@IMAGE1` 等价
- **索引超过实际参考数量时直接返回 HTTP 400**(例如只传了 2 张图却写 `@image5`)
- 服务端会把占位符改写成与对话框协议同形的 `<<<image_N:url>>>` 后再下发,各模型的最终行为如下:
  - **可灵系列**(O1 / V3 Omni / V3 / V2.6 / V2.5 Turbo):原生支持 `<<<image_N>>>` 形式,会按下标绑定到 `image_list` 中对应元素
  - **通义万相 2.6 R2V / Happy Horse 1.0 R2V**:模型内部把占位符替换为 `characterN` 角色 token
  - **其他模型**(Qwen Image / Seedream / Hailuo / Seedance):占位符外壳被剥掉,只剩 `image_N` 文本进入 prompt;没有真正的绑定语义,但人类可读
- **本能力仅对开放平台 API 生效**;网页对话框走自己的富文本 @ 提及通道,无需(也不会)消费此语法

示例(把第 1 张参考图中的人物放进第 1 个参考视频的场景)：

```plaintext
{
  "modelName": "通义万相 2.6",
  "prompt": "把 @image1 中的人物放进 @video1 的场景，保留 @image1 的服装",
  "mediaType": "VIDEO",
  "predictType": "AUTO_VIDEO",
  "aspectRatio": "16:9",
  "resolution": "720P",
  "videoTotalSeconds": 10,
  "inputImageList": [
    { "imageUrl": "https://.../hero.jpg", "width": 1024, "height": 1024 }
  ],
  "inputVideoList": [
    { "imageUrl": "https://.../scene.mp4" }
  ],
  "optimizePrompt": true
}
```

#### 请求示例

**文生图：**

```plaintext
{
  "modelName": "Qwen Image Turbo",
  "prompt": "一只穿着太空服的猫咪在月球上漫步，背景是蓝色地球",
  "mediaType": "IMAGE",
  "aspectRatio": "1:1",
  "resolution": "2K",
  "n": 4,
  "optimizePrompt": true
}
```

**图生图：**

```plaintext
{
  "modelName": "Qwen Image 2.0",
  "prompt": "将这张照片变成水彩画风格",
  "mediaType": "IMAGE",
  "predictType": "REF_2_IMG",
  "aspectRatio": "16:9",
  "resolution": "2K",
  "n": 2,
  "inputImageList": [
    { "imageUrl": "https://your-uploaded-image-url.jpg", "width": 1024, "height": 1024 }
  ]
}
```

**文生视频：**

```plaintext
{
  "modelName": "通义万相 2.2 Turbo",
  "prompt": "海浪拍打着金色的沙滩，夕阳西下",
  "mediaType": "VIDEO",
  "aspectRatio": "16:9",
  "resolution": "720P",
  "videoTotalSeconds": 5,
  "sound": true
}
```

**图生视频（首帧）：**

```plaintext
{
  "modelName": "通义万相 2.6 Flash",
  "prompt": "让画面中的花朵缓缓绽放",
  "mediaType": "VIDEO",
  "predictType": "FF_2_VIDEO",
  "aspectRatio": "16:9",
  "resolution": "720P",
  "videoTotalSeconds": 5,
  "sound": true,
  "inputImageList": [
    { "imageUrl": "https://your-uploaded-image-url.jpg", "width": 1280, "height": 720 }
  ]
}
```

**图生视频（首尾帧）：**

```plaintext
{
  "modelName": "可灵 3.0",
  "prompt": "让镜头从第一帧平滑过渡到最后一帧",
  "mediaType": "VIDEO",
  "predictType": "FLF_2_VIDEO",
  "aspectRatio": "16:9",
  "resolution": "1080P",
  "videoTotalSeconds": 5,
  "inputImageList": [
    { "imageUrl": "https://your-uploaded-start-frame.jpg", "width": 1280, "height": 720 },
    { "imageUrl": "https://your-uploaded-end-frame.jpg", "width": 1280, "height": 720 }
  ]
}
```

**自动视频模式（图片 + 视频参考）：**

```plaintext
{
  "modelName": "可灵 3.0 Omni",
  "prompt": "保留原始动作节奏，同时转成电影感赛博朋克风格",
  "mediaType": "VIDEO",
  "predictType": "AUTO_VIDEO",
  "aspectRatio": "16:9",
  "resolution": "1080P",
  "videoTotalSeconds": 10,
  "sound": false,
  "inputImageList": [
    { "imageUrl": "https://your-uploaded-style-reference.jpg", "width": 1280, "height": 720 }
  ],
  "inputVideoList": [
    { "imageUrl": "https://your-uploaded-source-video.mp4" }
  ]
}
```

#### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| recordId | string | 任务记录 ID，用于后续查询 |
| credit | object | 积分消耗信息 |
| credit.modelGroup | string | 模型分组名 |
| credit.previousFreeUsage | int | 消耗前剩余免费次数 |
| credit.currentFreeUsage | int | 消耗后剩余免费次数 |

#### 响应示例

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "recordId": "01JWXYZ...",
    "credit": {
      "modelGroup": "IMAGE_DEFAULT",
      "previousFreeUsage": 10,
      "currentFreeUsage": 6
    }
  }
}
```
---

### 2. 查询任务状态

```plaintext
GET /api/v1/platform/predict/query?recordId={recordId}
```

根据 `recordId` 查询任务状态和生成结果。建议以 2-5 秒间隔轮询，直到状态为终态。

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| recordId | string | 是 | 提交任务时返回的记录 ID |

#### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| recordId | string | 记录 ID |
| recordStatus | string | 任务整体状态，见[任务状态说明](#%E4%BB%BB%E5%8A%A1%E7%8A%B6%E6%80%81) |
| gmtCreate | string | 创建时间 |
| mediaType | string | `IMAGE` 或 `VIDEO` |
| modelInfo | object | 模型信息 |
| modelInfo.modelName | string | 模型名称 |
| genInfo | object | 生成参数信息 |
| genInfo.prompt | string | 提示词 |
| genInfo.predictType | string | 生成类型 |
| genInfo.aspectRatio | string | 画面比例 |
| genInfo.resolution | string | 分辨率 |
| genInfo.width | int | 宽度（像素） |
| genInfo.height | int | 高度（像素） |
| genInfo.videoTotalSeconds | int | 视频时长（秒） |
| genInfo.sound | boolean | 是否开启声音 |
| results | array | 生成结果列表 |
| results.taskId | string | 子任务 ID |
| results.imageId | string | 资源 ID |
| results.imageUrl | string | 结果图片/视频 URL（带水印） |
| results.status | string | 子任务状态 |
| results.progress | int | 进度百分比 |
| results.errorMsg | string | 错误信息 |
| results.star | int | 收藏状态 |

#### 响应示例

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "recordId": "01JWXYZ...",
    "recordStatus": "SUCCEED",
    "gmtCreate": "2026-03-11T10:30:00.000+08:00",
    "mediaType": "IMAGE",
    "modelInfo": {
      "modelName": "Qwen Image Turbo"
    },
    "genInfo": {
      "prompt": "一只穿着太空服的猫咪在月球上漫步",
      "predictType": "TXT_2_IMG",
      "aspectRatio": "1:1",
      "resolution": "2K",
      "width": 1024,
      "height": 1024,
      "optimizePrompt": true
    },
    "results": [
      {
        "taskId": "01JWABC...",
        "imageId": "01JWDEF...",
        "imageUrl": "https://cdn.wuli.art/result/xxx.png",
        "status": "SUCCEED",
        "progress": 100,
        "star": 0
      }
    ]
  }
}
```
---

### 3. 获取无水印图片/视频

```plaintext
POST /api/v1/platform/predict/noWatermarkImage
```

获取生成结果的无水印版本 URL。

> **重要：**需要先在网页端开启「去除品牌水印」，并在设置中开启「去除水印」，才可拿到左上角和右下角都没有水印的图片/视频。

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| taskId | string | 否 | 子任务 ID |
| resourceId | string | 否 | 资源 ID |
| resourceIdList | array | 否 | 资源 ID 列表（批量获取） |

> 三个参数至少传一个。

#### 请求示例

```plaintext
{
  "taskId": "01JWABC..."
}
```

或批量获取：

```plaintext
{
  "resourceIdList": ["01JWDEF...", "01JWGHI..."]
}
```

#### 响应示例

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "url": "https://cdn.wuli.art/result/xxx\_nowatermark.png",
    "urlList": [
      "https://cdn.wuli.art/result/xxx1\_nowatermark.png",
      "https://cdn.wuli.art/result/xxx2\_nowatermark.png"
    ]
  }
}
```
---

### 4. 获取预签名上传 URL

```plaintext
GET /api/v1/platform/image/getUploadUrl?filename={filename}
```

获取 OSS 预签名上传 URL，用于上传参考图片或视频。上传成功后，将 `uploadUrl` 去掉签名参数后的公网 URL 用作 `inputImageList` / `inputVideoList` 中的 `imageUrl` 字段值。

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| filename | string | 是 | 文件名（含后缀），如 `photo.jpg`、`clip.mp4` |

支持的图片格式：`jpg`、`jpeg`、`png`、`webp` 支持的视频格式：`mp4`、`mov`、`avi`、`webm`

#### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uploadUrl | string | 预签名上传 URL，使用 `PUT` 方法上传文件，有效期 1 小时 |
| objectName | string | 文件对象名（仅供参考） |

#### 响应示例

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "uploadUrl": "https://oss.aliyuncs.com/wuli/xxx?签名参数...",
    "objectName": "upload/2026/03/11/abc123.jpg"
  }
}
```

#### 使用流程

1.  调用本接口获取 `uploadUrl` 和 `objectName`
    
2.  使用 `PUT` 方法将文件二进制数据上传到 `uploadUrl`，请求头必须设置 `Content-Type: application/octet-stream`
    
3.  将 `uploadUrl` 去掉查询参数（`?Expires=...` 部分）后的基础 URL 作为 `inputImageList[].imageUrl` 或 `inputVideoList[].imageUrl` 的值传入生成接口
    

#### 上传文件到预签名 URL

获取到 `uploadUrl` 后，需要通过 HTTP `PUT` 请求将文件内容上传。以下是具体的上传方式：

**curl 示例（上传本地图片）：**

```bash
# 1. 获取预签名上传 URL
UPLOAD_RESP=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  "https://platform.wuli.art/api/v1/platform/image/getUploadUrl?filename=photo.jpg")

UPLOAD_URL=$(echo $UPLOAD_RESP | jq -r '.data.uploadUrl')

# 2. PUT 上传文件（Content-Type 必须为 application/octet-stream）
curl -X PUT \
  -H "Content-Type: application/octet-stream" \
  --data-binary @photo.jpg \
  "$UPLOAD_URL"

# 3. 去掉签名参数，得到公网 URL 用于后续生成任务
PUBLIC_URL=$(echo "$UPLOAD_URL" | cut -d'?' -f1)
echo "公网 URL: $PUBLIC_URL"
```

**curl 示例（上传本地视频）：**

```bash
UPLOAD_RESP=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  "https://platform.wuli.art/api/v1/platform/image/getUploadUrl?filename=clip.mp4")

UPLOAD_URL=$(echo $UPLOAD_RESP | jq -r '.data.uploadUrl')

curl -X PUT \
  -H "Content-Type: application/octet-stream" \
  --data-binary @clip.mp4 \
  "$UPLOAD_URL"

PUBLIC_URL=$(echo "$UPLOAD_URL" | cut -d'?' -f1)
```

**Python 示例（上传本地文件）：**

```python
import urllib.parse
import urllib.request
import json
from pathlib import Path

API_BASE = "https://platform.wuli.art/api/v1/platform"
TOKEN = "wuli-a1b2c3d4e5f6..."

def upload_file(file_path, token):
    path = Path(file_path)
    filename = path.name
    encoded_filename = urllib.parse.quote(filename)

    # Step 1: 获取预签名上传 URL
    req = urllib.request.Request(
        f"{API_BASE}/image/getUploadUrl?filename={encoded_filename}"
    )
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    upload_url = result["data"]["uploadUrl"]

    # Step 2: PUT 上传文件（Content-Type 必须为 application/octet-stream）
    file_data = path.read_bytes()
    put_req = urllib.request.Request(upload_url, data=file_data, method="PUT")
    put_req.add_header("Content-Type", "application/octet-stream")
    with urllib.request.urlopen(put_req, timeout=120) as _:
        pass

    # Step 3: 去掉查询参数，得到公网 URL
    parsed = urllib.parse.urlparse(upload_url)
    public_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return public_url

# 上传图片并用于图生图
image_url = upload_file("photo.jpg", TOKEN)
# 上传视频并用于视频生视频
video_url = upload_file("clip.mp4", TOKEN)
```

**Python 示例（下载远程图片后重新上传到 OSS）：**

如果参考图片来自第三方 URL，需要先下载再上传到呜哩 OSS：

```python
def upload_remote_image(image_url, token):
    # Step 1: 下载远程图片
    req = urllib.request.Request(image_url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        image_data = resp.read()

    # 从 URL 路径推断文件扩展名
    url_path = urllib.parse.urlparse(image_url).path
    ext = ".jpg"
    if "." in url_path.split("/")[-1]:
        ext = "." + url_path.split("/")[-1].rsplit(".", 1)[-1].lower()

    filename = f"upload{ext}"
    encoded_filename = urllib.parse.quote(filename)

    # Step 2: 获取预签名上传 URL
    req = urllib.request.Request(
        f"{API_BASE}/image/getUploadUrl?filename={encoded_filename}"
    )
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    upload_url = result["data"]["uploadUrl"]

    # Step 3: PUT 上传到 OSS
    put_req = urllib.request.Request(upload_url, data=image_data, method="PUT")
    put_req.add_header("Content-Type", "application/octet-stream")
    with urllib.request.urlopen(put_req, timeout=120) as _:
        pass

    # Step 4: 去掉查询参数，得到公网 URL
    parsed = urllib.parse.urlparse(upload_url)
    public_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return public_url
```
> **注意事项：**

*   上传时 `Content-Type` 必须设置为 `application/octet-stream`，不要使用 `multipart/form-data` 或文件的实际 MIME 类型
    
*   `uploadUrl` 有效期为 1 小时，请及时上传
    
*   上传完成后，需将 `uploadUrl` 去掉 `?` 及其后面的签名参数部分，得到的基础 URL 才能作为 `inputImageList[].imageUrl` 或 `inputVideoList[].imageUrl` 使用
    
*   支持的图片格式：`jpg`、`jpeg`、`png`、`webp`；支持的视频格式：`mp4`、`mov`、`avi`、`webm`
    
*   第三方 URL 的图片/视频不能直接用于生成任务，必须先上传到呜哩 OSS 获取公网 URL
    

---

## 可用模型

### 图片生成模型

| 模型名称 (modelName) | 支持的生成类型 | 支持的分辨率 | 最大生成数 | 最大参考图数 | 每张积分消耗 |
| --- | --- | --- | --- | --- | --- |
| 智能IMAGE 2 | TXT_2_IMG, REF_2_IMG | 1K, 2K, 4K | 4 | 4 | 质量档位计费：1K=1/7/26，2K=2/13/51，4K=4/16/56 |
| 全能图片 2 | TXT_2_IMG, REF_2_IMG | 1K, 2K, 4K | 4 | 4 | 1K=9，2K=13，4K=20 |
| 全能图片 Pro | TXT_2_IMG, REF_2_IMG | 1K, 2K, 4K | 4 | 4 | 1K/2K=4，4K=5 |
| 通义万相 2.7 | TXT_2_IMG, REF_2_IMG | 2K, 4K | 4 | 9 | 2K=1，4K=3 |
| Qwen Image 2.0 | TXT_2_IMG, REF_2_IMG | 2K, 4K | 4 | 4 | 1 |
| Qwen Image Turbo | TXT_2_IMG, REF_2_IMG | 2K, 4K | 4 | 4 | 1 |
| Seedream 5.0 Lite | TXT_2_IMG, REF_2_IMG | 2K, 3K | 4 | 8 | 4 |
| Seedream 4.5 | TXT_2_IMG, REF_2_IMG | 2K, 4K | 4 | 8 | 4 |
| Seedream 4.0 | TXT_2_IMG, REF_2_IMG | 1K, 2K, 4K | 4 | 8 | 4 |

> 当前默认推荐接入以上图片模型。`Qwen Image 25.08`、`Qwen Image 25.11`、`Qwen Image 25.12`、`通义万相 2.6` 图片模型在配置中仍保留兼容信息，但不作为当前默认接入模型。

#### 图片画面比例

| aspectRatio | 说明 |
| --- | --- |
| 1:1 | 正方形 |
| 4:3 | 横向 4:3 |
| 5:4 | 横向 5:4 |
| 3:2 | 横向 3:2 |
| 2:1 | 横向 2:1 |
| 16:9 | 宽屏横向 |
| 21:9 | 超宽横向 |
| 4:1 | 极宽横向 |
| 3:4 | 纵向 3:4 |
| 4:5 | 纵向 4:5 |
| 2:3 | 纵向 2:3 |
| 1:2 | 纵向 1:2 |
| 9:16 | 竖屏纵向 |
| 9:21 | 超高纵向 |
| 1:4 | 极高纵向 |

---

### 视频生成模型

| 模型名称 (modelName) | 支持的生成类型 | 支持的分辨率 | 支持的时长(秒) | 最大参考图数 | 最大参考视频数 | 支持声音开关 | 默认声音行为 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通义万相 2.7 | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO, AUTO\_VIDEO | 720P, 1080P | 5, 10, 15（AUTO\_VIDEO 仅 5, 10） | 2（AUTO\_VIDEO 为 5） | 3（AUTO\_VIDEO） | 否 | 以模型实际返回为准 |
| Happy Horse 1.1 | TXT_2_VIDEO, FF_2_VIDEO, AUTO\_VIDEO | 720P, 1080P | 5, 10, 15 | 1（AUTO\_VIDEO 为 9） | 0 | 是 | 默认开启 |
| Happy Horse 1.0 | TXT_2_VIDEO, FF_2_VIDEO, AUTO\_VIDEO | 720P, 1080P | 3-15（积分按 5/10/15 档） | 1（AUTO\_VIDEO 为 9） | 1（AUTO\_VIDEO） | 是 | 默认开启；有参考视频时可选择保留原声 |
| 通义万相 2.2 Turbo | TXT_2_VIDEO, FF_2_VIDEO | 720P | 5 | 1 | 0 | 否 | 无音频输出 |
| 通义万相 2.6 Flash | FF_2_VIDEO | 720P, 1080P | 5, 10, 15 | 1 | 0 | 否（当前实现固定开启） | 默认带音频 |
| 通义万相 2.6 | TXT_2_VIDEO, FF_2_VIDEO, AUTO\_VIDEO | 720P, 1080P | 5, 10, 15（AUTO\_VIDEO 为 5, 10） | 2（AUTO\_VIDEO 为 5） | 3（AUTO\_VIDEO） | 部分支持 | `AUTO_VIDEO` 可控；`FF_2_VIDEO` 当前固定带音频；其余模式以模型实际返回为准 |
| 可灵 3.0 Omni | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO, AUTO\_VIDEO | 720P, 1080P | 5, 10, 15 | 7 | 1 | 是 | 无参考视频时默认开启；有参考视频时默认保留原声 |
| 可灵 O1 | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO, AUTO\_VIDEO | 720P, 1080P | 5, 10 | 7 | 1 | 是 | 无参考视频时默认开启；有参考视频时默认保留原声 |
| 可灵 3.0 | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 720P, 1080P | 5, 10, 15 | 2 | 0 | 是 | 默认开启 |
| 可灵 2.6 | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 1080P | 5, 10 | 2 | 0 | 是 | 默认开启 |
| 可灵 2.5 Turbo | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 1080P | 5, 10 | 2 | 0 | 是 | 默认开启 |
| Seedance 1.5 Pro | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 480P, 720P | 5, 10, 12 | 2 | 0 | 是 | 默认开启 |
| Seedance 1.0 Pro | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 480P, 720P, 1080P | 5, 10 | 2 | 0 | 是 | 默认开启 |
| MiniMax Hailuo 2.3 | TXT_2_VIDEO, FF_2_VIDEO | 768P, 1080P | 6, 10 | 1 | 0 | 否 | 无音频输出 |
| MiniMax Hailuo 2.3 Fast | FF_2_VIDEO | 768P, 1080P | 6, 10 | 1 | 0 | 否 | 无音频输出 |

> 当前默认推荐接入以上视频模型。`智能模型`、`Wan 2.2 Turbo` 等隐藏模型在配置中保留兼容信息，但不作为当前默认接入模型。

> “支持声音开关”表示当前 API 请求里的 `sound` 字段是否会参与该模型/模式的后端转换逻辑，不等同于网页端是否已经开放对应 UI。

> 未传 `sound` 时，后端当前默认按 `true` 处理；但某些模型/模式会固定带音频、固定无音频，或在带参考视频时将其解释为“是否保留原视频声音”。

> 对支持音频控制的模型，关闭 `sound` 后可能命中更低的积分档位；对带参考视频的自动视频模式，还可能命中视频编辑相关积分档位。

#### 视频积分消耗

视频积分根据模型、分辨率、时长和生成类型不同而不同，以下为当前模型配置对应的积分参考：

**通义万相 2.7（TXT**_2_VIDEO / FF_2_VIDEO / FLF_2_VIDEO）

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 40 | 80 | 120 |
| 1080P | 60 | 120 | 180 |

**通义万相 2.7（AUTO\_VIDEO）**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 720P | 40 | 80 |
| 1080P | 60 | 120 |

**Happy Horse 1.1**

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 60 | 120 | 180 |
| 1080P | 70 | 140 | 210 |

**Happy Horse 1.0**

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 60 | 120 | 180 |
| 1080P | 100 | 200 | 300 |

**通义万相 2.2 Turbo**

| 分辨率 | 5秒 |
| --- | --- |
| 720P | 20 |

**通义万相 2.6 Flash**

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 20 | 40 | 60 |
| 1080P | 40 | 80 | 120 |

**通义万相 2.6（TXT**_2_VIDEO / FF_2_VIDEO）

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 40 | 80 | 120 |
| 1080P | 60 | 120 | 180 |

**通义万相 2.6（AUTO\_VIDEO）**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 720P | 40 | 80 |
| 1080P | 60 | 120 |

**可灵 3.0 Omni（TXT**_2_VIDEO / FF_2_VIDEO / FLF_2_VIDEO）

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 60 | 120 | 180 |
| 1080P | 80 | 160 | 240 |

**可灵 3.0 Omni（AUTO\_VIDEO）**

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 80 | 160 | 180 |
| 1080P | 100 | 200 | 240 |

**可灵 O1（TXT**_2_VIDEO / FF_2_VIDEO / FLF_2_VIDEO）

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 720P | 40 | 80 |
| 1080P | 60 | 100 |

**可灵 O1（AUTO\_VIDEO）**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 720P | 60 | 120 |
| 1080P | 80 | 160 |

**可灵 3.0**

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 80 | 160 | 240 |
| 1080P | 100 | 200 | 300 |

**可灵 2.6**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 1080P | 60 | 120 |

**可灵 2.5 Turbo**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 1080P | 40 | 80 |

**Seedance 1.5 Pro**

| 分辨率 | 5秒 | 10秒 | 12秒 |
| --- | --- | --- | --- |
| 480P | 20 | 40 | 60 |
| 720P | 40 | 80 | 100 |

**Seedance 1.0 Pro**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 480P | 20 | 40 |
| 720P | 40 | 80 |
| 1080P | 80 | 160 |

**MiniMax Hailuo 2.3**

| 分辨率 | 6秒 | 10秒 |
| --- | --- | --- |
| 768P | 40 | 80 |
| 1080P | 60 | 100 |

**MiniMax Hailuo 2.3 Fast**

| 分辨率 | 6秒 | 10秒 |
| --- | --- | --- |
| 768P | 20 | 40 |
| 1080P | 40 | 40 |

#### 视频画面比例

| aspectRatio | 说明 |
| --- | --- |
| 1:1 | 正方形 |
| 4:3 | 横向 4:3 |
| 3:4 | 纵向 3:4 |
| 16:9 | 宽屏横向 |
| 9:16 | 竖屏纵向 |

> 不同模型支持的画面比例可能不同，请以实际模型配置为准。

---

## 生成类型

| predictType | 说明 | 适用场景 |
| --- | --- | --- |
| TXT_2_IMG | 文生图 | 纯文本提示词生成图片 |
| REF_2_IMG | 图生图 | 一张或多张参考图片 + 提示词生成图片 |
| TXT_2_VIDEO | 文生视频 | 纯文本提示词生成视频 |
| FF_2_VIDEO | 图生视频（首帧） | 单张参考图 + 提示词生成视频 |
| FLF_2_VIDEO | 图生视频（首尾帧） | 首尾两张参考图 + 提示词生成视频 |
| AUTO\_VIDEO | 自动视频模式 | 参考图片、参考视频或混合参考素材 + 提示词生成视频 |

> 历史配置中的 `MULTI_IMG_2_VIDEO`、`VIDEO_2_VIDEO` 等能力，在当前对外模型配置中统一归入 `AUTO_VIDEO` 模式说明。

---

## 任务状态

| 状态 (status) | 说明 | 是否终态 |
| --- | --- | --- |
| INITIALIZING | 初始化中 | 否 |
| OPTIMIZING | 提示词优化中 | 否 |
| PENDING | 排队等待中 | 否 |
| PROCESSING | 生成中 | 否 |
| SUCCEED | 生成成功 | 是 |
| FAILED | 生成失败 | 是 |
| REVIEWFAILED | 内容审核不通过 | 是 |
| TIMEOUT | 任务超时 | 是 |
| CANCELLED | 已取消 | 是 |

---

## 错误码

| code | 说明 |
| --- | --- |
| 200 | 成功 |
| 401 | 未认证，Token 无效或缺失 |
| 403 | 无权限 |
| 429 | 请求频率过高 |
| 1001 | 参数错误 |
| 2001 | 积分余额不足 |
| 5000 | 服务内部错误 |

### 常见错误：HTTP 500「系统错误」

如果 `predict/submit` 返回 HTTP 500（消息为「系统错误，请稍后重试」），最常见的原因是 `inputImageList` 中漏传了 `width` / `height`。
通义万相 2.6 / 2.7、Seedream 4.x / 5.0、MiniMax Hailuo 2.3 等模型的参数校验器会直接读取这两个字段进行尺寸 / 宽高比校验，缺失会触发 NPE。
**请在客户端解析图片像素宽高后再随 `inputImageList` 一起提交。**

---

## 典型调用流程

```plaintext
1. 上传参考素材（如需要）
   GET /api/v1/platform/image/getUploadUrl?filename=ref.jpg
   → PUT 上传文件到返回的 uploadUrl（需加 Content-Type: application/octet-stream 请求头）
   → 将 uploadUrl 去掉签名参数后的公网 URL 作为图片/视频引用
2. 提交生成任务
   POST /api/v1/platform/predict/submit
   → 获得 recordId

3. 轮询任务状态（建议间隔 2~5 秒）
   GET /api/v1/platform/predict/query?recordId=xxx
   → 直到 recordStatus 为终态 (SUCCEED / FAILED / ...)

4. 获取无水印图片/视频（可选）
   重要：需要先在网页端开启「去除品牌水印」，并在设置中开启「去除水印」，才可拿到左上角和右下角都没有水印的图片/视频。
   POST /api/v1/platform/predict/noWatermarkImage
   → 获得无水印 URL
```
