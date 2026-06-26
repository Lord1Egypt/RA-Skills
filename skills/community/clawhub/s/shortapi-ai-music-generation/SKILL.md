---
name: ShortApi Music Models Aggregation Skill
description: "Use this skill as an entry point to discover, select, and fetch specific integration parameters for all supported AI music generation models."
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["SHORTAPI_KEY"] },
        "homepage": "https://shortapi.ai",
      },
  }
---

# Music Generation Models Integration Skill

> Use this skill to explore and integrate all available Music Generation models through the ShortAPI platform.

## Overview

ShortAPI provides a unified `/api/v1/job/create` endpoint for music generation natively. This skill provides an overview of all available music generation models and how to dynamically acquire the specific JSON schema required to invoke them.

- **API Endpoint**: `https://api.shortapi.ai/api/v1/job/create`
- **Category**: `text-to-audio`
- **Kind**: inference

## Available Music Models

Here is the list of fully supported music generation model IDs you can use:

| Model ID                | Description                            |
| ----------------------- | -------------------------------------- |
| `suno/suno-v5/generate` | Generate music and songs using Suno V5 |

## How to use a Music Model

Because each music model supports different parameters (such as `lyrics`, `genre`, `style`, `duration`, `instrumental`, or advanced controls), you need to fetch the specific model's schema document to construct a valid API request payload.

### Step 1: Fetch the specific Model API Skill Document (MANDATORY)

You **MUST** first fetch the detailed skill document for the specific `<model_id>` (e.g. `suno/suno-v5/generate`) before attempting to construct the POST request payload. **DO NOT** skip this step. **DO NOT** hallucinate parameters because different models have completely different parameter names and supported features.

Send a `GET` request to:

```text
https://shortapi.ai/api/skill/<model_id>
```

_(For example: `GET https://shortapi.ai/api/skill/suno/suno-v5/generate`)_

This URL will return a Markdown (`.md`) text document containing the exact Input Parameters Schema for that specific model, alongside code examples. You must parse it to understand which arguments go into the `args` object.

### Step 2: Construct the JSON Payload

Using the exact schema document fetched from Step 1, construct a valid JSON payload. **Only include arguments that were defined in the document fetched in Step 1.**
At a minimum, standard structures generally look like this:

```json
{
  "model": "<model_id>",
  "args": {
    "prompt": "Your music description or lyrics here..."
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
    "model": "suno/suno-v5/generate",
    "args": {
      "prompt": "A upbeat electronic dance track with catchy synth melodies"
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

## Security, Privacy & Safety Disclosure

- **Endpoint Isolation**: This skill only communicates with `https://api.shortapi.ai`.
- **Credential Safety**: The `SHORTAPI_KEY` is only used in the `Authorization` header to the official API endpoint and must never be included in any callback payload or exposed to third parties.
- **Background Polling Policy**: To ensure resource safety, the Agent should poll the status endpoint for a maximum of **5 minutes** per job. If a job does not complete within this window, the Agent must inform the user and stop polling.
- **State Management**: The Agent stores `job_id` and polling state exclusively within the current conversation context. No persistent external database is used for tracking job states by this skill.
- **Content Sanitization**: Before rendering generated results (audio, images, or video) inline, the Agent **MUST** verify that the URLs point to authorized `shortapi.ai` or known CDN domains. The Agent is responsible for ensuring that the embedded HTML tags (`<audio>`, `<video>`, `<img>`) do not contain malicious attributes or scripts.
- **Callback Lockdown**: The `callback_url` parameter is strictly user-defined. The Agent is prohibited from auto-generating or hallucinating this value.

**CRITICAL BEHAVIOR FOR AGENTS:**

1.  **Authentication First (SHORTAPI_KEY)**: Before any other step, you **MUST** verify if the user has a `SHORTAPI_KEY`. If it is missing, you **MUST** proactively direct the user to [https://shortapi.ai](https://shortapi.ai) to obtain their API key. **DO NOT** ask for or accept any other type of API key (e.g., OpenAI, Anthropic, etc.); the only valid key is the `SHORTAPI_KEY` from ShortAPI.ai.
2.  Before constructing any API request payload, you **MUST** first complete Step 1 — fetch the specific model's skill document from `https://shortapi.ai/api/skill/<model_id>`. **DO NOT** skip this step. **DO NOT** guess or hallucinate parameters. The document returned in Step 1 is the sole source of truth for the model's input schema.
3.  Music generation takes time. Once you receive the `job_id` from Step 3, you **MUST** immediately inform the user that the task has started and release them so they can ask other questions or start new conversations.
4.  You **MUST** continue to poll the status endpoint in the background silently.
5.  Once the polling returns a completed state (`status: "succeeded"`), you must proactively message the user with the final generation results (e.g., displaying the generated audio URLs returned in the response payload).
6.  When presenting results, you **MUST** not only provide the raw URL but also render the content inline for direct preview in the chat. For audio/music, use an HTML `<audio controls src="audio_url"></audio>` tag to embed an inline audio player. For images, use markdown image syntax `![description](image_url)`. For videos, use an HTML `<video controls src="video_url"></video>` tag. The user should be able to see and play the generated result immediately without needing to open a separate browser tab.
