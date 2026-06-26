---
name: qwen-logo-designer
description: 商业LOGO设计技能。通过用户描述生成专业商业LOGO图片。使用阿里云百炼千问图像模型(qwen-image-2.0-pro)进行文生图。当用户需要：(1) 设计公司/品牌LOGO (2) 生成商业标识图标 (3) 创建品牌视觉符号 (4) 根据描述生成logo图片时使用此技能。支持自定义尺寸、风格、负面提示词等参数。生成的图片自动保存为MD5文件名，支持去重。
---

# Qwen Logo Designer

## Overview

通过自然语言描述，为用户生成专业的商业LOGO图片。使用阿里云百炼的千问图像模型 (qwen-image-2.0-pro)。

**特性：**
- ✅ 自动保存为 MD5 文件名（去重）
- ✅ 通过环境变量配置输出目录
- ✅ 支持多种尺寸和风格
- ✅ 可选去除水印

## Quick Start

用户描述LOGO需求后，执行以下流程：

1. **收集需求** - 确认以下信息（如用户未提供，主动询问）：
   - 品牌/公司名称
   - 行业类型
   - 风格偏好（现代/复古/极简/科技感等）
   - 配色偏好（可选）
   - 图标/文字/组合型LOGO偏好

2. **生成Prompt** - 将用户需求转换为专业的图像生成提示词

3. **调用API** - 使用 `scripts/generate_logo.py` 生成LOGO

4. **返回结果** - 展示生成的图片地址

## 使用方法

### 基本调用

```bash
python3 scripts/generate_logo.py --prompt "为科技公司设计的现代简约风格LOGO，蓝白配色，几何图形与字母C结合" --api-key "$DASHSCOPE_API_KEY"
```

### 完整参数

```bash
python3 scripts/generate_logo.py \
  --prompt "LOGO描述..." \
  --negative-prompt "低质量,模糊,变形" \
  --size "1024*1024" \
  --no-watermark \
  --api-key "$DASHSCOPE_API_KEY"
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | 是 | - | LOGO设计描述 |
| `--negative-prompt` | 否 | 见脚本 | 负面提示词，避免生成不想要的元素 |
| `--size` | 否 | 1024*1024 | 图片尺寸，支持 512*512, 1024*1024, 2048*2048 等 |
| `--no-watermark` | 否 | - | 添加此参数去除水印 |
| `--api-key` | 是 | - | 阿里云百炼 API Key |
| `--output` | 否 | - | 保存图片的本地路径（可选） |

## Prompt 优化指南

### 商业LOGO专用提示词模板

**极简风格：**
```
minimalist logo design for [公司名], [行业], clean lines, simple geometric shapes, [配色], white background, vector style, professional, timeless
```

**科技风格：**
```
modern tech logo for [公司名], futuristic, gradient colors, abstract geometric, digital elements, clean typography, [配色]
```

**复古风格：**
```
vintage logo design for [公司名], retro aesthetic, classic typography, emblem style, [配色], hand-crafted feel
```

**创意/艺术风格：**
```
creative logo design for [公司名], artistic, unique shape, bold colors, memorable, brand identity focused
```

### 中英文混合建议

千问图像模型对中英文提示词都有良好支持。对于中文品牌名，建议：
- 品牌名保持中文
- 设计风格描述使用英文获得更精准效果

示例：
```
为"云端科技"设计现代简约LOGO，蓝色渐变，云朵与电路图形结合，tech company logo, cloud and circuit elements, blue gradient, minimalist, modern
```

## 默认负面提示词

脚本内置以下负面提示词，确保LOGO质量：

```
低分辨率，低画质，模糊，噪点，变形，扭曲，构图混乱，文字错误，拼写错误，
水印，签名，边框，复杂背景，过度饱和，过度曝光，欠曝，色偏
```

## 注意事项

**URL 过期时间**： 生成的图片 URL 有效期很短（约 1 小时），请尽快保存或使用。使用 `--output` 参数直接保存到本地。

## 环境配置

需要设置环境变量：

```bash
# API Key (必需)
export DASHSCOPE_API_KEY="your-api-key-here"

# 输出目录 (可选，默认当前目录)
export LOGO_OUTPUT_DIR="~/logos"

# 或使用 WORKSPACE 作为备选
export WORKSPACE="~/.openclaw/workspace"
```

## 文件命名规则

- **自动命名**：使用图片内容的 MD5 值作为文件名（如 `a1b2c3d4e5f6.png`）
- **去重**：相同内容的图片不会重复保存
- **默认目录**：`LOGO_OUTPUT_DIR` > `WORKSPACE` > 当前目录

## 注意事项

**Q: 生成的LOGO有水印怎么办？**
A: 添加 `--no-watermark` 参数

**Q: 图片尺寸不够大？**
A: 使用 `--size 2048*2048` 生成高清图片

**Q: 想要透明背景？**
A: 在prompt中添加 "transparent background, no background, isolated on white"

**Q: 生成的文字不准确？**
A: 图像生成模型对文字渲染有限制，建议生成图形LOGO后用设计软件添加品牌名
