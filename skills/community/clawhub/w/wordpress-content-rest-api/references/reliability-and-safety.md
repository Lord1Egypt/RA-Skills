# Error, Retry, Rate-Limit, and Dry-Run Rules

## Dry-Run First (Mandatory)

Before any write operation:
1. Validate auth with a read call.
2. Fetch target object (or candidate set).
3. Build intended payload and list field-level changes.
4. Validate dependencies (taxonomy/media IDs).
5. Proceed to write only after checks pass.

## Error Handling

Classify failures:
- `400/401/403`: payload/auth/permission issue -> fix input/auth; do not blind retry.
- `404`: wrong endpoint/object ID/environment mismatch.
- `409/412`: state conflict -> re-read object and retry with refreshed state.
- `429`: rate-limited -> back off and retry.
- `5xx`: transient server issue -> bounded retry.

Always capture:
- status code
- response body (sanitized)
- endpoint + method

## Retry Guidance

Retry only idempotent or safely repeatable calls.

Recommended backoff for retryable errors (`429`, `5xx`):
- up to 4 retries
- exponential delays: 1s, 2s, 4s, 8s
- add jitter if running parallel flows

Honor `Retry-After` when present.

## Rate-Limit Guidance

- Keep request bursts small.
- Prefer fewer larger reads (`per_page`) over many tiny calls.
- Serialize writes when content integrity matters.
- Pause bulk operations on repeated `429`.

## Write Safety Guards

- Default to `status=draft`.
- Publish only with explicit user approval.
- For bulk updates, process in batches and verify each batch.
- On first unexpected failure, halt and reassess before continuing.
