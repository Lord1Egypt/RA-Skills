# Output envelope

```json
{
  "ok": true,
  "provider": "baidu",
  "text": "# Complete extracted Markdown",
  "result": {
    "task_id": "task-...",
    "status": "success",
    "response": {}
  },
  "artifacts": {
    "markdown_url": "https://...",
    "parse_result_url": "https://..."
  },
  "error": null
}
```

For a local provider, `result` contains `backend`, `model`, and `image_count`; `artifacts` is normally empty.

Failure envelope:

```json
{
  "ok": false,
  "provider": "baidu",
  "text": "",
  "result": null,
  "artifacts": {},
  "error": {
    "code": "API_ERROR",
    "message": "Sanitized error description"
  }
}
```

The stable consumer contract is the top-level envelope. Provider-specific fields under `result.response` may evolve with the upstream service.

