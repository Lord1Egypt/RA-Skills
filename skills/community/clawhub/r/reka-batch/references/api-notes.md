# Reka Batch API notes

Condensed from https://developer.reka.ai/batch, /batch/results, /batch/reference and /pricing as of
2026-10-28. The Batch API is in beta; check those pages when something here disagrees with reality.

## Surface

OpenAI-compatible. Base URL `https://api.reka.ai/v1`, header `Authorization: Bearer $REKA_API_KEY`.
The OpenAI Python and TypeScript SDKs work unchanged with that base URL.

| Call | Purpose |
|---|---|
| `POST /v1/files` (multipart, `purpose=batch`) | Upload a JSONL request file. No idempotency key. |
| `GET /v1/files?purpose=batch&limit=&order=&after=` | List files (find an upload whose reply was lost). |
| `GET /v1/files/{id}/content` | Download a file (inputs, results, errors). |
| `DELETE /v1/files/{id}` | Delete; HTTP 409 if it is the input of an unfinished batch. |
| `POST /v1/batches` | Create: `input_file_id`, `endpoint: /v1/chat/completions`, `completion_window: 24h`, optional `metadata` (16 pairs). Optional `Idempotency-Key` header. |
| `GET /v1/batches/{id}` | Status, `request_counts`, `usage`, `output_file_id`, `error_file_id`. |
| `GET /v1/batches?limit=&after=` | List, newest first. |
| `POST /v1/batches/{id}/cancel` | Cancel; finished rows are kept and billed. |

No webhooks: poll for status.

## Limits

- Models: `glm5.3-flash`, `qwen3.8-27b`. One model per file. Endpoint `/v1/chat/completions` only.
- Up to 50,000 requests and 100 MB per file; UTF-8 JSONL, one request per line.
- `custom_id` unique per file, up to 512 characters.
- Tools and structured outputs work as in Chat Completions; `stream: true` is rejected.
- Rows not finished within 24 hours expire.
- Turnaround measured 2026-10-28 on 12-50 row jobs: 6-10 s, or 95 s with `reasoning_effort: "high"`.
  The 24-hour window is a ceiling, not a typical wait.

## Prefix caching

Measured on the live API (2026-10-28), the same live and in batch:

- No cache-read tokens at all below 1,024 prompt tokens.
- Above that, `cached_tokens` is the prompt length rounded down to 640-token blocks, minus one block
  (prompt 1,444 → 640 cached; 3,264 → 2,560; 4,778 → 3,840).
- A repeated prefix is only a hit if an earlier request with that exact prefix was already served;
  the first row of a batch pays full price.
- `cached_tokens` and `created_cache_tokens` come back in `usage.prompt_tokens_details` per row, and
  summed in `usage.input_tokens_details` on the batch object. `collect` reports both.

## Statuses

`validating` → `in_progress` → `finalizing` → `completed`. Also `failed` (the input file was
invalid; see `errors.data` with line numbers), `cancelling`/`cancelled`, and `expired` (the window
ended; finished rows are still in the result files).

A `completed` batch can contain failed rows: check `request_counts` and the error file.

## Result rows

Every line has `custom_id` and either `response` (`status_code`, `request_id`, `body` = a normal
chat completion) or `error` (`code`, `message`). Rows can arrive in any order.

- Succeeded: `error` null, `response.status_code` 200.
- Rejected by the model endpoint: `error` null, non-200 `status_code`.
- Never ran: `error.code` `batch_expired` or `batch_cancelled`.
- Empty `content` with `finish_reason: length`: thinking used the `max_tokens` budget.

Measured 2026-10-28 on `qwen3.8-27b` in batch: `reasoning_effort: "none"` returns
`reasoning_tokens: 0` and a normal answer (50/50 rows valid JSON at `max_tokens: 256`), while
`"high"` bills about 127 reasoning tokens per row for the same prompt. So the switch works through
the gateway, and short labels do not need extra headroom when it is set.

## Errors when calling the API

| HTTP | Meaning | Action |
|---|---|---|
| 400 / 422 | Bad request | Fix it. |
| 401 | Bad key | Check `REKA_API_KEY`. |
| 403 | No credit left, or the key cannot use batch | Top up or use another key. |
| 404 | Wrong, deleted or someone else's id | Check the id. |
| 409 | Idempotency key reused with a different body; or deleting a busy input file | Use a new key; wait. |
| 429 `batch_queue_full` | Queue full | Wait for `Retry-After` (currently 300 s), create again with the same file. |
| timeout / 5xx | Unknown outcome | Retry; for create reuse the idempotency key; for uploads list files first. |

If the account runs out of credit mid-batch, rows not yet started fail with 403. Revoking the key
that created a batch stops it within about a minute.

## Prices (USD per million tokens)

| Model | Live input | Live cached | Live output | Batch input | Batch cached | Batch output |
|---|---|---|---|---|---|---|
| `glm5.3-flash` | 0.15 | 0.015 | 0.50 | 0.075 | 0.0075 | 0.25 |
| `qwen3.8-27b` | 0.20 | 0.05 | 2.50 | 0.10 | 0.025 | 1.25 |

Reasoning tokens bill as output. Refusals and cut-off answers bill like any answer. Rows that never
ran are free; a batch that failed validation is free. Each row is billed at the batch rate in
force when it runs. Reka's worked example: 1M input + 1M output on `qwen3.8-27b` costs $1.35 in a
batch against $2.70 live.

## Retention

Live requests to these models store nothing. A batch must hold the requests until it runs, so Reka
keeps them until it finishes, then deletes its copies. Your input and result files stay until you
delete them, or 31 days after upload. Download results before then.
