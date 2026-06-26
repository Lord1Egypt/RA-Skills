# Loova Seedance 2.0 Video API Reference

## Authentication

- Obtain your API key after logging in at [https://loova.ai/](https://loova.ai/).
- All requests must include the header: `Authorization: Bearer <API_KEY>`.

## 1. Submit Task: POST /api/v1/video/seedance-2

This is the **single** Seedance 2.0 generation endpoint for both:

- Text-to-video (no media inputs)
- Image-to-video / video reference / audio reference (optional media inputs)

- **URL**: `https://api.loova.ai/api/v1/video/seedance-2`
- **Method**: POST
- **Headers**:
  - With file upload (`files` provided): `Authorization: Bearer <API_KEY>` and use **multipart/form-data**
  - Without file upload: `Authorization: Bearer <API_KEY>`, `Content-Type: application/json`
- **Body**:
  - multipart/form-data: flat fields at the top level (`model`, `prompt`, etc.), optional `files` parts
    - For list fields like `image_urls`, send **repeated form keys** (e.g. multiple `image_urls` entries)
  - application/json: `{ "model": string, "prompt": string, ... }` (all params at the top level)


| Field                 | Type          | Required | Description                                                                                       |
| --------------------- | ------------- | -------- | ------------------------------------------------------------------------------------------------- |
| `model`               | string        | Yes      | `seedance_2_0` or `seedance_2_0_fast`                                                             |
| `prompt`              | string        | Yes      | Prompt; supports @ reference syntax                                                               |
| `functionMode`        | string        | No       | `first_last_frames` (first/last frame) / `omni_reference` (omni mode)                             |
| (multipart) `files`   | File[]        | No       | Optional media files (images/video/audio) sent as multipart/form-data File parts                  |
| `image_urls`          | string[]      | No       | Optional image URL list                                                                           |
| `video_urls`          | string[]      | No       | Optional video URL list                                                                           |
| `audio_urls`          | string[]      | No       | Optional audio URL list                                                                           |
| `ratio`               | string        | No       | Video aspect ratio, default `16:9`                                                                |
| `aspect_ratio`        | string        | No       | Video aspect ratio (legacy), default `16:9`                                                       |
| `duration`            | number/string | No       | Duration in seconds, 4–15, default `5`                                                            |


**Response**: Contains `task_id` for polling the result.

## 2. Get Result: GET /v1/tasks

- **URL**: `https://api.loova.ai/v1/tasks?task_id=<task_id>`
- **Method**: GET
- **Headers**: `Authorization: Bearer <API_KEY>`
- **Usage**:
  - Clients (including OpenClaw) should **poll about once per minute** until the task status is completed or failed.
  - Video generation can take up to **several hours**, so keep polling (or use a long timeout) accordingly.
  - As soon as the status indicates success/completed and a video URL/result is available, clients (including OpenClaw) should **immediately surface the result to the end user** without additional delay.

