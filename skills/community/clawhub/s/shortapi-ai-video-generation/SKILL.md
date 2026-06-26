---
name: ShortApi Video Models Aggregation Skill
description: "Use this skill as an entry point to discover, select, and fetch specific integration parameters for all supported AI video generation models."
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["SHORTAPI_KEY"] },
        "homepage": "https://shortapi.ai",
      },
  }
---

# Video Generation Models Integration Skill

> Use this skill to explore and integrate all available Video Generation models through the ShortAPI platform.

## Overview

ShortAPI provides a unified `/api/v1/job/create` endpoint for video generation across multiple top-tier providers natively. This skill provides an overview of all available video generation models and how to dynamically acquire the specific JSON schema required to invoke them.

- **API Endpoint**: `https://api.shortapi.ai/api/v1/job/create`
- **Category**: `text-to-video`, `image-to-video`
- **Kind**: inference

## Available Video Models

Here is the list of fully supported video generation model IDs you can use:

| Model ID                                   | Description                                          |
| ------------------------------------------ | ---------------------------------------------------- |
| `google/veo-3.1/text-to-video`             | Generate videos from text using Veo 3.1              |
| `google/veo-3.1/image-to-video`            | Generate videos from images using Veo 3.1            |
| `google/veo-3.1/extend-video`              | Extend existing videos using Veo 3.1                 |
| `google/veo-3.1/first-last-frame-to-video` | Generate videos from first and last frames (Veo 3.1) |
| `google/veo-3.1/reference-to-video`        | Generate videos from reference using Veo 3.1         |
| `google/veo-3/text-to-video`               | Generate videos from text using Veo 3                |
| `google/veo-3/image-to-video`              | Generate videos from images using Veo 3              |
| `kwaivgi/kling-3.0/text-to-video`          | Generate videos from text using Kling 3.0            |
| `kwaivgi/kling-3.0/image-to-video`         | Generate videos from images using Kling 3.0          |
| `kwaivgi/kling-o1/text-to-video`           | Generate videos from text using Kling O1             |
| `kwaivgi/kling-o1/image-to-video`          | Generate videos from images using Kling O1           |
| `kwaivgi/kling-o1/video-to-video`          | Transform videos using Kling O1                      |
| `kwaivgi/kling-2.6/text-to-video`          | Generate videos from text using Kling 2.6            |
| `kwaivgi/kling-2.6/image-to-video`         | Generate videos from images using Kling 2.6          |
| `bytedance/seedance-2.0/text-to-video`     | Generate videos from text using Seedance 2.0         |
| `vidu/vidu-q3/text-to-video`               | Generate videos from text using Vidu Q3              |
| `vidu/vidu-q3/image-to-video`              | Generate videos from images using Vidu Q3            |
| `vidu/vidu-q3/start-end-to-video`          | Generate videos from start/end frames (Vidu Q3)      |
| `vidu/vidu-q2/text-to-video`               | Generate videos from text using Vidu Q2              |
| `vidu/vidu-q2/image-to-video`              | Generate videos from images using Vidu Q2            |
| `vidu/vidu-q2/reference-to-video`          | Generate videos from reference using Vidu Q2         |
| `vidu/vidu-q2/start-end-to-video`          | Generate videos from start/end frames (Vidu Q2)      |
| `pixverse/pixverse-5.5/text-to-video`      | Generate videos from text using Pixverse 5.5         |
| `pixverse/pixverse-5.5/image-to-video`     | Generate videos from images using Pixverse 5.5       |
| `pixverse/pixverse-5.5/transition`         | Create video transitions using Pixverse 5.5          |
| `alibaba/wan-2.6/text-to-video`            | Generate videos from text using Wan 2.6              |
| `alibaba/wan-2.6/image-to-video`           | Generate videos from images using Wan 2.6            |
| `alibaba/wan-2.6/reference-to-video`       | Generate videos from reference using Wan 2.6         |

## How to use a Video Model

Because each video model supports different parameters (such as `duration`, `resolution`, `aspect_ratio`, `fps`, or advanced controls), you need to fetch the specific model's schema document to construct a valid API request payload.

### Step 1: Fetch the specific Model API Skill Document (MANDATORY)

