---
name: video-transcript-extractor
version: 1.0.0
description: |
  Extract text from videos and audio across 20+ platforms including TikTok, YouTube, Bilibili, and Douyin. Uses multi-level extraction strategy (subtitle track → speech recognition → AI correction) to achieve 95%+ accuracy. Supports batch processing and multi-language content.
tags: ["video", "transcript", "extraction", "speech-recognition", "youtube", "tiktok", "bilibili", "content-creation"]
---

# Video Transcript Extractor

> 🎬 Extract text from videos and audio with multi-platform support

## Skill Overview

This skill helps AI Agents extract text content from various video and audio platforms, supporting 20+ platforms including Douyin, Bilibili, Xiaohongshu, Weibo, WeChat Video, TikTok, YouTube, and Instagram. With multi-level extraction strategy (subtitle track → speech recognition → AI correction), it ensures 95%+ accuracy.

## Core Capabilities

- **Multi-platform Support**: Douyin, Kuaishou, Bilibili, Xiaohongshu, Weibo, WeChat Video, TikTok, YouTube and 20+ more
- **Smart Extraction**: Prioritizes native subtitles (100% accuracy), uses ASR + AI correction when needed
- **Audio Separation**: Automatically identifies and extracts background music info
- **Batch Processing**: Support batch extraction for multiple video links
- **Multi-language**: Chinese, English, Japanese, Korean and 100+ languages

## Trigger Keywords

- `/extract-transcript`
- `/video-to-text`
- `/transcript-extraction`
- `/video-subtitle-extract`
- `/audio-to-text`
- `/extract-video-text`

## How to Use

### Basic Usage

Provide a video link, and the Agent automatically identifies the platform and extracts the transcript:

```
User: Extract transcript from: https://v.douyin.com/xxxxx
Agent: Extracting video transcript...
     Video Title: xxx
     Duration: 3m 25s
     
     【Transcript Content】
     (Full extracted transcript)
     
     【Background Music】
     Song: xxx
     Artist: xxx
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| video_url | Yes | Video share link |
| extract_audio | No | Whether to extract audio, default false |
| auto_correct | No | Whether to enable AI correction, default true |

### Supported Platforms

| Platform | Share Link Format | Subtitle | Audio |
|----------|-------------------|----------|-------|
| Douyin | https://v.douyin.com/xxx | ✅ | ✅ |
| Kuaishou | https://v.kuaishou.com/xxx | ✅ | ✅ |
| Bilibili | https://b23.tv/xxx or BV号 | ✅ | ✅ |
| Xiaohongshu | https://www.xiaohongshu.com/xxx | ✅ | ✅ |
| Weibo | https://weibo.com/xxx | ✅ | ✅ |
| WeChat Video | Video account link | ✅ | ✅ |
| TikTok | https://tiktok.com/@xxx/video/xxx | ✅ | ✅ |
| YouTube | https://youtube.com/xxx | ✅ | ✅ |

## Extraction Strategy

### Strategy 1: Subtitle Track (Highest Priority)

Prioritize native subtitles from video:
1. Extract CC subtitles/official subtitles
2. Extract user-uploaded subtitle files
3. Return original text if subtitles available

### Strategy 2: Speech Recognition

Use ASR when no subtitles:
1. Separate video/audio streams
2. Call ASR API to recognize speech
3. Return timestamp-to-text mapping

### Strategy 3: AI Correction

Intelligent correction after recognition:
1. Fix obvious typos
2. Optimize punctuation
3. Complement colloquial expressions
4. Output complete, fluent transcript

## Output Format

```markdown
## Video Information
- Title: xxx
- Platform: YouTube
- Duration: 3m 25s
- Published: 2024-01-15
- Author: @xxx

## Transcript Content
(Complete transcript, ready for copy-paste)

## Timeline
- 00:00 - Opening Introduction
- 00:15 - Core Content Begins
- 01:30 - Case Analysis
- 03:00 - Summary

## Background Music
- Song: xxx
- Artist: xxx
- Music Link: https://...
```

## Usage Examples

### Example 1: Extract YouTube Video Transcript

```
User: Extract this video transcript: https://youtube.com/watch?v=xxx
Agent: Extracting YouTube video transcript...
     ✅ Extraction successful!
     
     Video Title: Future Trends in AI Agents
     Duration: 5m 12s
     
     【Transcript Content】
     Hello everyone, today we're going to talk about the future of AI agents...
     (Full transcript ~2000 words)
```

### Example 2: Extract TikTok Video

```
User: Extract this TikTok transcript: https://tiktok.com/@user/video/xxx
Agent: Extracting TikTok video transcript...
     ✅ Extraction successful!
     
     Video Title: Quick makeup tutorial
     Subtitle Type: Auto-generated subtitles
     Accuracy: 98%
     
     【Transcript Content】
     (Full transcript content)
```

### Example 3: Batch Extraction

```
User: Batch extract these video transcripts:
1. https://youtube.com/xxx1
2. https://tiktok.com/xxx2
3. https://instagram.com/xxx3

Agent: Batch extracting...
     ✅ Batch extraction complete!
     
     | # | Platform | Title | Status | Words |
     |---|----------|-------|--------|-------|
     | 1 | YouTube | AI Tutorial | ✅ Success | 1234 |
     | 2 | TikTok | Coding Tips | ✅ Success | 856 |
     | 3 | Instagram | Travel Vlog | ✅ Success | 542 |
```

## Technical Implementation

### API Call Flow

```
1. Parse video link → Get real URL and platform type
2. Call platform API → Get video info and subtitles/audio
3. Format conversion → Output as standard Markdown
4. AI correction (optional) → Improve accuracy
5. Return result → Display to user
```

### API Endpoints Reference

| Platform | API Endpoint | Notes |
|----------|--------------|-------|
| YouTube | `/api/v1/youtube/web/fetch_one_video` | TikHub API |
| TikTok | `/api/v1/tiktok/web/fetch_one_video` | TikHub API |
| Douyin | `/api/v1/douyin/web/fetch_one_video_by_share_url` | TikHub API |
| Bilibili | `/api/v1/bilibili/web/fetch_one_video` | Requires BV number |

### Audio Processing

- Prioritize `music.play_url` field for pure audio
- Fallback to `video.play_addr` field
- Duration is in milliseconds, divide by 1000 for seconds

## Notes

1. **Subtitle Priority**: Native subtitles are prioritized for 100% accuracy
2. **Link Format**: Supports both share links and direct links
3. **Copyright Notice**: Extracted content is for learning reference only
4. **Long Video**: Videos over 10 minutes should be extracted in segments
5. **Network Issues**: Retry or manually provide subtitle files if needed

## Use Cases

- 📝 **Content Creators**: Quickly get viral video transcripts for reference
- 🔍 **Market Research**: Analyze competitor video content strategies
- 📚 **Knowledge Organization**: Convert video content to text notes
- 🤖 **AI Training**: Collect corpus data
- 📱 **Social Sharing**: Share core video content with friends

## Changelog

### v1.0.0 (2024-01-20)
- Initial release
- Support for YouTube, TikTok, Instagram, Douyin and more
- Subtitle track priority extraction strategy
- AI intelligent correction support

## Author Info

- Author: AI Agent Helper
- Version: 1.0.0
- Framework: OpenClaw
