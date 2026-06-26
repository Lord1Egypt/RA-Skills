---
name: wechat-video-search
description: (已验证) 通过 TikHub API 搜索微信视频号视频(需要翻墙)，支持关键词搜索，返回视频下载链接和分析数据。
metadata:
  version: 1.0.0
  source: https://github.com/your-repo/wechat-video-search
  author: 明智的超级 AI 助理
  tags: [wechat, video, search, tikhub, social-media]
  license: MIT
  requirements:
    - python
    - "pip:requests"
---

# SKILL.md for wechat-video-search

## Description

微信视频号视频搜索技能，通过调用 **TikHub 官方 API** 来获取搜索结果。支持关键词搜索，返回视频下载链接、点赞数、播放量等分析数据。

## Configuration

本技能需要一个有效的 TikHub API Token 才能工作。请在您的 `~/.openclaw/config.json` 文件中添加以下配置项。

```json
{
  "tikhub_api_token": "YOUR_TIKHUB_API_TOKEN"
}
```

> 您可以在 [TikHub 官网](https://user.tikhub.io/register) 注册免费获取 Token。

## How to Use

### 命令行调用

```bash
python3 scripts/wechat_video_search.py "美食"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| keyword | 搜索关键词（必填） | - |
| --raw | 输出原始 JSON 数据 | 否 |

### 示例

```bash
# 简单搜索
python3 scripts/wechat_video_search.py "餐饮 鸡鸭鹅"

# 输出原始 JSON
python3 scripts/wechat_video_search.py "熟食" --raw
```

## 重要笔记：Windows 环境下的调用

此脚本在 Windows 环境下运行时，可能会因为默认的 GBK 编码无法处理 API 返回的特殊字符（如 emoji）而导致 `UnicodeEncodeError`。

**为了确保脚本能正确执行，必须在调用时使用 `-X utf8` 参数强制 Python 解释器使用 UTF-8 编码。**

**正确调用示例 (PowerShell):**
```powershell
& "F:\python 3.10\python.exe" -X utf8 "C:\Users\EDY\.openclaw\skills\wechat-video-search-1.0.0\scripts\wechat_video_search.py" "你的关键词"
```

## API 端点

- **域名**: https://api.tikhub.dev（中国大陆用户）
- **路径**: /api/v1/wechat_channels/fetch_search_latest
- **方法**: GET
- **参数**: keywords（URL 编码）
- **认证**: Authorization: Bearer <token>

## 返回数据

```json
{
  "code": 200,
  "data": [
    {
      "video_id": "视频 ID",
      "desc": "视频描述",
      "author": {
        "nickname": "作者昵称"
      },
      "statistics": {
        "play_count": 播放量,
        "digg_count": 点赞数
      },
      "video": {
        "play_addr": {
          "url_list": ["视频下载链接"]
        }
      }
    }
  ]
}
```

## 注意事项

1. 中国大陆用户必须使用 `api.tikhub.dev` 域名，不要用 `api.tikhub.io`（被墙）
2. Token 可与 douyin-video-search、douyin-downloader 等其他 TikHub 系技能共用
3. 返回的视频链接可直接下载或用于分析
