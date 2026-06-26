---
name: tripo3d
description: Tripo3D AI 3D model generation. Use when generating 3D models from text prompts or images via the Tripo3D API. Supports Text-to-3D, Image-to-3D, Multiview-to-3D, model refinement, polling, and batch generation. Triggered by requests like "generate a 3D model", "text to 3D", "image to 3D", "photo to 3D", "create 3D from photo", or when the user provides a Tripo3D API token.
---

# Tripo3D AI 3D Generation Skill

## Overview

Tripo3D is a leading AI 3D generation platform. This skill handles:
- **Text → 3D**: Natural language prompt to 3D model
- **Image → 3D**: Single image to 3D model (photo to 3D)
- **Multiview → 3D**: 4 images (front/left/back/right) to higher fidelity 3D
- **Refine Model**: Enhance an existing draft model
- **Polling**: Check generation status and retrieve results
- **Download**: GLB/FBX model files + preview images

## Setup

Requires `TRIPO3D_API_KEY` environment variable.

Get your API key at: https://platform.tripo3d.ai

### Proxy Configuration (Windows + Clash Verge)

Clash Verge (verge-mihomo) proxy port: **7897** — not 7890.

Use PowerShell for all API calls:
```powershell
Invoke-RestMethod -Uri '...' -Proxy 'http://127.0.0.1:7897' -ProxyUseDefaultCredentials
```

For file downloads, use .NET WebClient:
```powershell
$wc = New-Object System.Net.WebClient
$wc.Proxy = New-Object System.Net.WebProxy("http://127.0.0.1:7897")
$wc.Proxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials
$wc.DownloadFile($url, $outPath)
```

Python SDK (aiohttp) does NOT respect system proxy — use PowerShell instead.

## Base URL

```
https://api.tripo3d.ai/v2/openapi
```

All requests require header:
```
Authorization: Bearer <TRIPO3D_API_KEY>
Content-Type: application/json
```

## Core Endpoints

| Action | Method | Path |
|--------|--------|------|
| Create task | POST | `/task` |
| Check status | GET | `/task/{task_id}` |
| Upload image (STS) | POST | `/upload/sts` |
| Get balance | GET | `/user/balance` |

## Task Types

All generation uses `POST /task` with different `type` field values:

| Type | Description |
|------|-------------|
| `text_to_model` | Text prompt → 3D model |
| `image_to_model` | Single image → 3D model |
| `multiview_to_model` | 4 images (front/left/back/right) → 3D model |
| `refine_model` | Refine an existing draft model |

---

## Workflow 1: Text to 3D

**Step 1 — Create task**
```
POST /v2/openapi/task
```
```json
{
  "type": "text_to_model",
  "prompt": "a fierce tiger with orange and black stripes"
}
```

**Step 2 — Poll status**
```
GET /v2/openapi/task/{task_id}
```
Poll every 5–10 seconds. Done when `status === "success"`.

**Step 3 — Download model**
From response: `data.output.pbr_model.url`

---

## Workflow 2: Image to 3D

**Step 1 — Upload image (STS)**
```
POST /v2/openapi/upload/sts
Content-Type: multipart/form-data
```
Form field: `file` (JPEG/PNG/WEBP, max 10MB, min 256px)

Response:
```json
{ "code": 0, "data": { "image_token": "uuid-xxx" } }
```

**Step 2 — Create image-to-3D task**
```
POST /v2/openapi/task
```
```json
{
  "type": "image_to_model",
  "file": {
    "type": "jpg",
    "file_token": "<image_token>"
  }
}
```

Or use image URL directly (no upload needed):
```json
{
  "type": "image_to_model",
  "file": {
    "type": "jpg",
    "url": "https://example.com/photo.jpg"
  }
}
```

**Step 3 — Poll status** (same as Text-to-3D)

**Step 4 — Download model**

---

## Workflow 3: Multiview to 3D

