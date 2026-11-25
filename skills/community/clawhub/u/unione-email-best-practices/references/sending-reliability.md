# Sending reliability

- **Queue every send**: the web request writes a job, a worker calls `email/send`. The user does not wait for the
  API and a provider outage does not break signup.
- **Idempotence**: `idempotence_key` = event + entity (`password-reset-<token_id>`); UniOne declines a repeat
  within one minute. For longer windows keep an "email sent" record per event in your database and check it before
  sending.
- **Retries**: only retryable errors (network errors, timeouts, HTTP 429 and 5xx: `retryable` of the SDK error) →
  retry with backoff and jitter and the same `idempotence_key`, inside the one-minute window (e.g. 1 s, 4 s, 16 s,
  ~45 s). After the window the key no longer protects: check your own "sent" record before sending again (a timeout
  may have sent the message). Other 4xx → log, alert, do not retry unchanged.
- **Partial results**: handle `failed_emails` — mark those recipients, do not retry them blindly. A
  `temporary_unavailable` address keeps failing for the next three days: retry it after that, not in a loop.
- **Webhooks**: answer 200 within 3 seconds, process from a queue, deduplicate, accept out-of-order events.
  After an outage of your endpoint, reconcile the statuses with an event dump (`event-dump/create` for the period).
- **Timeouts**: set a client timeout (10–30 s) — the SDKs do.
- **SMTP limits**: up to 5,000 emails an hour per connection and 10 connections; above that, or when you need
  `failed_emails` at once, use the Web API.
- **Monitoring**: alert on error rates of `email/send`, on webhook signature failures and on a stopped webhook
  (`webhook/list` → `status`).
