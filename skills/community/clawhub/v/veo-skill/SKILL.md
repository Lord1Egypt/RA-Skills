---
name: veo-skill
description: Veo, Veo 3.1 Fast - Google AI video generation models for AI agents. 1080p HD output, reference image support, intelligent audio generation.
metadata:
  openclaw:
    requires:
      env:
        - MONET_API_KEY # Required: API key from monet.vision
      bins: []
---

# Veo Skill

Veo is Google's advanced AI video generation model series designed for AI agents. Part of the Monet AI unified API platform.

## When to Use

Use this skill when:

- **High-Quality Video Generation**: Create professional-grade 1080p HD videos
  - veo-3-1: Advanced AI video with sound generation
  - veo-3-1-fast: Ultra-fast video generation
- **Reference Image to Video**: Use reference images to guide video content and style
- **Multiple Aspect Ratios**: Generate videos for different platforms (16:9 for YouTube, 9:16 for TikTok)
- **Audio-Visual Content**: Veo 3.1 includes intelligent audio generation

## Getting API Key

1. Visit https://monet.vision to register an account
2. After login, go to https://monet.vision/skills/keys to create an API Key
3. Configure the API Key in environment variables or code

If you don't have an API Key, ask your owner to apply at monet.vision.

## Quick Start

### Create a Video Generation Task

```bash
curl -X POST https://monet.vision/api/v1/tasks/async \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -d '{
    "type": "video",
    "input": {
      "model": "veo-3-1",
      "prompt": "A cat running in the park",
      "duration": 8,
      "aspect_ratio": "16:9"
    },
    "idempotency_key": "unique-key-123"
  }'
```

> ⚠️ **Important**: `idempotency_key` is **required**. Use a unique value (e.g., UUID) to prevent duplicate task creation if the request is retried.

Response:

```json
{
  "id": "task_abc123",
  "status": "pending",
  "type": "video",
  "created_at": "2026-02-27T10:00:00Z"
}
```

### Get Task Status and Result

Task processing is asynchronous. You need to poll the task status until it becomes `success` or `failed`. **Recommended polling interval: 5 seconds**.

```bash
curl https://monet.vision/api/v1/tasks/task_abc123 \
  -H "Authorization: Bearer $MONET_API_KEY"
```

Response when completed:

```json
{
  "id": "task_abc123",
  "status": "success",
  "type": "video",
  "outputs": [
    {
      "model": "veo-3-1",
      "status": "success",
      "progress": 100,
      "url": "https://files.monet.vision/..."
    }
  ],
  "created_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T10:01:30Z"
}
```

**Example: Poll until completion**

```typescript
const TASK_ID = "task_abc123";
const MONET_API_KEY = process.env.MONET_API_KEY;

async function pollTask() {
  while (true) {
    const response = await fetch(
      `https://monet.vision/api/v1/tasks/${TASK_ID}`,
      {
        headers: {
          Authorization: `Bearer ${MONET_API_KEY}`,
        },
      },
    );

    const data = await response.json();
    const status = data.status;

    if (status === "success") {
      console.log("Task completed successfully!");
      console.log(JSON.stringify(data, null, 2));
      break;
    } else if (status === "failed") {
      console.log("Task failed!");
      console.log(JSON.stringify(data, null, 2));
      break;
    } else {
      console.log(`Task status: ${status}, waiting...`);
      await new Promise((resolve) => setTimeout(resolve, 5000));
    }
  }
}

