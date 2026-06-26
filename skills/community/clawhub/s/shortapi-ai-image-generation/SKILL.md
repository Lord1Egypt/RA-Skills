---
name: ShortApi Image Models Aggregation Skill
description: "Use this skill as an entry point to discover, select, and fetch specific integration parameters for all supported AI image generation models."
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["SHORTAPI_KEY"] },
        "homepage": "https://shortapi.ai",
      },
  }
---

# Image Generation Models Integration Skill

> Use this skill to explore and integrate all available Image Generation models through the ShortAPI platform.

## Overview

ShortAPI provides a unified `/api/v1/job/create` endpoint for image generation across multiple top-tier providers natively. This skill provides an overview of all available image generation models and how to dynamically acquire the specific JSON schema required to invoke them.

- **API Endpoint**: `https://api.shortapi.ai/api/v1/job/create`
- **Category**: `text-to-image`, `image-to-image`
- **Kind**: inference

## Available Image Models

Here is the list of fully supported image generation model IDs you can use:

| Model ID                                  | Description                           |
| ----------------------------------------- | ------------------------------------- |
| `google/nano-banana-pro/text-to-image`    | Generate images using Nano Banana Pro |
| `google/nano-banana-pro/edit`             | Edit images using Nano Banana Pro     |
| `bytedance/seedream-4.5/text-to-image`    | Generate images using Seedream 4.5    |
| `bytedance/seedream-4.5/edit`             | Edit images using Seedream 4.5        |
| `shortapi/z-image/text-to-image`          | Generate images using Z-Image         |
| `google/nano-banana/text-to-image`        | Generate images using Nano Banana     |
| `google/nano-banana/edit`                 | Edit images using Nano Banana         |
| `midjourney/midjourney-v7/text-to-image`  | Generate images using Midjourney V7   |
| `midjourney/midjourney-v7/image-to-image` | Modify images using Midjourney V7     |
| `shortapi/flux-1.0/text-to-image`         | Generate images using Flux 1.0        |
| `shortapi/flux-1.0/image-to-image`        | Modify images using Flux 1.0          |
| `alibaba/wan-2.6/text-to-image`           | Generate images using Wan 2.6         |
| `alibaba/wan-2.6/image-to-image`          | Modify images using Wan 2.6           |
| `google/nano-banana-2/text-to-image`      | Generate images using Nano Banana 2   |
| `google/nano-banana-2/edit`               | Edit images using Nano Banana 2       |
| `bytedance/seedream-5.0/text-to-image`    | Generate images using Seedream 5.0    |
| `bytedance/seedream-5.0/edit`             | Edit images using Seedream 5.0        |

## How to use an Image Model

Because each image model supports different parameters (such as `aspect_ratio`, `image_size`, `guidance_scale`, or advanced controls natively built into the prompt), you need to fetch the specific model's schema document to construct a valid API request payload.

### Step 1: Fetch the specific Model API Skill Document (MANDATORY)

You **MUST** first fetch the detailed skill document for the specific `<model_id>` (e.g. `google/nano-banana-pro/text-to-image`) before attempting to construct the POST request payload. **DO NOT** skip this step. **DO NOT** hallucinate parameters because different models have completely different parameter names for the same concept (e.g. one model might use `aspect_ratio` while another uses `image_size`).

Send a `GET` request to:

```text
https://shortapi.ai/api/skill/<model_id>
```

_(For example: `GET https://shortapi.ai/api/skill/google/nano-banana-pro/text-to-image`)_

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
    "model": "google/nano-banana-pro/text-to-image",
    "args": {
      "prompt": "An astronaut riding a horse in photorealistic style"
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
3.  Image generation takes time. Once you receive the `job_id` from Step 3, you **MUST** immediately inform the user that the task has started and release them so they can ask other questions or start new conversations.
4.  You **MUST** continue to poll the status endpoint in the background silently.
5.  Once the polling returns a completed state (`status: "succeeded"`), you must proactively message the user with the final generation results (e.g., displaying the generated image URLs returned in the response payload).
6.  When presenting results, you **MUST** not only provide the raw URL but also render the content inline for direct preview in the chat. For images, use markdown image syntax `![description](image_url)` to embed the image. For videos, use an HTML `<video controls src="video_url"></video>` tag. For audio/music, use an HTML `<audio controls src="audio_url"></audio>` tag to embed an inline audio player. The user should be able to see and play the generated result immediately without needing to open a separate browser tab.
