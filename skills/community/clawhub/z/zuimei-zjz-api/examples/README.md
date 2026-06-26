# 最美证件照 API SDK

AI 图像处理 API 的 Python/TypeScript SDK。

## API 端点

| 接口 | 说明 |
|------|------|
| `/api/v1/photo/id-photo` | 一键证件照 |
| `/api/v1/segment/portrait` | 智能抠图 |
| `/api/v1/segment/background` | 换背景色 |
| `/api/v1/photo/enhance` | 人脸增强 |
| `/api/v1/photo/layout` | 排版照 |
| `/api/v1/photo/edit` | 图片编辑 |

## 快速开始

### Python

```bash
pip install requests

export ZUIMEI_API_KEY="your_api_key"
export ZUIMEI_SECRET_KEY="your_secret_key"

python python_sdk.py
```

### TypeScript

```bash
npm install axios form-data

export ZUIMEI_API_KEY="your_api_key"
export ZUIMEI_SECRET_KEY="your_secret_key"

npx tsc typescript_sdk.ts && node typescript_sdk.js
```

## 使用示例

```python
from python_sdk import ZuimeiZjzClient

client = ZuimeiZjzClient()

# 一寸证件照（蓝底+美颜）
result = client.id_photo("photo.jpg", width=295, height=413, background_color="#438EDB", beautify=True)

# 智能抠图
result = client.segment_portrait("photo.jpg")

# 换背景色（多色）
result = client.segment_background("photo.jpg", background_color="#FFFFFF;#438EDB", quality="hd-pro")

# 人脸增强
result = client.enhance("blurry.jpg", fidelity=0.3, use_sr=True)

# 排版照
result = client.layout("id_photo.jpg", layout_type="6inch")

# 图片编辑
result = client.edit("photo.jpg", width=800, height=600)
```
