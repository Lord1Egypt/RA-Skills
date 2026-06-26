# Veo Skill

[![API](https://img.shields.io/badge/API-monet.vision-blue)](https://monet.vision)
[![Documentation](https://img.shields.io/badge/docs-latest-green)](https://monet.vision/skills/keys)

Veo is Google's advanced AI video generation model series designed for AI agents. It provides high-quality video output with support for reference images, multiple aspect ratios, and professional-grade production. Part of the Monet AI unified API platform.

## ✨ Features

### 🌟 Google Veo Series

- **veo-3-1**: Advanced AI video generation with sound support
- **veo-3-1-fast**: Ultra-fast video generation

### 🎯 Key Capabilities

- **1080p HD Output**: Generate high-resolution professional videos
- **Reference Images**: Support reference images for style and content guidance
- **Multiple Aspect Ratios**: From standard 16:9 to vertical 9:16
- **Audio Generation**: Veo 3.1 supports intelligent audio generation
- **Fast Mode**: Quick generation for rapid iteration

## 🚀 Quick Start

### Get API Key

1. Visit [monet.vision](https://monet.vision) to register an account
2. After login, go to [API Keys page](https://monet.vision/skills/keys) to create an API Key
3. Configure the API Key in environment variables or code

### Setup

Set environment variable:

```bash
export MONET_API_KEY="monet_xxx"
```

### Your First Video Generation Task

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

> ⚠️ **Important**: `idempotency_key` is **required**. Use a unique value (e.g., UUID) to prevent duplicate task creation on retries.

**Response Example:**

```json
{
  "id": "task_abc123",
  "status": "pending",
  "type": "video",
  "created_at": "2026-02-27T10:00:00Z"
}
```

### Query Task Status

Task processing is asynchronous. You need to poll the task status until it becomes `success` or `failed`. **Recommended polling interval: 5 seconds**.

```bash
curl https://monet.vision/api/v1/tasks/task_abc123 \
  -H "Authorization: Bearer $MONET_API_KEY"
```

**Response when completed:**

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

### Polling Example (TypeScript)

```typescript
const TASK_ID = 'task_abc123';
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

    if (status === 'success') {
      console.log('Task completed successfully!');
      console.log(JSON.stringify(data, null, 2));
      break;
    } else if (status === 'failed') {
      console.log('Task failed!');
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

## 📖 API Reference

### Create Task (Async)

**POST** `/api/v1/tasks/async`

Create an async task, returns task ID immediately.

### Create Task (Streaming)

**POST** `/api/v1/tasks/sync`

Create task with SSE streaming, waits for completion and streams progress.

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

**GET** `/api/v1/tasks/{taskId}`

Get task status and result.

### List Tasks

**GET** `/api/v1/tasks/list`

List tasks with pagination.

```bash
curl "https://monet.vision/api/v1/tasks/list?page=1&pageSize=20" \
  -H "Authorization: Bearer $MONET_API_KEY"
```

### Upload File

**POST** `/api/v1/files`

Upload a file to get an online access URL.

> 📁 **File Storage**: Uploaded files are stored for **24 hours** and will be automatically deleted after expiration.

```bash
curl -X POST https://monet.vision/api/v1/files \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -F "file=@/path/to/your/image.jpg" \
  -v
```

## 🎬 Supported Models

### veo-3-1

_Veo 3.1 - Google Advanced Video Generation_

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

_Veo 3.1 Fast - Ultra-Fast Video Generation_

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

## 💡 Usage Examples

### Example 1: Basic Video Generation

```typescript
const response = await fetch('https://monet.vision/api/v1/tasks/async', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${process.env.MONET_API_KEY}`,
  },
  body: JSON.stringify({
    type: 'video',
    input: {
      model: 'veo-3-1',
      prompt: 'A futuristic city with neon lights',
      duration: 8,
      aspect_ratio: '16:9',
    },
    idempotency_key: crypto.randomUUID(),
  }),
});

const task = await response.json();
console.log('Task created:', task.id);
```

### Example 2: Generate Video with Reference Image

```typescript
// First, upload reference image
const formData = new FormData();
formData.append('file', imageFile);

const uploadResponse = await fetch('https://monet.vision/api/v1/files', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.MONET_API_KEY}`,
  },
  body: formData,
});

const fileData = await uploadResponse.json();
const imageUrl = fileData.url;

// Then create video task with reference image
const response = await fetch('https://monet.vision/api/v1/tasks/async', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${process.env.MONET_API_KEY}`,
  },
  body: JSON.stringify({
    type: 'video',
    input: {
      model: 'veo-3-1',
      prompt: 'Generate a dynamic video based on this image',
      images: [imageUrl],
      duration: 8,
      aspect_ratio: '16:9',
    },
    idempotency_key: crypto.randomUUID(),
  }),
});

const task = await response.json();
console.log('Task created:', task.id);
```

### Example 3: Fast Mode for Quick Iteration

```typescript
const response = await fetch('https://monet.vision/api/v1/tasks/async', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${process.env.MONET_API_KEY}`,
  },
  body: JSON.stringify({
    type: 'video',
    input: {
      model: 'veo-3-1-fast',
      prompt: 'A beautiful sunset over the ocean',
      duration: 8,
      aspect_ratio: '16:9',
    },
    idempotency_key: crypto.randomUUID(),
  }),
});

const task = await response.json();
console.log('Task created:', task.id);
```

## 🔐 Authentication

All API requests require authentication via the `Authorization` header:

```
Authorization: Bearer monet_xxx
```

## 📋 Task Status

| Status       | Description                          |
| ------------ | ------------------------------------ |
| `pending`    | Task created, waiting for processing |
| `processing` | Task is being processed              |
| `success`    | Task completed successfully          |
| `failed`     | Task failed                          |

## 🌟 Best Practices

1. **Use Idempotency Keys**: Always provide a unique `idempotency_key` for tasks to prevent duplicate creation
2. **Reference Images**: Use reference images to guide video style and content
3. **Fast Mode for Iteration**: Use `veo-3-1-fast` for quick iterations, switch to `veo-3-1` for final production
4. **Aspect Ratio Selection**: Choose appropriate aspect ratio based on your distribution platform (16:9 for YouTube, 9:16 for TikTok/Shorts)
5. **Polling Interval**: Poll every 5 seconds to avoid excessive requests while getting timely updates

## 📚 Related Links

- Documentation: [SKILL.md](./SKILL.md)
- Website: [monet.vision](https://monet.vision)
- API Keys: [monet.vision/skills/keys](https://monet.vision/skills/keys)

---

Please visit [monet.vision](https://monet.vision) for terms of service and usage license.

Powered by Monet AI - Comprehensive content generation platform built for AI agents
