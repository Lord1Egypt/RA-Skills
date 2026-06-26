---
name: zhipu-image-gen
description: AI text-to-image generation using Zhipu AI's GLM-Image model. Use when the user requests image generation, creating images from text descriptions, or mentions "文生图", "生成图片", "画图". Supports various image sizes and Chinese/English prompts.
metadata:
  openclaw:
    requires:
      env:
        - ZHIPU_API_KEY
      bins:
        - curl
        - jq
---

# Zhipu Image Generator

智谱 AI GLM-Image 文生图工具。支持中英文提示词生成高质量图片。

## 快速开始

```bash
~/.openclaw/workspace/skills/zhipu-image-gen/scripts/generate_image.sh -p "你的提示词"
```

## 文件结构

```
~/.openclaw/workspace/skills/zhipu-image-gen/
├── SKILL.md              # 本文档
├── .env.example          # 配置模板
└── scripts/
    └── generate_image.sh # 图片生成脚本
```

## 配置

### 方式一：环境变量（推荐）

```bash
export ZHIPU_API_KEY="your_api_key_here"
```

### 方式二：.env 文件

```bash
# 复制模板并填入 API Key
cp ~/.openclaw/workspace/skills/zhipu-image-gen/.env.example ~/.openclaw/workspace/skills/zhipu-image-gen/.env
# 编辑 .env 文件，填入你的 API Key
```

### 获取 API Key

1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 进入控制台 → API 密钥管理
4. 复制 API Key

## 使用方法

### 基本用法

```bash
# 中文提示词
./scripts/generate_image.sh -p "一只可爱的小猫咪，坐在阳光明媚的窗台上"

# 英文提示词
./scripts/generate_image.sh -p "A cute kitten sitting on a sunny windowsill"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --prompt` | 图片描述（必填） | - |
| `-s, --size` | 图片尺寸 | 1280x1280 |
| `-o, --output` | 输出目录 | 当前目录 |
| `-w, --watermark` | 启用水印 | false |
| `-h, --help` | 显示帮助 | - |

### 支持的尺寸

- `1280x1280`（默认，方形）
- `1024x1024`
- `768x768`
- 其他 API 支持的常用尺寸

## 示例

```bash
# 生成风景图
./generate_image.sh -p "夕阳下的海边沙滩，海浪轻轻拍打着岸边"

# 指定尺寸
./generate_image.sh -p "一款现代简约风格的智能手表" -s 1024x1024

# 保存到指定目录
./generate_image.sh -p "一朵盛开的玫瑰花" -o ~/Pictures
```

## 文件结构

```
~/.openclaw/workspace/skills/zhipu-image-gen/
├── SKILL.md              # 本文档
├── .env                  # API Key 配置（需自行创建）
├── .env.example          # 配置模板
└── scripts/
    └── generate_image.sh # 图片生成脚本
```

## 注意事项

- 生成的图片为 PNG 格式
- 文件名格式：`glm_image_YYYYMMDD_HHMMSS.png`
- 支持中英文提示词
- 描述越详细，效果越好
- API 调用按次数计费
