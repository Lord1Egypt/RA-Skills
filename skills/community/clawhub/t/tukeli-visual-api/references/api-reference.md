# API 参考文档 — 图可丽视觉 API

> **重要**：图可丽 API 的请求域名为 `https://picupapi.tukeli.net`，与官网域名 `www.tukeli.net` 不同，请勿混淆。

## 目录

1. [认证方式](#认证方式)
2. [通用抠图 API](#通用抠图-api)
3. [人脸变清晰 API](#人脸变清晰-api)
4. [AI背景更换 API](#ai背景更换-api)
5. [通用参数说明](#通用参数说明)
6. [响应格式](#响应格式)
7. [错误码](#错误码)

---

## 认证方式

所有请求必须在 Header 中携带 `APIKEY`：

```
APIKEY: 你的专属API Key
```

API 基础域名：`https://picupapi.tukeli.net`

---

## 通用抠图 API

自动识别图像中主体轮廓，与背景进行分离，返回透明 PNG。支持人像、物体、头像等多种类型，适应复杂背景和光线。

### mattingType 类型说明

| 值 | 说明 |
|----|------|
| `1` | 人像抠图（发丝级精度，适合证件照、电商服饰等）|
| `2` | 物体抠图（商品、宠物、箱包等）|
| `3` | 头像抠图（头部+头发区域）|
| `6` | 通用抠图（默认，适应多物体、复杂背景）|

### POST /api/v1/matting（二进制响应）

**请求说明**
- 请求方式：POST
- 返回类型：PNG 图像（二进制）

**Header 参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `Content-Type` | string | `multipart/form-data` |
| `APIKEY` | string | 您的专属 API Key |

**Body 参数（URL 参数附加在 URL 后面）**

| 参数 | 必填 | 说明 |
|------|------|------|
| `file` | 是 | 图片文件 |
| `mattingType` | 是（URL参数）| 抠图类型：1/2/3/6（默认6）|
| `crop` | 否（URL参数）| 是否裁剪至最小非透明区域，`true` 裁剪，`false` 或不填不裁剪 |
| `bgcolor` | 否（URL参数）| 填充背景色，十六进制 RGB，如 `FFFFFF`，不填则透明 |
| `outputFormat` | 否（URL参数）| 输出格式：`png`、`webp`、`jpg_$quality`（如 `jpg_75`），默认 `png` |

**响应**：直接返回 `Content-Type: image/png`，图片处理后的二进制文件。

### POST /api/v1/matting2（Base64 响应）

同上，额外支持：

| 参数 | 必填 | 说明 |
|------|------|------|
| `faceAnalysis` | 否（URL参数）| 为 `true` 时返回人脸关键点信息 |

**响应（含人脸关键点）**：
```json
{
  "code": 0,
  "data": {
    "imageBase64": "iVBORw0KGgo...",
    "faceAnalysis": {
      "face_num": 1,
      "faces": [
        [236.46, 497.67, 1492.75, 2050.21, 236.46, 497.67, 1492.75, 2050.21]
      ],
      "point": [
        [
          [213.59, 1035.07],
          [221.80, 1219.90]
        ]
      ]
    }
  },
  "msg": null,
  "time": 1620798570850
}
```

> `faces` 数组坐标顺序：p1(x,y), p3(x,y), p2(x,y), p4(x,y)（人脸框四角）
> `point` 数组共返回 68 个关键点坐标

### GET /api/v1/mattingByUrl（图片URL模式）

**Header 参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `APIKEY` | string | 您的专属 API Key |

**URL 参数**

| 参数 | 必填 | 说明 |
|------|------|------|
| `mattingType` | 是 | 抠图类型：1/2/3/6 |
| `url` | 是 | 图片的 URL 地址 |
| `crop` | 否 | 是否裁剪 |
| `bgcolor` | 否 | 背景颜色 |
| `faceAnalysis` | 否 | 是否返回人脸关键点 |
| `outputFormat` | 否 | 输出格式 |

**响应**：返回 JSON，格式同 `/api/v1/matting2`。

### 计费规则

- 图片 15M 以下：每次成功调用消耗 **1 点**
- 图片 15M~25M：每次成功调用消耗 **2 点**

---

## 人脸变清晰 API

AI 增强人脸清晰度，将模糊、低分辨率、像素化的人脸照片转为高清图。

### POST /api/v1/matting（二进制响应）

**请求说明**
- 请求 URL：`https://picupapi.tukeli.net/api/v1/matting?mattingType=18`
- 请求方式：POST
- 返回类型：PNG 图像（二进制）

**Header 参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `Content-Type` | string | `multipart/form-data` |
| `APIKEY` | string | 您的专属 API Key |

**Body 参数**

| 参数 | 必填 | 说明 |
|------|------|------|
| `file` | 是 | 图片文件 |

**响应**：直接返回 `Content-Type: image/png`，图片处理后的二进制文件。

### POST /api/v1/matting2（Base64 响应）

- 请求 URL：`https://picupapi.tukeli.net/api/v1/matting2?mattingType=18`
- 参数同上

**响应**：
```json
{
  "code": 0,
  "data": {
    "imageBase64": "iVBORw0KGgo..."
  },
  "msg": null,
  "time": 1590462453264
}
```

### GET /api/v1/mattingByUrl（图片URL模式）

- 请求 URL：`https://picupapi.tukeli.net/api/v1/mattingByUrl`
- 请求方式：GET

**URL 参数**

| 参数 | 必填 | 说明 |
|------|------|------|
| `mattingType` | 是 | 固定值：`18` |
| `url` | 是 | 图片的 URL 地址 |

### 计费规则

- 每次成功调用消耗 **2 点**

### 支持格式

- PNG、JPG、JPEG、BMP、WEBP
- 最大分辨率：4096×4096 像素
- 最大文件大小：15 MB

---

## AI背景更换 API

根据文字描述，自动对输入图片的透明区域进行 AI 扩展，生成新背景。

> **注意**：此接口为**异步接口**，需要先提交任务获取 `taskId`，再轮询查询结果。

### 提交任务：POST /api/v1/paintAsync

**请求说明**
- 请求 URL：`https://picupapi.tukeli.net/api/v1/paintAsync`
- 请求方式：POST
- 返回类型：JSON

**Header 参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `APIKEY` | string | 您的专属 API Key |

**Body 参数（JSON）**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `imgUrl` | string | 条件必填 | 输入图片地址（与 `imgBase64` 至少填一个）|
| `imgBase64` | string | 条件必填 | 图片的 Base64 编码字符串（与 `imgUrl` 至少填一个）|
| `text` | string | 是 | 想要生成的图片背景描述 |

**响应**：
```json
{
  "code": 0,
  "data": 12345,
  "msg": null,
  "time": 1599644436677
}
```

> `data` 字段为任务 ID（`taskId`），用于后续查询结果。

### 查询结果：GET /api/v1/getPaintResult

**请求说明**
- 请求 URL：`https://picupapi.tukeli.net/api/v1/getPaintResult`
- 请求方式：GET
- 返回类型：JSON

**Header 参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `APIKEY` | string | 您的专属 API Key |

**URL 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `taskId` | number | 是 | 提交任务时返回的任务 ID |

**响应**：
```json
{
  "code": 0,
  "data": {
    "id": 1234,
    "percentage": 65,
    "status": 1,
    "resultUrl": "https://xxxx"
  },
  "msg": null,
  "time": 1599644436677
}
```

**status 状态说明**

| 值 | 说明 |
|----|------|
| `0` | 生成中 |
| `1` | 已完成（`resultUrl` 为结果图临时链接，5分钟后失效）|
| `2` | 处理失败 |
| `3` | 排队中 |

### 计费规则（按分辨率）

| 宽高分辨率 | 消耗点数 |
|-----------|---------|
| ≤ 512×512 | 3 点/次 |
| 512×512 ~ 1024×1024 | 6 点/次 |
| 1024×1024 ~ 1920×1080 | 12 点/次 |

---

## 通用参数说明

### outputFormat

| 值 | 说明 |
|----|------|
| `png` | 无损，支持透明（默认）|
| `webp` | 现代格式，文件更小 |
| `jpg_$quality` | JPEG 压缩，quality 为 0~100，如 `jpg_75` |

### bgcolor

| 值 | 说明 |
|----|------|
| 十六进制颜色码 | 如 `FFFFFF`（白色）、`000000`（黑色）|
| 不填 | 透明背景（默认）|

---

## 响应格式

### 成功（二进制模式）
- `Content-Type: image/png`（或 webp/jpeg）
- Body：图片二进制数据

### 成功（Base64 模式）
```json
{
  "code": 0,
  "data": {
    "imageBase64": "base64编码的图片数据"
  },
  "msg": null,
  "time": 1590462453264
}
```

### 错误响应
```json
{
  "code": 1001,
  "data": null,
  "msg": "余额不足",
  "time": 1590462453264
}
```

---

## 错误码

| 错误码 | 说明 | 处理建议 |
|--------|------|---------|
| `0` | 成功 | — |
| `1001` | 余额不足 | 充值点数 |
| `1002` | API Key 无效 | 检查密钥是否正确 |
| `1003` | 不支持的图片格式 | 使用 PNG/JPG/JPEG/BMP/GIF |
| `1004` | 图片分辨率超限 | 缩小至 4096×4096 以内 |
| `1005` | 文件大小超限 | 压缩至 25MB 以内（抠图）或 15MB 以内（人脸变清晰）|

---

## 请求示例

### curl（通用抠图，文件上传，二进制响应）
```bash
curl -H 'APIKEY: INSERT_YOUR_API_KEY_HERE' \
     -F 'file=@/path/to/file.jpg' \
     -f 'https://picupapi.tukeli.net/api/v1/matting?mattingType=6&crop=true' \
     -o out.png
```

### curl（通用抠图，Base64 响应）
```bash
curl -H 'APIKEY: INSERT_YOUR_API_KEY_HERE' \
     -F 'file=@/path/to/file.jpg' \
     -f 'https://picupapi.tukeli.net/api/v1/matting2?mattingType=6&crop=true'
```

### curl（人脸变清晰，Base64 响应）
```bash
curl -H 'APIKEY: INSERT_YOUR_API_KEY_HERE' \
     -F 'file=@/path/to/file.jpg' \
     -f 'https://picupapi.tukeli.net/api/v1/matting2?mattingType=18'
```

### Python（通用抠图，二进制响应）
```python
import requests

response = requests.post(
    'https://picupapi.tukeli.net/api/v1/matting?mattingType=6',
    files={'file': open('/path/to/file.jpg', 'rb')},
    headers={'APIKEY': 'INSERT_YOUR_API_KEY_HERE'},
)
with open('out.png', 'wb') as f:
    f.write(response.content)
```

### Python（人脸变清晰，Base64 响应）
```python
import requests

response = requests.post(
    'https://picupapi.tukeli.net/api/v1/matting2?mattingType=18',
    files={'file': open('/path/to/file.jpg', 'rb')},
    headers={'APIKEY': 'INSERT_YOUR_API_KEY_HERE'},
)
data = response.json()
image_base64 = data['data']['imageBase64']
```

### Python（AI背景更换，提交任务）
```python
import requests

# 提交任务
response = requests.post(
    'https://picupapi.tukeli.net/api/v1/paintAsync',
    json={
        'imgUrl': 'https://example.com/transparent.png',
        'text': '美丽的海滩背景，阳光明媚'
    },
    headers={'APIKEY': 'INSERT_YOUR_API_KEY_HERE'},
)
task_id = response.json()['data']
print(f'任务ID: {task_id}')
```

### Python（AI背景更换，查询结果）
```python
import requests, time

task_id = 12345  # 提交任务时返回的ID

while True:
    response = requests.get(
        'https://picupapi.tukeli.net/api/v1/getPaintResult',
        params={'taskId': task_id},
        headers={'APIKEY': 'INSERT_YOUR_API_KEY_HERE'},
    )
    data = response.json()['data']
    status = data['status']
    if status == 1:
        print(f'完成！结果图：{data["resultUrl"]}')
        break
    elif status == 2:
        print('处理失败')
        break
    else:
        print(f'处理中... {data.get("percentage", 0)}%')
        time.sleep(3)
```
