---
name: Tencent TTS Podcast Generator
description: Convert text to podcast audio using Tencent Cloud TTS. Supports both short and long text processing, generates up to 30-minute long audio with automatic chunking and parallel processing. Supports 26 Chinese voices including basic, featured, customer service, and Tencent featured voices.
license: MIT
---

# Tencent TTS Podcast Generator

Convert text content to podcast audio files using Tencent Cloud TTS service.

## Capabilities

### What This Skill Can Do
- **Short & Long Text Compatible**: Intelligently detects text length, processes short text directly, auto-chunks long text
- **Long Text to Speech**: Supports generating podcasts up to 30 minutes long (~7200 characters)
- **Concurrent Processing**: Long texts are automatically split and processed in parallel for faster generation
- **26 Voices**: Supports basic, featured, customer service, and Tencent featured voices
- **Smart Chunking**: Splits text at semantic boundaries (paragraph/sentence) for natural audio flow
- **Duration Estimation**: Automatically estimates generated audio duration
- **Auto Retry**: Automatically retries failed requests to improve success rate

### Short & Long Text Processing Strategy

> **Note**: Tencent Cloud TTS single request limit is ~150 characters. Texts exceeding this will be auto-chunked.

| Text Type | Length Range | Processing Method | Concurrency | Timeout |
|-----------|-------------|-------------------|-------------|---------|
| Ultra Short | ≤50 chars | Direct request | 1 | 30s |
| Short | 50-150 chars | Direct request | 1 | 30s |
| Medium | 150-500 chars | Auto-chunk (2-4 chunks) | 2-3 | 60s |
| Long | 500-2000 chars | Auto-chunk (4-14 chunks) | 3-5 | 60s |
| Extra Long | 2000-7200 chars | Auto-chunk (14-50 chunks) | 3-5 | 60s |

### What This Skill Does NOT Do
- Does not generate mp3 format (wav only)
- Does not support background music or sound effects
- Does not auto-generate podcast scripts (user must provide)
- Does not support dual-speaker dialogue mode (single voice only)

---

## File Structure

This Skill consists of the following files:

- `tts_podcast.py`
  Main entry script
  - Tencent Cloud TTS signature generation
  - Audio file generation
  - COS upload functionality

- `tts_tool.py`
  AgentScope tool interface wrapper

- `SKILL.md`
  This file, describing Skill capabilities, boundaries, and usage conventions

- `requirements.txt`
  Python dependency configuration

---

## Input & Output Specifications

### Input Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `Text` | Text content to convert | Yes | - |
| `VoiceType` | Voice ID (see voice table below, either this or VoiceName) | No | 502006 |
| `VoiceName` | Voice name (see voice table below, either this or VoiceType) | No | - |
| `secret_id` | Tencent Cloud SecretId | Yes | - |
| `secret_key` | Tencent Cloud SecretKey | Yes | - |
| `max_workers` | Concurrent threads (3-5 for long text, 1 for short) | No | 3 |
| `chunk_size` | Chunk size in characters (long text optimization) | No | 140 |
| `timeout` | Request timeout in seconds | No | 30/60 |
| `enable_retry` | Enable automatic retry | No | true |
| `max_retries` | Max retry attempts | No | 2 |
| `preserve_paragraphs` | Preserve paragraph boundaries when chunking | No | true |
| `cos_secret_id` | Tencent Cloud COS SecretId (optional, defaults to TTS credentials) | No | - |
| `cos_secret_key` | Tencent Cloud COS SecretKey (optional, defaults to TTS credentials) | No | - |
| `upload_cos` | Whether to upload to COS, true/false (default false, local only) | No | false |
| `bucket_name` | COS Bucket name (default: ti-aoi) | No | ti-aoi |
| `app_id` | COS App ID (default: 1257195185) | No | 1257195185 |
| `region` | COS region (default: ap-guangzhou) | No | ap-guangzhou |

### Output

```json
{
  "Code": 0,
  "Msg": "success",
  "AudioUrl": "https://xxx.cos.ap-guangzhou.myqcloud.com/xxx.wav"
}
```

