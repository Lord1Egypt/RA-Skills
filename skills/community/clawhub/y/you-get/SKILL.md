---
name: you-get
description: 网页媒体下载助手 - 从YouTube、Bilibili等网站下载视频、音频、图片
version: 0.1.2
metadata:
  openclaw:
    requires:
      bins:
        - python
        - you-get
        - ffmpeg
    emoji: "⬇️"
    homepage: https://github.com/soimort/you-get
---

# you-get 网页媒体下载助手

## 技能概述

本技能帮助用户从Web下载媒体内容（视频、音频、图片），支持以下场景：
- **视频下载**: 从YouTube、Bilibili、优酷等网站下载视频
- **音频下载**: 从SoundCloud、网易云音乐等下载音频
- **图片下载**: 从Tumblr、Instagram等下载图片
- **在线观看**: 使用本地播放器观看在线视频（无广告）

**支持网站**: YouTube, Twitter, Bilibili, 优酷, 爱奇艺, Instagram, Tumblr, SoundCloud 等 80+ 网站

## 使用流程

AI 助手将引导你完成以下步骤：
1. 安装 you-get（如未安装）
2. 查看可下载的视频质量
3. 选择格式并下载
4. 验证下载结果

## 关键章节导航

- [安装指南](./guides/01-installation.md)
- [快速开始](./guides/02-quickstart.md)
- [高级用法](./guides/03-advanced-usage.md)
- [常见问题](./troubleshooting.md)

## AI 助手能力

当你向 AI 描述下载需求时，AI 会：
- 自动识别网址支持的网站
- 查看所有可用的视频质量和格式
- 执行下载命令并监控进度
- 处理下载失败并提供替代方案
- 支持断点续传和批量下载
- 提取视频字幕和元数据

## 核心功能

- ✅ 支持 80+ 主流视频/音频网站
- ✅ 自动选择最佳质量下载
- ✅ 支持指定格式和分辨率
- ✅ 支持断点续传
- ✅ 支持代理下载
- ✅ 支持在线播放
- ✅ 自动下载字幕
- ✅ 支持cookies登录下载

## 快速示例

```bash
# 下载YouTube视频
you-get 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 查看可用格式
you-get -i 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 指定格式下载
you-get --itag=18 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 使用代理
you-get -x 127.0.0.1:8087 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

## 安装要求

- Python 3.7.4 或更高版本
- FFmpeg 1.0 或更高版本（用于视频合并）
- （可选）RTMPDump（用于RTMP流）

## 许可证

MIT License

## 项目链接

- GitHub: https://github.com/soimort/you-get
- 官网: https://you-get.org/
- 文档: https://github.com/soimort/you-get/wiki
