---
name: vision
description: |
  让没有原生 vision 能力的模型获得识图能力。当用户发送图片、分享图片路径、或要求分析/描述/识别图片内容时，必须使用此 skill。
  触发场景（必须使用）：用户说"看这张图"、"帮我识别这个图片"、"描述一下这张图"、"分析这个截图"、"比较这些图片"、发送图片文件路径、消息中出现图片附件、或要求识别图片中的文字/内容时。
  多图支持：当用户一次发送多张图片或要求比较/对比图片时，使用多图模式。
  不触发场景：用户只是讨论图片处理技术、询问图片格式、要求生成图片、或编写图片处理代码时，不要使用此 skill。
---

# Vision Skill

让没有原生识图能力的模型（如 DeepSeek）也能"看图"——通过调用外部视觉 API 获取图片的文字描述。

## 快速配置

```bash
node scripts/vision.js --setup
```

按提示输入 API Key、API 地址、模型名称。

### 查看当前配置

```bash
node scripts/vision.js --config
```

## 使用方法

### 自动触发（推荐）

当用户发送图片或要求分析图片时，自动调用：

```bash
node scripts/vision.js "<图片路径>" "用中文描述这张图片"
```

### 单张图片

```bash
# 本地图片
node scripts/vision.js /path/to/image.jpg "描述图片内容"

# 网络图片
node scripts/vision.js --url https://example.com/image.png "这是什么？"
```

### 多张图片

```bash
# 多张本地图片
node scripts/vision.js image1.jpg image2.jpg image3.jpg "比较这些图片的异同"

# 混合本地和网络图片
node scripts/vision.js local.jpg --url https://example.com/online.png "这两张图有什么关系？"
```

## 支持的图片格式

jpg, jpeg, png, gif, webp, bmp

## 支持的视觉服务

| 服务 | 模型 | 备注 |
|------|------|------|
| **阿里云百炼（推荐）** | `qwen3.5-omni-plus` | 新用户 100 万 token 免费 |
| 阿里云百炼 | `qwen-vl-max` | 同上 |
| OpenAI | `gpt-4o-mini` | 需海外支付 |
| 其他 | 任何 OpenAI 兼容格式 | 改 `BASE_URL` 和模型名即可 |

## 配置文件说明

配置文件：`~/.claude/skills/vision/config.json`

```json
{
  "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "api_key": "你的API Key",
  "model": "qwen3.5-omni-plus"
}
```

## 工作原理

1. 读取图片文件 → 转换为 base64
2. 调用视觉 API（OpenAI 兼容格式）
3. 返回文字描述

## 注意事项

- 需要 Node.js 环境
- 首次使用需配置 API Key
- 网络图片需要能访问对应 URL
