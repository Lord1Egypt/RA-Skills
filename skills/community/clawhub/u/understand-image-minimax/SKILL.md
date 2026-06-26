---
name: understand-image-minimax
description: 图片理解技能，使用 Minimax Coding Plan VLM API 分析图片
metadata: {"clawdbot":{"emoji":"🖼️","requires":{"bins":["node"]}}}
---

# Understand Image

使用 Minimax Coding Plan VLM API 分析图片内容。API Key 从环境变量 `MINIMAX_API_KEY` 读取。

当接收到用户发送的图片或用户询问图片的内容时请务必使用该技能

## 使用方法

```bash
node {baseDir}/scripts/understand.cjs "你的问题" "图片URL或本地路径"
```

## 示例

```bash
# 分析网络图片
node {baseDir}/scripts/understand.cjs "描述这张图片" "https://example.com/photo.jpg"

# 分析本地图片
node {baseDir}/scripts/understand.cjs "这张图片有什么" "/Users/xbos1314/Downloads/image.png"

# 询问具体问题
node {baseDir}/scripts/understand.cjs "图片中有几个人?" "https://example.com/group.jpg"
```

## 数据来源

API Key 从环境变量读取：
- 环境变量：`MINIMAX_API_KEY`
- API Host：固定为 `https://api.minimaxi.com`

## 支持的图片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

## 输入支持

- **网络图片**: 直接使用 HTTP/HTTPS URL
- **本地图片**: 使用绝对路径或相对路径
- **Base64**: 支持 data: URL 格式
