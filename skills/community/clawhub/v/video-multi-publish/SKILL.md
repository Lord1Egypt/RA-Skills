---
name: video-multi-publish
description: One-stop multi-platform video publishing workflow. From video clipping to multi-platform publishing, full process automation. Supports automatic clipping for platform formats, intelligent title optimization, tag recommendation, best publish time recommendation, one-click publishing to WeChat, Bilibili, Xiaohongshu, Douyin, YouTube, TikTok and more.
license: MIT License
metadata:
    skill-author: academic-assistant
    version: 1.0.0
    created: 2026-03-14
---

# Video Multi-Platform Publish

## Overview

一站式多平台视频发布工作流技能，从视频剪辑到多平台发布全流程自动化。

**核心功能**:
- ✅ 视频自动剪辑 (多平台格式适配)
- ✅ 智能标题优化
- ✅ 智能标签推荐
- ✅ 自动描述生成
- ✅ 最佳发布时间推荐
- ✅ 一键发布多平台
- ✅ 数据分析跟踪

**支持平台**:
- 微信公众号
- B 站
- 小红书
- 抖音
- YouTube
- TikTok

---

## 🚀 Quick Start

### Basic Usage

```bash
# 一键剪辑并发布到所有平台
python video_multi_publish.py -i input.mp4 --title "我的视频" --desc "视频描述"

# 剪辑并发布到指定平台
python video_multi_publish.py -i input.mp4 -p wechat bilibili --title "我的视频"

# 仅剪辑不发布
python video_multi_publish.py -i input.mp4 --clip-only

# 仅发布不剪辑 (使用已剪辑的视频)
python video_multi_publish.py -i clipped_video.mp4 --publish-only
```

### Python API

```python
from video_multi_publish import VideoMultiPublisher

# 创建发布器
publisher = VideoMultiPublisher()

# 一站式服务 (剪辑 + 发布)
publisher.publish_all(
    input_file="input.mp4",
    title="我的视频",
    description="视频描述",
    platforms=["wechat", "bilibili", "xiaohongshu", "douyin"]
)

# 仅剪辑
publisher.clip_video(
    input_file="input.mp4",
    platforms=["wechat", "bilibili", "xiaohongshu"]
)

# 仅发布
publisher.publish_video(
    video_file="clipped_video.mp4",
    platform="wechat",
    title="优化后的标题",
    description="优化后的描述"
)
```

---

## 📋 Workflow Stages

### Stage 1: 视频分析 (1-2 分钟)

**分析内容**:
- 视频格式
- 分辨率
- 时长
- 帧率
- 比特率
- 音频信息

**输出**:
```json
{
  "format": "mp4",
  "resolution": "1920x1080",
  "duration": 1800,
  "fps": 30,
  "bitrate": "8000k",
  "audio": "aac"
}
```

---

### Stage 2: 自动剪辑 (5-15 分钟)

**根据目标平台自动剪辑**:

| 平台 | 画面比例 | 分辨率 | 时长 | 操作 |
|------|----------|--------|------|------|
| **微信公众号** | 16:9 | 1920x1080 | ≤10 分钟 | 裁剪时长 |
| **B 站** | 16:9 | 1920x1080 | ≤15 分钟 | 裁剪时长 |
| **小红书** | 9:16 | 1080x1920 | ≤3 分钟 | 裁剪 + 转竖屏 |
| **抖音** | 9:16 | 1080x1920 | ≤5 分钟 | 裁剪 + 转竖屏 |
| **YouTube** | 16:9 | 1920x1080 | ≤120 分钟 | 保持原样 |
| **TikTok** | 9:16 | 1080x1920 | ≤3 分钟 | 裁剪 + 转竖屏 |

**输出**:
```
output_dir/
├── video_wechat.mp4
├── video_bilibili.mp4
├── video_xiaohongshu.mp4
├── video_douyin.mp4
├── video_youtube.mp4
└── video_tiktok.mp4
```

---

### Stage 3: 内容优化 (2-5 分钟)

**标题优化**:
```
原标题："我的视频"

优化后:
- 微信公众号："5 个实用技巧，让你的视频更专业！"
- B 站："【新手必看】5 个实用技巧｜从入门到精通"
- 小红书："视频必看！5 个技巧超实用"
- 抖音："5 个实用技巧，学会秒变大神！"
- YouTube: "5 Practical Tips to Make Your Videos Professional"
- TikTok: "5 Tips You Need to Know!"
```

