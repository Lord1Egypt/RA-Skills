---
name: threads_fastapi
description: Call the user's FastAPI backend to queue/generate/publish Threads posts.
---

# Threads FastAPI skill

Use this skill whenever the user asks to **generate**, **queue**, **schedule**, or **publish** content to Threads.

## Required environment variables (on the Gateway host)

- `THREADS_FASTAPI_BASE_URL` (example: `http://127.0.0.1:8000`)
- `THREADS_QUEUE_SECRET` (the value to send as `X-Queue-Secret`, only for `/threads/publish`)
- Optional: `THREADS_TENANT_ID` (default: `agency_paris`)

If these are missing, ask the user for the correct values.

## Storage options (backend-side)

This skill does not store media itself. Storage is handled by the FastAPI backend.

### Local Pack (demo / single machine)
Set on the backend:

```
STORAGE_PROVIDER=local
UPLOADS_DIR=uploads
UPLOADS_PATH=/uploads
```

This stores uploads in `UPLOADS_DIR` and serves them from `UPLOADS_PATH`.

### Cloud storage (prod)
Set `STORAGE_PROVIDER=cloudinary` or `s3` on the backend and configure the
provider credentials there.

## Endpoints (per your spec)

- `POST {BASE}/api/v1/threads/publish`
  - Requires header `X-Queue-Secret`
- `POST {BASE}/api/v1/assistant/chat`
  - No queue secret header (unless your backend requires it later)

Both accept JSON.

## How to call (safe)

Use the **HTTP tool** in OpenClaw (not `exec`).  
Send JSON directly to the FastAPI endpoint with the required headers.

Example:
- URL: `{BASE}/api/v1/threads/publish`
- Method: `POST`
- Headers: `X-Queue-Secret: <THREADS_QUEUE_SECRET>`
- Body: JSON payload (see below)

## Payloads

### A) Publish / enqueue Threads post

Call `POST {BASE}/api/v1/threads/publish` with:

```json
{
  "message": "<message text>",
  "images": [],
  "scheduled_at": null,
  "publish_mode": "queue",
  "auto_proxy_images": true,
  "meta": {
    "tenant_id": "agency_paris",
    "source": "telegram",
    "chat_id": "<tg chat id>",
    "user_id": "<tg user id>",
    "username": "<tg username>"
  }
}
```

### B) /postimg generate+enqueue via assistant

Call `POST {BASE}/api/v1/assistant/chat` with:

```json
{
  "session_id": "tg_<chat id>",
  "execute_tools": true,
  "message": "Generate and enqueue one image post",
  "context": {
    "tenant_id": "agency_paris",
    "prompt": "<tg args>",
    "message": "<tg args>",
    "provider": "replicate",
    "model": "black-forest-labs/flux-1.1-pro",
    "source": "telegram",
    "campaign": "remote_demo",
    "api_base_url": "http://127.0.0.1:8000"
  }
}
```

**Note:** The skill should fill `tenant_id` from `THREADS_TENANT_ID` when set.

## Safety

- Never forward secrets from chat into shell commands except as the `-QueueSecret` argument.
- Do not log the secret.
- Validate that `BaseUrl` is an http(s) URL.
