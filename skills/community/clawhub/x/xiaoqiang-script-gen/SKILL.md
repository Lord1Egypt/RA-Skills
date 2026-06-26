---
name: video-script-generator
version: "1.0.0"
license: MIT
description: >-
  AI-powered short video script generator. Input a video topic/title,
  get complete matching content: viral titles, opening hooks, 
  interactive comments, hashtag recommendations.
  Zero API cost — template-based generation works out of the box.
  Use when creating short video content for Douyin/TikTok/YouTube Shorts,
  or when you need quick script ideas and viral captions.
user-invocable: true
tags:
  - video-script
  - short-video
  - content-creation
  - douyin
  - tiktok
  - social-media
  - copywriting
metadata:
  openclaw:
    emoji: "🎬"
    primaryEnv: ""
    install:
      - name: ""
        type: ""
        spec: ""
    requires: {}
---

# video-script-generator — AI短视频文案生成器 🎬

Generate complete short video content packages in seconds. No API keys, no external dependencies — pure template-based generation.

## Usage

### Full Package Generation

```bash
# Generate everything: titles + hook + comments + hashtags
node cli.js "职场干货"
node cli.js "职场干货" --style 搞笑 --platform 抖音
```

### Individual Content Types

```bash
# Only viral titles
node cli.js titles "职场干货"

# Only opening hook
node cli.js hook "职场干货" --duration 15

# Only hashtags
node cli.js hashtags "职场干货" --platform 快手

# Only comment templates  
node cli.js comments "职场干货"
```

## Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `--style` | 实用/搞笑/情感/知识 | 实用 | Content style |
| `--platform` | 抖音/快手/视频号/B站 | 抖音 | Target platform |
| `--duration` | 15/30/60 | 30 | Video duration (seconds) |
| `--json` | flag | false | JSON output format |

## Output Example

```
🎬 视频主题：职场干货

📌 爆款标题（5条）
1. 领导绝对不会告诉你的职场潜规则
2. 同事不会教你的3个职场生存技巧
3. 为什么你努力工作却不被提拔？
4. 职场新人必须知道的5件事
5. 离职前一定要想清楚的3个问题

🎙️ 开头话术（15秒）
"你知道吗？职场里90%的人都踩过这个坑...
不是能力不行，是没人告诉你...
今天这条视频，我用3分钟帮你避坑。"

💬 评论区互动话术
- "你觉得职场最重要的是什么？评论区聊聊"
- "踩过这个坑的点个赞"
- "关注我，每天分享职场干货"

#标签
#职场 #职场干货 #职场技巧 #职场生存 #加薪 #升职 #打工人 #职场女性 #职场男性 #自我提升
```

## Styles

- **实用** — Tips, how-tos, tutorials
- **搞笑** — Humorous, relatable content
- **情感** — Emotional, storytelling
- **知识** — Educational, in-depth explanations

## Platforms

- **抖音** — Maximum hashtags, trendy language
- **快手** — More casual, community-focused
- **视频号** — WeChat ecosystem friendly
- **B站** — Longer form, detailed content

## Why This Skill?

✅ **Zero cost** — No API keys needed
✅ **Instant results** — Generate in milliseconds  
✅ **Multi-format** — Titles, hooks, comments, hashtags
✅ **Platform optimized** — Different styles per platform

## Technical Details

- Pure Node.js, no external dependencies
- Template-based generation with randomization
- Single file CLI (`cli.js`)
- ~6KB total size

## Roadmap (v1.1+)

- [ ] More template variations per style
- [ ] Batch generation mode
- [ ] Custom template support
- [ ] Viral score prediction

---

*Part of the AI Content Creator Suite*
*License: MIT — Free to use, modify, and distribute*
