# Limits, credits, and batches

Seedance documentation describes credit reservation on submission, settlement on success, and release on failure. Duplicate POSTs can incur multiple charges. No common public cost-estimation, balance, billing, or idempotency API is defined; do not invent quotes or completed refunds.

A clear request for one result normally authorizes its generation. Clarify scope before exceeding counts, repeated alternatives, or materially higher costs. Get a missing batch count; errors/timeouts do not authorize replacement tasks.

Read [Seedance parameters](../api/seedance.md) for model/duration/resolution/reference limits. Separate API limits from creative quality advice.

Subtitle removal handles one video per task, without a public batch, callback, or cancellation contract. Client batches default to sequential execution and retain each ID. Missing pricing/rate-limit details do not imply free use.

[Seedance billing](https://vibbit.apifox.cn/514565013e0) · [Subtitle removal](https://vibbit.apifox.cn/514584287e0)

[Translation](../api/translate_video.md) accepts 1-100 videos/request and up to 16 target languages/video. This is API-specific. Submit/edit/confirm at no more than 2 requests/second; space sequential calls. No cross-process global limiter is supplied. Query every 5-10 seconds. No translation price formula is published; do not apply Seedance's formula.
