---
name: zhz-image-gen
homepage: http://openclaw.bjbook.net/
description: 中文AI图片生成工具，支持通义万相(DashScope)接口。用于生成漫画、插图、海报等图片内容。当用户需要生成图片时使用。
version: 1.0.0
metadata:
  openclaw:
    requires:
      packages:
        - requests
        - pyyaml
---

# 中文AI图片生成工具

基于通义万相(DashScope)接口的图片生成工具，专为中文用户设计。

## 安装依赖

```bash
pip install requests pyyaml
```

## 快速开始

```bash

# 生成图片
python scripts/main.py --prompt "一只猫" --image cat.png

# 指定参数
python scripts/main.py --prompt "美丽的风景" --image out.png --ar 16:9 --quality 2k
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--prompt`, `-p` | 提示词文本 |
| `--promptfiles` | 从文件读取提示词（可多个） |
| `--image` | 输出图片路径（必需） |
| `--model`, `-m` | 模型ID（默认：qwen-image-3.0-pro） |
| `--ar` | 宽高比（16:9, 1:1, 4:3, 3:4 等） |
| `--size` | 指定尺寸（宽x高，如 1024x1024） |
| `--quality` | 质量等级：normal（普通）或 2k（高清），默认 2k |
| `--ref` | 参考图片（仅 wan2.7-image 系列模型支持） |

## 支持的模型

| 模型 | 说明 | 特点 |
|------|------|------|
| `qwen-image-3.0-pro` | 通义万相3.0专业版 | 最新模型，质量最高，自动优化 |
| `qwen-image-3.0` | 通义万相3.0标准版 | 最新模型，速度快 |
| `qwen-image-2.0-pro` | 通义万相2.0专业版 | 支持自定义尺寸，质量高 |
| `qwen-image-2.0` | 通义万相2.0标准版 | 支持自定义尺寸，速度快 |
| `wan2.7-image-pro` | 万相2.7图片专业版 | 支持参考图片，最高4K |
| `wan2.7-image` | 万相2.7图片标准版 | 支持参考图片 |

## 配置文件

工具会自动加载配置文件，按以下优先级查找：

1. `.zhz-skills/image-gen/config.yaml`（项目级）
2. `~/.zhz-skills/image-gen/config.yaml`（用户级）

配置文件格式：

```yaml
# 默认模型
default_model: qwen-image-3.0-pro

# 默认质量
default_quality: 2k

# 默认宽高比
default_aspect_ratio: "1:1"
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 通义万相API密钥（可选） |
| `DASHSCOPE_BASE_URL` | 自定义API端点（可选） |
| `DASHSCOPE_IMAGE_MODEL` | 模型（可选） |

## 使用示例

### 基本生成

```bash
python scripts/main.py --prompt "一只可爱的猫咪" --image cat.png
```

### 指定尺寸和宽高比

```bash
python scripts/main.py --prompt "壮丽的山川" --image landscape.png --ar 16:9 --quality 2k
```

### 使用参考图片（仅 wan2.7 模型）

```bash
python scripts/main.py --prompt "保持人物特征，更换背景为海滩" \
  --image output.png \
  --model wan2.7-image-pro \
  --ref reference.png
```

### 从文件读取提示词

```bash
python scripts/main.py --promptfiles prompt.txt --image output.png
```

## 注意事项

- 生成图片通常需要 15-30 秒
- 参考图片仅 wan2.7-image 系列模型支持，最多9张
- API密钥需要从通义万相控制台获取
- 配置文件优先级高于环境变量