You **MUST** first fetch the detailed skill document for the specific `<model_id>` (e.g. `google/veo-3.1/text-to-video`) before attempting to construct the POST request payload. **DO NOT** skip this step. **DO NOT** hallucinate parameters because different video models have completely different parameter names for the same concept (e.g. one model might use `duration` while another uses `length`, one might use `resolution` while another uses `quality`).

Send a `GET` request to:

```text
https://shortapi.ai/api/skill/<model_id>
```

_(For example: `GET https://shortapi.ai/api/skill/google/veo-3.1/text-to-video`)_

This URL will return a Markdown (`.md`) text document containing the exact Input Parameters Schema for that specific model, alongside code examples. You must parse it to understand which arguments go into the `args` object.

### Step 2: Construct the JSON Payload

Using the exact schema document fetched from Step 1, construct a valid JSON payload. **Only include arguments that were defined in the document fetched in Step 1.**
At a minimum, standard structures generally look like this:

```json
{
  "model": "<model_id>",
  "args": {
    "prompt": "Your descriptive text prompt here..."
    // ...other model-specific required or optional parameters strictly parsed from Step 1
  },
  "callback_url": "YOUR_OPTIONAL_WEBHOOK_URL"
}
```

### Step 3: Invoke the Unified Generation Endpoint

Make an HTTP POST request to the API Endpoint. Include the Bearer token in the `Authorization` header.

#### Bash (cURL) Example

```bash
response=$(curl --request POST \
  --url https://api.shortapi.ai/api/v1/job/create \
  --header "Authorization: Bearer $SHORTAPI_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "google/veo-3.1/text-to-video",
    "args": {
      "prompt": "A cinematic drone shot flying over a futuristic city at sunset"
    }
  }')
JOB_ID=$(echo "$response" | grep -o '"job_id": *"[^"]*"' | sed 's/"job_id": *//; s/"//g')
```

### Step 4: Fetch Generation Status (Background Polling)

Use the returned `job_id` to poll the query API:

```bash
curl --request GET \
  --url "https://api.shortapi.ai/api/v1/job/query?id=$JOB_ID" \
  --header "Authorization: Bearer $SHORTAPI_KEY"
```

## Security & Privacy Compliance

- **Endpoint Isolation**: This skill only communicates with `https://api.shortapi.ai`.
- **Callback Lockdown**: The `callback_url` parameter is strictly user-defined. The Agent is prohibited from auto-generating or hallucinating this value.
- **Credential Safety**: The `SHORTAPI_KEY` is only used in the `Authorization` header to the official API endpoint and must never be included in any callback payload.

**CRITICAL BEHAVIOR FOR AGENTS:**

1.  **Authentication First (SHORTAPI_KEY)**: Before any other step, you **MUST** verify if the user has a `SHORTAPI_KEY`. If it is missing, you **MUST** proactively direct the user to [https://shortapi.ai](https://shortapi.ai) to obtain their API key. **DO NOT** ask for or accept any other type of API key (e.g., OpenAI, Anthropic, etc.); the only valid key is the `SHORTAPI_KEY` from ShortAPI.ai.
2.  Before constructing any API request payload, you **MUST** first complete Step 1 — fetch the specific model's skill document from `https://shortapi.ai/api/skill/<model_id>`. **DO NOT** skip this step. **DO NOT** guess or hallucinate parameters. The document returned in Step 1 is the sole source of truth for the model's input schema.
3.  Video generation takes time. Once you receive the `job_id` from Step 3, you **MUST** immediately inform the user that the task has started and release them so they can ask other questions or start new conversations.
4.  You **MUST** continue to poll the status endpoint in the background silently.
5.  Once the polling returns a completed state (`status: "succeeded"`), you must proactively message the user with the final generation results (e.g., displaying the generated video URLs returned in the response payload).
6.  When presenting results, you **MUST** not only provide the raw URL but also render the content inline for direct preview in the chat. For videos, use an HTML `<video controls src="video_url"></video>` tag to embed an inline video player. For images, use markdown image syntax `![description](image_url)`. For audio/music, use an HTML `<audio controls src="audio_url"></audio>` tag. The user should be able to see and play the generated result immediately without needing to open a separate browser tab.