pollTask();
```

## Supported Models

### veo-3-1

**veo-3-1** - Google Veo 3.1

_Advanced AI video generation with sound_

- 🎯 **Use Cases**: High-quality video generation with audio
- 🎵 **Audio**: Intelligent audio generation included
- ⏱️ **Duration**: 8 seconds
- 🖥️ **Resolution**: 1080p HD

```typescript
{
  model: "veo-3-1",
  prompt: string,                // Required
  images?: string[],             // Optional: Reference images
  duration?: number,             // Optional: 8 (default)
  aspect_ratio?: "1:1" | "16:9" | "9:16"
}
```

### veo-3-1-fast

**veo-3.1-fast** - Veo 3.1 Fast

_Ultra-fast video generation_

- 🎯 **Use Cases**: Quick video generation for rapid iteration
- ⚡ **Speed**: Ultra-fast generation
- ⏱️ **Duration**: 8 seconds
- 🖥️ **Resolution**: 1080p HD

```typescript
{
  model: "veo-3-1-fast",
  prompt: string,                // Required
  images?: string[],             // Optional: Reference images
  duration?: number,             // Optional: 8 (default)
  aspect_ratio?: "1:1" | "16:9" | "9:16"
}
```

## API Reference

### Create Task (Async)

POST `/api/v1/tasks/async` - Create an async task. Returns immediately with task ID.

**Request:**

```bash
curl -X POST https://monet.vision/api/v1/tasks/async \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -d '{
    "type": "video",
    "input": {
      "model": "veo-3-1",
      "prompt": "A cat running in the park"
    },
    "idempotency_key": "unique-key-123"
  }'
```

> ⚠️ **Important**: `idempotency_key` is **required**. Use a unique value (e.g., UUID) to prevent duplicate task creation if the request is retried.

**Response:**

```json
{
  "id": "task_abc123",
  "status": "pending",
  "type": "video",
  "created_at": "2026-02-27T10:00:00Z"
}
```

### Create Task (Streaming)

POST `/api/v1/tasks/sync` - Create a task with SSE streaming. Waits for completion and streams progress.

**Request:**

```bash
curl -X POST https://monet.vision/api/v1/tasks/sync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -N \
  -d '{
    "type": "video",
    "input": {
      "model": "veo-3-1",
      "prompt": "A cat running"
    },
    "idempotency_key": "unique-key-123"
  }'
```

### Get Task

GET `/api/v1/tasks/{taskId}` - Get task status and result.

**Request:**

```bash
curl https://monet.vision/api/v1/tasks/task_abc123 \
  -H "Authorization: Bearer $MONET_API_KEY"
```

**Response:**

```json
{
  "id": "task_abc123",
  "status": "success",
  "type": "video",
  "outputs": [
    {
      "model": "veo-3-1",
      "status": "success",
      "progress": 100,
      "url": "https://files.monet.vision/..."
    }
  ],
  "created_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T10:01:30Z"
}
```

### List Tasks

GET `/api/v1/tasks/list` - List tasks with pagination.

**Request:**

```bash
curl "https://monet.vision/api/v1/tasks/list?page=1&pageSize=20" \
  -H "Authorization: Bearer $MONET_API_KEY"
```

**Response:**

```json
{
  "tasks": [
    {
      "id": "task_abc123",
      "status": "success",
      "type": "video",
      "outputs": [
        {
          "model": "veo-3-1",
          "status": "success",
          "progress": 100,
          "url": "https://files.monet.vision/..."
        }
      ],
      "created_at": "2026-02-27T10:00:00Z",
      "updated_at": "2026-02-27T10:01:30Z"
    }
  ],
  "page": 1,
  "pageSize": 20,
  "total": 100
}
```

### Upload File

POST `/api/v1/files` - Upload a file to get an online access URL.

> 📁 **File Storage**: Uploaded files are stored for **24 hours** and will be automatically deleted after expiration.

**Request:**

```bash
curl -X POST https://monet.vision/api/v1/files \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -F "file=@/path/to/your/image.jpg" \
  -v
```

**Response:**

```json
{
  "id": "file_xyz789",
  "url": "...",
  "filename": "image.jpg",
  "size": 1048576,
  "content_type": "image/jpeg",
  "created_at": "2026-02-27T10:00:00Z"
}
```

## Configuration

### Environment Variables

```bash
export MONET_API_KEY="monet_xxx"
```

### Authentication

All API requests require authentication via the `Authorization` header:

```
Authorization: Bearer monet_xxx
```
