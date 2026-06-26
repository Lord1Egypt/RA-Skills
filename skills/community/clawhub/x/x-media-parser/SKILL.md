---
name: x-media-parser
description: 解析 X/Twitter 帖子，获取图片和视频的下载直链。使用 vxtwitter API，无需登录。
homepage: https://github.com
metadata:
  {
    "openclaw": {
      "emoji": "𝕏"
    }
  }
---

# X Media Parser

解析 X/Twitter 帖子，获取图片和视频的下载直链。

## 功能

- ✅ 解析 X/Twitter 帖子
- ✅ 获取图片直链（支持多图）
- ✅ 获取视频直链（支持多视频）
- ✅ 无需登录/X API Key
- ✅ 支持 GIF
- ✅ 返回媒体元信息（分辨率、时长等）

## 使用方法

### 命令行

```bash
x-media-parser "https://x.com/user/status/1234567890"
```

### 返回格式

```json
{
  "success": true,
  "media": {
    "type": "video",
    "title": "用户名: 贴文内容",
    "directUrl": "https://video.twimg.com/...",
    "videoUrls": ["..."],
    "imageUrls": null,
    "thumbnail": "https://pbs.twimg.com/...",
    "duration": 120,
    "resolution": "1920x1080"
  }
}
```

### 媒体类型

- `video` - 单视频
- `videos` - 多视频
- `image` - 单图片
- `images` - 多图片
- `mixed` - 混合（视频+图片）

## 底层实现

使用 vxtwitter API: `https://api.vxtwitter.com/Twitter/status/{tweetId}`

## 依赖

- curl
- python3

## 配合 Aria2 使用

```bash
# 解析帖子
JSON=$(x-media-parser "https://x.com/user/status/123")

# 提取直链
URL=$(echo "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['media']['directUrl'])")

# 发送到 Aria2 下载
aria2-download "$URL"
```

## 一键下载脚本

同目录下提供 `x-aria-download.sh`，可一键解析并下载：

```bash
x-aria-download "https://x.com/user/status/123"
```

文件名格式：`昵称_贴文前10字_编号.扩展名`
