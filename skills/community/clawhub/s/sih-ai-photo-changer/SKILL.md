---
name: sih-image-gen
description: AI图片生成与编辑工具，使用Sih.AI API进行自然语言驱动的图片处理。支持换装、换背景、换脸、风格转换（动漫/粘土/油画等）、美颜修图等功能。当用户需要通过自然语言描述来编辑图片（如"把衣服换成bikini"、"背景换成海边"、"转换成动漫风格"）时使用此skill。
---

# Sih.AI 图片生成

## 快速开始

通过自然语言描述来编辑图片，使用 `scripts/image_gen.py` 脚本调用API。

### 基本用法

```bash
# 使用URL
python scripts/image_gen.py "https://example.com/image.jpg" "背景改为在海边"

# 使用本地文件
python scripts/image_gen.py "./photo.jpg" "换成动漫风格"

# 指定模型
python scripts/image_gen.py "./photo.jpg" "美颜修图" "sihai-image-27"
```

### 常用处理提示词

- **换背景**: "背景改为在海边"、"背景换成城市夜景"、"背景改为森林"
- **换装**: "把衣服换成bikini"、"换成晚礼服"、"换成运动装"
- **风格转换**: "转换成动漫风格"、"转换成油画风格"、"转换成粘土风格"
- **美颜**: "美颜修图"、"磨皮美白"、"瘦身"

## API参数

### image (必需)
- **类型**: string 或 array
- **格式**:
  - 图片URL: `https://example.com/image.jpg`
  - Base64: 纯base64编码字符串（**不带** `data:image/...;base64,` 前缀）
- **说明**: 脚本会自动将本地文件路径转换为纯Base64格式（适配sihai-image-27模型）

### prompt (必需)
- **类型**: string
- **说明**: 自然语言描述想要的编辑效果
- **建议**: 使用简洁、明确的中文描述

### model (可选)
- **类型**: string
- **默认值**: `sihai-image-27`
- **说明**: 使用的模型名称

## 输出格式

API返回JSON格式，包含生成的图片URL：

```json
{
  "model": "sihai-image-27",
  "created": 1773386658,
  "data": [
    {
      "url": "https://...",
      "size": "2048x2048"
    }
  ],
  "usage": {
    "generated_images": 1,
    "output_tokens": 16384,
    "total_tokens": 16384
  }
}
```

## 错误处理

- **401/403**: API token无效或过期
- **400**: 参数错误（图片URL无效、prompt为空等）
- **500/503**: 服务暂时不可用，稍后重试

## 注意事项

- 确保图片URL可公开访问
- sihai-image-27模型使用纯base64编码，**不需要** `data:image/...;base64,` 前缀
- 生成的图片URL有效期为24小时
