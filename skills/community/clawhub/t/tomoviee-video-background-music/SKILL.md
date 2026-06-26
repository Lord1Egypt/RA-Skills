---
name: tomoviee-video-scoring
description: Generate music tailored to video content. Use when users request video_soundtrack operations or related tasks.
---

# Tomoviee AI - 视频配乐 (Video Soundtrack)

## Overview

Generate music tailored to video content.

**API**: `tm_video_scoring`

## Quick Start

### Authentication

```bash
python scripts/generate_auth_token.py YOUR_APP_KEY YOUR_APP_SECRET
```

### Python Client

```python
from scripts.tomoviee_video_soundtrack_client import TomovieeClient

client = TomovieeClient("app_key", "app_secret")
```

## API Usage

### Basic Example

```python
task_id = client._make_request({
    video='https://example.com/my-video.mp4'
    prompt='Modern tech product music, clean'
})

result = client.poll_until_complete(task_id)
import json
output = json.loads(result['result'])
```

### Parameters

- `video` (required): Video URL (MP4, <200M)
- `prompt`: Optional style guidance
- `duration`: Audio duration (5-900, default: 20)

## Async Workflow

1. **Create task**: Get `task_id` from API call
2. **Poll for completion**: Use `poll_until_complete(task_id)`
3. **Extract result**: Parse returned JSON for output URLs

**Status codes**:
- 1 = Queued
- 2 = Processing
- 3 = Success (ready)
- 4 = Failed
- 5 = Cancelled
- 6 = Timeout

## Resources

### scripts/
- `tomoviee_video_soundtrack_client.py` - API client
- `generate_auth_token.py` - Auth token generator

### references/
See bundled reference documents for detailed API documentation and examples.

## External Resources

- **Developer Portal**: https://www.tomoviee.ai/developers.html
- **API Documentation**: https://www.tomoviee.ai/doc/
- **Get API Credentials**: Register at developer portal
