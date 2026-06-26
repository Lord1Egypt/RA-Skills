# MiniMax 文生图 API 参考

## 基础信息

- **API 地址**: `https://api.minimaxi.com/v1/image_generation`
- **认证**: Bearer Token (HTTP Bearer Auth)
- **API Key 获取**: [MiniMax 平台 - 接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key)

## 请求头

| Header | 必填 | 说明 |
|--------|------|------|
| `Content-Type` | 是 | `application/json` |
| `Authorization` | 是 | `Bearer {API_KEY}` |

## 请求体 (ImageGenerationReq)

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `model` | string | 是 | - | 模型名称：`image-01` 或 `image-01-live` |
| `prompt` | string | 是 | - | 图片文本描述，最长 1500 字符 |
| `style` | object | 否 | - | 画风设置，**仅 `image-01-live` 支持** |
| `aspect_ratio` | string | 否 | `1:1` | 宽高比 |
| `width` | integer | 否 | - | 图片宽度 [512, 2048]，需是 8 的倍数 |
| `height` | integer | 否 | - | 图片高度 [512, 2048]，需是 8 的倍数 |
| `response_format` | string | 否 | `url` | 返回格式：`url` 或 `base64` |
| `seed` | integer | 否 | - | 随机种子，用于复现结果 |
| `n` | integer | 否 | 1 | 生成图片数量 [1, 9] |
| `prompt_optimizer` | boolean | 否 | false | 是否开启 prompt 自动优化 |
| `aigc_watermark` | boolean | 否 | false | 是否添加水印 |

### 宽高比 (aspect_ratio)

| 值 | 分辨率 |
|----|--------|
| `1:1` | 1024x1024 |
| `16:9` | 1280x720 |
| `4:3` | 1152x864 |
| `3:2` | 1248x832 |
| `2:3` | 832x1248 |
| `3:4` | 864x1152 |
| `9:16` | 720x1280 |
| `21:9` | 1344x576 (仅 `image-01`) |

### 画风类型 (style_type)

**仅 `image-01-live` 模型支持：**

| 值 | 说明 |
|----|------|
| `漫画` | 漫画风格 |
| `元气` | 元气/活力风格 |
| `中世纪` | 中世纪风格 |
| `水彩` | 水彩画风格 |

## 响应体 (ImageGenerationResp)

```json
{
  "data": {
    "image_urls": ["https://..."],
    "image_base64": ["..."]
  },
  "metadata": {
    "success_count": 3,
    "failed_count": 0
  },
  "id": "03ff3cd0820949eb8a410056b5f21d38",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

## 错误码 (status_code)

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1002 | 触发限流，请稍后再试 |
| 1004 | 账号鉴权失败，请检查 API_KEY |
| 1008 | 账号余额不足 |
| 1026 | 图片描述涉及敏感内容 |
| 2013 | 参数异常，请检查入参 |
| 2049 | 无效的 API Key |

## 使用示例

### 示例 1: 基本文生图

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

response = requests.post(
    "https://api.minimaxi.com/v1/image_generation",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "image-01",
        "prompt": "一只可爱的小老虎，毛绒绒的，大眼睛，温暖友好的氛围，高质量插画风格",
        "aspect_ratio": "1:1",
        "n": 1,
        "response_format": "url"
    }
)

result = response.json()
image_url = result["data"]["image_urls"][0]
print(f"生成的图片: {image_url}")
```

### 示例 2: 带风格的图片生成

```python
response = requests.post(
    "https://api.minimaxi.com/v1/image_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "image-01-live",
        "prompt": "一位穿着汉服的少女在樱花树下",
        "style": {
            "style_type": "水彩",
            "style_weight": 0.8
        },
        "aspect_ratio": "16:9"
    }
)
```

### 示例 3: 生成多张图片

```python
response = requests.post(
    "https://api.minimaxi.com/v1/image_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "image-01",
        "prompt": "未来城市天际线，赛博朋克风格，霓虹灯，飞行汽车",
        "n": 4,
        "aspect_ratio": "16:9",
        "seed": 42  # 使用相同种子可复现相似结果
    }
)

urls = response.json()["data"]["image_urls"]
for i, url in enumerate(urls):
    print(f"图片 {i+1}: {url}")
```