**标签生成**:
```
智能推荐:
- 微信公众号：视频号、原创、热门
- B 站：原创、教程、技能、实用、干货
- 小红书：#视频 #技巧 #干货 #教程 #实用
- 抖音：#热门 #推荐 #技巧 #教程 #干货
- YouTube: Tutorial, Tips, How to, Guide, Professional
- TikTok: #fyp #viral #tips #tutorial #trending
```

**描述优化**:
```
模板:
[吸引注意力的开头]
[视频内容介绍]
[关键看点/时间点]
[行动号召]
[相关标签]

示例:
想让你的视频更专业吗？这 5 个技巧一定要学会！

本期视频分享 5 个实用的视频技巧，包括：
- 00:30 技巧 1
- 01:45 技巧 2
- 03:20 技巧 3
- 04:50 技巧 4
- 06:10 技巧 5

学会这些技巧，你的视频质量提升一个档次！

#视频 #技巧 #干货 #教程 #实用
```

---

### Stage 4: 平台发布 (10-30 分钟)

**发布流程**:
```
1. 上传视频
   ↓
2. 填写信息 (标题/描述/标签)
   ↓
3. 设置封面
   ↓
4. 设置发布选项
   ↓
5. 确认发布
   ↓
6. 获取链接
```

**发布结果**:
```json
{
  "wechat": {
    "status": "success",
    "url": "https://mp.weixin.qq.com/s/xxx",
    "publish_time": "2026-03-15 20:00:00"
  },
  "bilibili": {
    "status": "success",
    "url": "https://www.bilibili.com/video/xxx",
    "publish_time": "2026-03-15 18:00:00"
  },
  ...
}
```

---

### Stage 5: 数据分析 (持续)

**跟踪指标**:
- 观看次数
- 点赞数
- 评论数
- 分享数
- 完播率
- 粉丝增长

**数据面板**:
```python
from video_multi_publish import VideoMultiPublisher

publisher = VideoMultiPublisher()

# 获取各平台数据
stats = publisher.get_analytics(days=7)

for platform, data in stats.items():
    print(f"{platform}:")
    print(f"  观看次数：{data['views']}")
    print(f"  点赞数：{data['likes']}")
    print(f"  评论数：{data['comments']}")
    print(f"  分享数：{data['shares']}")
    print()
```

---

## 🎯 Platform Specifications

### 微信公众号

| 参数 | 限制 | 推荐值 |
|------|------|--------|
| **画面比例** | 16:9 | 16:9 |
| **分辨率** | 1920x1080 | 1920x1080 |
| **最长时间** | 10 分钟 | 5-10 分钟 |
| **视频编码** | H.264 | H.264 |
| **比特率** | - | 5000k |
| **标题长度** | 最多 64 字符 | 30-50 字符 |
| **标签数量** | 最多 3 个 | 3 个 |
| **最佳发布时间** | - | 20:00-22:00 |

---

### B 站

| 参数 | 限制 | 推荐值 |
|------|------|--------|
| **画面比例** | 16:9 | 16:9 |
| **分辨率** | 1920x1080 | 1920x1080 |
| **最长时间** | 15 分钟 | 10-15 分钟 |
| **视频编码** | H.264 | H.264 |
| **比特率** | - | 6000k |
| **标题长度** | 最多 80 字符 | 40-60 字符 |
| **标签数量** | 最多 10 个 | 5-10 个 |
| **最佳发布时间** | - | 18:00-20:00 |

---

### 小红书

| 参数 | 限制 | 推荐值 |
|------|------|--------|
| **画面比例** | 9:16 | 9:16 |
| **分辨率** | 1080x1920 | 1080x1920 |
| **最长时间** | 3 分钟 | 1-3 分钟 |
| **视频编码** | H.264 | H.264 |
| **比特率** | - | 8000k |
| **标题长度** | 最多 20 字符 | 10-20 字符 |
| **标签数量** | 最多 5 个 | 5 个 |
| **最佳发布时间** | - | 19:00-21:00 |

---

### 抖音

| 参数 | 限制 | 推荐值 |
|------|------|--------|
| **画面比例** | 9:16 | 9:16 |
| **分辨率** | 1080x1920 | 1080x1920 |
| **最长时间** | 5 分钟 | 1-3 分钟 |
| **视频编码** | H.264 | H.264 |
| **比特率** | - | 8000k |
| **标题长度** | 最多 55 字符 | 20-40 字符 |
| **标签数量** | 最多 5 个 | 5 个 |
| **最佳发布时间** | - | 19:00-21:00 |

