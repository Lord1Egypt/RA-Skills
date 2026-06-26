# Threads FastAPI (OpenClaw Skill)

This OpenClaw skill lets an agent **queue / schedule / publish** content to Threads by calling **your FastAPI backend**.

It is designed for the common setup where:
- the skill is public/open (easy install)
- the **backend is your product** (hosted API, billed to customers)

## What it does

- Calls `POST {BASE}/api/v1/threads/publish` to enqueue or publish a Threads post
- (Optional) Calls `POST {BASE}/api/v1/assistant/chat` if you implement assistant-style generation on the backend

## Requirements

Set these environment variables on the OpenClaw Gateway host:

- `THREADS_FASTAPI_BASE_URL` (example: `https://api.yourdomain.com`)
- `THREADS_QUEUE_SECRET` (sent as `X-Queue-Secret` to `/threads/publish`)
- Optional: `THREADS_TENANT_ID` (default: `agency_paris`)

## How to use (agent)

When the user asks to **generate**, **queue**, **schedule**, or **publish** Threads content, the agent should call this skill.

### Queue a post (example payload)

`POST {BASE}/api/v1/threads/publish` with:

```json
{
  "message": "<post text>",
  "images": [],
  "scheduled_at": null,
  "publish_mode": "queue",
  "auto_proxy_images": true,
  "meta": {
    "tenant_id": "agency_paris",
    "source": "openclaw"
  }
}
```

## Helper scripts

- `publish.ps1`: generic HTTP POST helper (adds `X-Queue-Secret` header)
- `threads_publish_and_poll.ps1`: convenience script that publishes and optionally polls job status

## Security notes

- **Never** hardcode secrets in the repo.
- `THREADS_QUEUE_SECRET` must be provided via environment variables.
- Prefer HTTPS for `THREADS_FASTAPI_BASE_URL`.

## License

MIT (see `LICENSE`).
