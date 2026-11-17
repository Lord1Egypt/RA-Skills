# Errors and Recovery

| Condition | Action |
| --- | --- |
| 400 validation error | Describe the endpoint again and remove unsupported fields. |
| 401 | Configure a valid `SOCQ_API_KEY`. |
| 402 | Check the balance and reduce scope; do not retry unchanged. |
| 403 | Check API-key status and IP allowlist. |
| 409 idempotency conflict | Use the original input or a new idempotency key. |
| 429 | Respect `Retry-After`; distinguish request-rate and credit-window limits. |
| Task `failed` | Read `error_message`; do not create a duplicate task automatically. |
| MCP tool unavailable | Check URL `platforms`/`tools` filters or reconnect in compact mode. |
| Poll timeout | Preserve the task ID and resume polling later. |

SocQ may switch among configured data providers. Report the final normalized error to the user; do not expose raw credentials or assume a provider-specific error means the endpoint is permanently unsupported.