Upload 4 images (front, left, back, right), then:
```
POST /v2/openapi/task
```
```json
{
  "type": "multiview_to_model",
  "files": [
    { "type": "jpg", "file_token": "<front_token>" },
    { "type": "jpg", "file_token": "<left_token>" },
    { "type": "jpg", "file_token": "<back_token>" },
    { "type": "jpg", "file_token": "<right_token>" }
  ]
}
```
Front image is required; other 3 can be empty `{}`.

---

## Workflow 4: Refine Model

```
POST /v2/openapi/task
```
```json
{
  "type": "refine_model",
  "draft_model_task_id": "<task_id_of_draft>"
}
```
Note: Only works with `model_version < v2.0-20240919` drafts.

---

## Common Parameters

| Parameter | Applies to | Description |
|-----------|-----------|-------------|
| `model_version` | all | Version: `P1-20260311`, `Turbo-v1.0-20250506`, `v3.1-20260211`, `v3.0-20250812`, `v2.5-20250123` (default), `v2.0-20240919`, `v1.4-20240625` |
| `texture` | all | Enable texture, default `true` |
| `pbr` | all | Enable PBR, default `true` |
| `texture_quality` | all | `"detailed"` or `"standard"` (default) |
| `face_limit` | all | Limit polygon count (1000~20000) |
| `quad` | text/image | `true` → FBX output (not GLB) |
| `compress` | all | `"geometry"` for compressed output |
| `auto_size` | all | Scale to real-world meters |
| `texture_alignment` | image/multiview | `"original_image"` or `"geometry"` |
| `model_seed` | all | Integer, reproducible generation |
| `texture_seed` | all | Integer, reproducible texture |
| `enable_image_autofix` | image/multiview | Auto-enhance input image |
| `generate_parts` | text/image | Segmentation mode |

### P1-20260311 (Low-poly optimized)
Use for game assets, stylized/low-poly models. Only supports: `model_version`, `model_seed`, `face_limit` (48~20000), `texture`, `pbr`, `texture_seed`, `texture_quality`, `auto_size`, `compress`, `export_uv`.

---

## Polling Logic

⚠️ Generation is asynchronous. Poll every 5–10 seconds.

Status values:
- `queued` → waiting in queue
- `running` → actively generating
- `success` → done, use `output`
- `failed` / `banned` / `expired` / `cancelled` → check error

Never block with `sleep`. Submit job, reply with `task_id`, poll only when user asks.

---

## Download

Model URLs expire after ~5 minutes. Download immediately after success.

Use .NET WebClient (PowerShell):
```powershell
$wc = New-Object System.Net.WebClient
$wc.Proxy = New-Object System.Net.WebProxy("http://127.0.0.1:7897")
$wc.Proxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials
$wc.DownloadFile($modelUrl, $outPath)
```

Output files from `data.output`:
- `pbr_model.url` → GLB file (main model)
- `generated_image.url` → AI concept preview image
- `rendered_image.url` → Model rendering preview

---

## Cost

| Task | Credits |
|------|---------|
| Text-to-3D | ~20 |
| Image-to-3D | ~20 |
| Multiview-to-3D | ~20 |
| Refine Model | ~20 |

Check balance: `GET /v2/openapi/user/balance`

---

## Error Handling

| Code | Meaning |
|------|---------|
| 2010 | Insufficient credit |
| 2001 | Task not found (wrong task_id or API key mismatch) |
| 2002 | Unsupported task type |
| 2003 | Empty input file |
| 2004 | Unsupported file type |
| 429 2000 | Rate limited — retry later |

---

## Windows PowerShell Upload Example

```powershell
$headers = @{
  'Authorization' = 'Bearer <API_KEY>'
}
$filePath = "C:/path/to/image.jpg"
$response = Invoke-RestMethod -Uri 'https://api.tripo3d.ai/v2/openapi/upload/sts' `
  -Method POST `
  -Headers $headers `
  -ContentType 'multipart/form-data' `
  -Proxy 'http://127.0.0.1:7897' `
  -ProxyUseDefaultCredentials `
  -Body @{
    file = Get-Item $filePath
  }
$imageToken = $response.data.image_token
```
