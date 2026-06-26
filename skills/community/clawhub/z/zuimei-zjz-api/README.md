# 最美证件照 API Skill

AI 图像处理 API 技能包，支持证件照制作、智能抠图、人脸增强、换背景色等功能。

**官网**：https://zuimei.huipai.vip

## 功能特性

- 🎯 **一键证件照** - 完整证件照制作流程，支持多种规格和背景色
- ✂️ **智能抠图** - 人像抠图，生成透明背景 PNG
- 🎨 **换背景色** - 支持纯色、渐变、多色背景替换
- ✨ **人脸增强** - 修复模糊照片，提升清晰度
- 📄 **排版照** - 生成打印排版照（6寸/5寸/A4）
- 🔧 **图片编辑** - 尺寸调整、格式转换、DPI 设置

## API 端点

| 接口 | 端点 | 说明 |
|------|------|------|
| 一键证件照 | `/api/v1/photo/id-photo` | 完整证件照制作流程 |
| 智能抠图 | `/api/v1/segment/portrait` | 人像抠图，生成透明 PNG |
| 换背景色 | `/api/v1/segment/background` | 替换背景颜色，支持渐变和多色 |
| 人脸增强 | `/api/v1/photo/enhance` | 修复模糊、提升清晰度 |
| 排版照 | `/api/v1/photo/layout` | 生成打印排版照 |
| 图片编辑 | `/api/v1/photo/edit` | 尺寸调整、格式转换 |

## 安装

### 从 ClawHub 安装

```bash
clawhub install zuimei-zjz-api
```

### 从 GitHub 安装

```bash
clawhub install --git https://github.com/flaravel/zuimei-zjz-api.git
```

## 快速开始

### 环境变量

```bash
export ZUIMEI_API_KEY="your_api_key"
export ZUIMEI_SECRET_KEY="your_secret_key"
```

### Python 示例

```python
from python_sdk import ZuimeiZjzClient

client = ZuimeiZjzClient()

# 一寸证件照（蓝底，默认不开启美颜）
result = client.id_photo("photo.jpg", width=295, height=413,
                         background_color="#438EDB")

# 智能抠图
result = client.segment_portrait("photo.jpg")

# 换背景色
result = client.segment_background("photo.jpg", background_color="#FFFFFF")

# 人脸增强
result = client.enhance("blurry.jpg", fidelity=0.3, use_sr=True)

# 排版照
result = client.layout("id_photo.jpg", layout_type="6inch")

# 图片编辑
result = client.edit("photo.jpg", width=800, height=600)
```

## 文档

- [API.md](./API.md) - API 详细文档
- [openapi.yaml](./openapi.yaml) - OpenAPI 3.0 规范
- [examples/](./examples/) - Python/TypeScript SDK 示例
- [prompts/](./prompts/) - AI 提示词模板

## 认证方式

使用 v2 签名认证（HMAC-SHA256）：

```python
import hmac
import hashlib

def generate_signature(method, url, timestamp, nonce, content_sha256, secret_key):
    sign_str = f"{method}\n{url}\n{timestamp}\n{nonce}\n{content_sha256}"
    return hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
```

## 许可证

MIT

## 联系方式

- 官网：https://zuimei.huipai.vip