---

## Usage

### Environment Requirements
- Python 3.8+
- tencentcloud-sdk-python
- cos-python-sdk-v5
- requests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from tts_podcast import main

result = main({
    "Text": "Hello, welcome to today's podcast.",
    "VoiceType": 502006,
    "secret_id": "YOUR_SECRET_ID",
    "secret_key": "YOUR_SECRET_KEY"
})

print(result)
# {'Code': 0, 'Msg': 'success', 'AudioUrl': 'https://...'}
```

### Short Text Optimized Usage

```python
# Short text (<150 chars) - Use single thread for fast response
result = main({
    "Text": "Hello, this is a short message.",
    "VoiceType": 502006,
    "secret_id": "YOUR_SECRET_ID",
    "secret_key": "YOUR_SECRET_KEY",
    "max_workers": 1,      # Single thread is sufficient
    "timeout": 30,         # 30 second timeout
    "enable_retry": True   # Enable retry
})
```

### Long Text Optimized Usage

```python
# Long text (>150 chars) - Use concurrency for speed
long_text = """Chapter 1: The Origin of AI

The concept of artificial intelligence can be traced back to ancient Greek mythology..."""

result = main({
    "Text": long_text,
    "VoiceType": 502007,
    "secret_id": "YOUR_SECRET_ID",
    "secret_key": "YOUR_SECRET_KEY",
    "max_workers": 5,          # Concurrent processing
    "chunk_size": 140,         # 140 chars per chunk
    "timeout": 60,             # 60 second timeout
    "preserve_paragraphs": True  # Preserve paragraph boundaries
})
```

---

## Voice Reference

| VoiceType | Voice Name | Characteristics |
|-----------|------------|-----------------|
| 0 | 普通女声 | Standard female |
| 1 | 普通男声 | Standard male |
| 5 | 情感女声 | Emotional female |
| 6 | 情感男声 | Emotional male |
| 1000 | 智障少女 | Lively cute |
| 1001 | 阳光少年 | Bright youthful |
| 1002 | 温柔淑女 | Gentle female |
| 1003 | 成熟青年 | Mature male |
| 1004 | 严厉管事 | Stern female |
| 1005 | 亲和女声 | Friendly female |
| 1006 | 甜美女声 | Sweet female |
| 1007 | 磁性男声 | Magnetic male |
| 1008 | 播音主播 | Broadcast anchor |
| 101001 | 客服女声 | Customer service |
| 101005 | 售前客服 | Pre-sales service |
| 101007 | 售后客服 | After-sales service |
| 101008 | 亲和客服 | Friendly service |
| 502006 | 小旭 | Tencent voice |
| 502007 | 小巴 | Tencent voice |
| 502008 | 思驰 | Tencent voice |
| 502009 | 思佳 | Tencent voice |
| 502010 | 思悦 | Tencent voice |
| 502011 | 小宁 | Tencent voice |
| 502012 | 小杨 | Tencent voice |
| 502013 | 云扬 | Tencent voice |
| 502014 | 云飞 | Tencent voice |

---

## Technical Architecture

### tts_podcast.py

- **TTS**: Uses Tencent Cloud TTS API signature v3
- **Upload**: Uses Tencent Cloud COS SDK for audio file upload
- **Auth**: Supports credentials from parameters or environment variables
- **Short & Long Text Compatible**:
  - Short text (≤150 chars): Direct single request, fast response
  - Long text (>150 chars): Smart chunking + concurrent processing + auto-merge

### Text Chunking Strategy

1. **Paragraph Priority**: Try to preserve paragraph integrity, split at paragraph boundaries
2. **Sentence Boundaries**: When paragraphs are too long, split at sentence ending punctuation (。！？；)
3. **Semantic Protection**: Avoid truncating in the middle of words, ensure semantic coherence
4. **Length Control**: Each chunk does not exceed 150 characters (Tencent Cloud API limit)

---

## License

MIT