---

### YouTube

| 参数 | 限制 | 推荐值 |
|------|------|--------|
| **画面比例** | 16:9 | 16:9 |
| **分辨率** | 1920x1080 | 1920x1080 |
| **最长时间** | 120 分钟 | 10-20 分钟 |
| **视频编码** | H.264 | H.264 |
| **比特率** | - | 8000k |
| **标题长度** | 最多 100 字符 | 50-80 字符 |
| **标签数量** | 最多 15 个 | 10-15 个 |
| **最佳发布时间** | - | 14:00-16:00 (UTC) |

---

### TikTok

| 参数 | 限制 | 推荐值 |
|------|------|--------|
| **画面比例** | 9:16 | 9:16 |
| **分辨率** | 1080x1920 | 1080x1920 |
| **最长时间** | 3 分钟 | 1-3 分钟 |
| **视频编码** | H.264 | H.264 |
| **比特率** | - | 8000k |
| **标题长度** | 最多 150 字符 | 30-60 字符 |
| **标签数量** | 最多 5 个 | 5 个 |
| **最佳发布时间** | - | 18:00-20:00 (local) |

---

## 🔧 Advanced Usage

### Custom Platforms

```bash
# 只发布到指定平台
python video_multi_publish.py -i input.mp4 \
  -p wechat bilibili xiaohongshu \
  --title "我的视频"
```

### Custom Settings

```bash
# 自定义剪辑时长
python video_multi_publish.py -i input.mp4 \
  --clip-duration 300 \
  --title "我的视频"

# 自定义发布时间
python video_multi_publish.py -i input.mp4 \
  --schedule "2026-03-15 20:00:00" \
  --title "我的视频"
```

### Skip Stages

```bash
# 仅剪辑 (不发布)
python video_multi_publish.py -i input.mp4 --clip-only

# 仅发布 (使用已剪辑的视频)
python video_multi_publish.py -i clipped.mp4 --publish-only
```

---

## 📊 Performance Benchmarks

| 视频时长 | 剪辑时间 | 发布时间 | 总时间 |
|----------|----------|----------|--------|
| 5 分钟 | ~3 分钟 | ~10 分钟 | ~13 分钟 |
| 15 分钟 | ~8 分钟 | ~15 分钟 | ~23 分钟 |
| 30 分钟 | ~15 分钟 | ~20 分钟 | ~35 分钟 |
| 60 分钟 | ~25 分钟 | ~25 分钟 | ~50 分钟 |

*Times vary based on hardware and network speed*

---

## 🔍 Troubleshooting

### Issue 1: FFmpeg Not Found

**Error**: `ffmpeg is not recognized`

**Solution**:
```bash
# Install ffmpeg
winget install ffmpeg  # Windows
brew install ffmpeg    # macOS
sudo apt-get install ffmpeg  # Linux
```

---

### Issue 2: Upload Failed

**Error**: `Upload failed: Network error`

**Solution**:
```bash
# Check network connection
ping api.platform.com

# Retry upload
python video_multi_publish.py -i input.mp4 --retry
```

---

### Issue 3: Title Too Long

**Error**: `Title exceeds maximum length`

**Solution**:
```bash
# Use shorter title
python video_multi_publish.py -i input.mp4 \
  --title "Shorter Title"
```

---

## 🔗 Integration

### Standalone Usage

```python
from video_multi_publish import VideoMultiPublisher

publisher = VideoMultiPublisher()

# One-stop service
publisher.publish_all(
    input_file="input.mp4",
    title="My Video",
    description="Video description",
    platforms=["wechat", "bilibili", "xiaohongshu"]
)
```

### Integration with Other Skills

This skill integrates:
- **video-clip** - Video clipping
- **video-publish** - Video publishing

---

## 📁 Skill Files

```
skills/video-multi-publish/
├── openclaw.skill.json      # Skill configuration
├── SKILL.md                 # Skill documentation (this file)
├── scripts/
│   ├── video_multi_publish.py  # Main script
│   └── utils.py             # Utility functions
└── examples/
    └── example_usage.py     # Example usage
```

---

## Author

**Skill Version**: v1.0.0  
**Created**: 2026-03-14  
**Maintainer**: academic-assistant  
**License**: MIT License

---

*One-stop multi-platform video publishing!* 🎬📤
