---
name: tiktok-bulk-publisher
version: 1.2.0
description: 批量上传和发布 TikTok 视频，支持 OAuth 2.0 授权 API，自定义标题、隐私和互动设置
author: fly3094
tags: [tiktok, video, automation, social-media, batch, oauth]
support: 
  paypal: 492227637@qq.com
  email: 492227637@qq.com
metadata:
  clawdbot:
    emoji: 🎵
    requires:
      bins:
        - python3
        - curl
    config:
      env:
        TIKTOK_CLIENT_KEY:
          description: TikTok API Client Key
          required: true
        TIKTOK_CLIENT_SECRET:
          description: TikTok API Client Secret
          required: true
---

# TikTok Bulk Publisher 🎵

批量上传和发布 TikTok 视频，自动化视频发布流程。

## 功能特点

- ✅ 批量上传视频
- ✅ 自定义标题和描述
- ✅ 隐私设置（公开/好友/私密）
- ✅ 互动设置（评论/合拍/duet）
- ✅ OAuth 2.0 授权
- ✅ TikTok API 2026 版支持
- ✅ 视频自动剪辑功能
- ✅ 热门音乐推荐
- ✅ 标签优化建议
- ✅ 发布时段分析

## 使用方法

```bash
# 批量上传视频
python3 scripts/tiktok_publisher.py --videos ./videos/ --config config.json

# 指定发布时段
python3 scripts/tiktok_publisher.py --videos ./videos/ --schedule "18:00-22:00"
```

## 许可证

MIT

## 作者

fly3094
