---
name: minimax-image
description: MiniMax 图片生成技能。集成文生图和图生图功能，支持从文本描述生成图片，也可基于参考图生成新图片。触发场景：(1) 用户请求生成图片，(2) 用户提供描述并要求生成图片，(3) 用户上传参考图并要求基于该图生成新图，(4) 用户想要生成指定风格的图片。支持的风格：漫画、元气、中世纪、水彩（仅 image-01-live）。支持的宽高比：1:1、16:9、4:3、3:2、2:3、3:4、9:16、21:9。
---

# MiniMax 图片生成技能

## 功能概览

| 功能 | API 端点 | 说明 |
|------|----------|------|
| 文生图 | `/v1/image_generation` | 从文本描述生成图片 |
| 图生图 | `/v1/image_generation` | 基于参考图 + 文本生成新图 |

## 工作流程

### 文生图

```
文本描述 → API 调用 → 自动保存本地 → 返回路径
```

### 图生图

```
参考图 + 文本描述 → API 调用 → 自动保存本地 → 返回路径
```

## 快速开始

### 文生图

```python
import requests
import os
import base64

API_KEY = os.getenv("MINIMAX_API_KEY")
URL = "https://api.minimaxi.com/v1/image_generation"

payload = {
    "model": "image-01",
    "prompt": "一只可爱的小老虎在森林里",
    "aspect_ratio": "16:9",
    "n": 1,
    "response_format": "url"
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(URL, json=payload, headers=headers)
result = response.json()
image_url = result["data"]["image_urls"][0]

# 自动下载保存
save_dir = os.path.expanduser("~/.openclaw/workspace/assets/images")
os.makedirs(save_dir, exist_ok=True)
filename = f"generated_{int(time.time())}.jpeg"
save_path = os.path.join(save_dir, filename)

img_response = requests.get(image_url)
with open(save_path, 'wb') as f:
    f.write(img_response.content)

print(f"图片已保存: {save_path}")
```

### 图生图

```python
# 读取本地图片并转为 Base64
with open("reference.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

payload = {
    "model": "image-01",
    "prompt": "same person wearing traditional Chinese Hanfu",
    "aspect_ratio": "3:4",
    "n": 1,
    "subject_reference": [
        {
            "type": "character",
            "image_file": f"data:image/jpeg;base64,{img_base64}"
        }
    ]
}
```

## 支持的模型

| 模型 | 说明 | 适用场景 |
|------|------|----------|
| `image-01` | 高质量图片生成 | 通用场景 |
| `image-01-live` | 带风格的图片生成 | 需要漫画/水彩等风格 |

## 核心参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | `image-01` 或 `image-01-live` |
| `prompt` | string | 是 | 图片描述，最长 1500 字符 |
| `n` | int | 否 | 生成数量 [1, 9]，默认 1 |
| `subject_reference` | array | 否 | 参考图配置（图生图用） |
| `style` | object | 否 | 风格设置（仅 image-01-live） |
| `aspect_ratio` | string | 否 | 宽高比 |

### subject_reference 结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 当前仅支持 `character` |
| `image_file` | string | 是 | 参考图 URL 或 Base64 |

### 参考图要求

- **格式**：JPG, JPEG, PNG
- **大小**：小于 10MB
- **最佳效果**：单人正面照片

## 宽高比

| 值 | 分辨率 |
|----|--------|
| `1:1` | 1024x1024 |
| `16:9` | 1280x720 |
| `4:3` | 1152x864 |
| `3:2` | 1248x832 |
| `2:3` | 832x1248 |
| `3:4` | 864x1152 |
| `9:16` | 720x1280 |
| `21:9` | 1344x576 (仅 image-01) |

## 风格类型（仅 image-01-live）

| 风格 | 说明 |
|------|------|
| `漫画` | 漫画风格 |
| `元气` | 元气/活力风格 |
| `中世纪` | 中世纪风格 |
| `水彩` | 水彩画风格 |

## 输出目录

生成的图片默认保存在：`~/.openclaw/workspace/assets/images/`

文件名格式：`{type}_{timestamp}_{index}.jpeg`
- `type`: text2img / img2img
- `timestamp`: Unix 时间戳
- `index`: 多图时的序号

## 脚本工具

- `scripts/generate_image.py` - 文生图工具（自动保存本地）
- `scripts/image_to_image.py` - 图生图工具（自动保存本地）

### 命令行用法

```bash
# 文生图
python generate_image.py "一只可爱的小老虎" --ratio 16:9 --n 3

# 图生图
python image_to_image.py "穿汉服的女孩" --ref path/to/image.jpg --ratio 3:4
```

## API 参考

- [references/image-api.md](references/image-api.md) - 完整 API 文档
