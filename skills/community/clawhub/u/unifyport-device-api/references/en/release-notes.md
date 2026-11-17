# Release notes — 1.1.0

[English](release-notes.md) | [简体中文](../zh-CN/release-notes.md)

Status: unreleased candidate. Local validation and a ClawHub dry run do not publish this version. Final human public-evidence review is pending.

## Changes since 1.0.0

- Adds the previously merged public operation tracking, authorization session and Passkey actions, contact membership, conversation history, posts/comments and calls. Coverage is 82 actions, 78 routes and 24 events; counts do not imply unrestricted parameter coverage.
- Documents Facebook session authorization, separate authorized/runtime readiness, E2EE user conversations, single text or single media, partial audio support and four existing standard callbacks. No new Facebook receipt events or inferred duration units.
- Completes nine existing action surfaces: nested WhatsApp Protocol credentials on import-auth-session, label_id on list-conversations, up_to_message_sender_id on mark-conversation-read, and account_id in the documented location for all six Webhook actions.
- Protocol import validates the exact nested schema, required keys, int32/uint32 and boolean types; rejects edge_routing, credential routing through provider_data and non-public upstream addresses. Full stdin, credential opt-in, HMAC and whole-object/scattered-key redaction apply.
- Preserves caller-owned Idempotency-Key confirmation, sparse values, opaque IDs, nanosecond timestamp strings, legacy X session/PIN/proxy inputs, and top-level empty proxy clearing on account PATCH.
- Aligns package metadata, bilingual Skill metadata, runner User-Agent and explicit ClawHub release parameters at 1.1.0. Adds version, evidence and exact-file manifest gates, including ignore-rule attestation and a matching tokenless official CLI dry-run before any upload. Quality tests support both pending and completed human review; uploads only the Skill directory.

## Limits and release conditions

update-account.provider_account_ref remains rejected pending clarification of writable identity semantics. Message aliases keep separate intent-specific allowlists. Provider-specific business validity and Webhook ownership are verified by the server, not inferred locally. Protocol server overrides follow the runner's stricter public-host policy. No live account acceptance is claimed. See [migration](migration.md).
