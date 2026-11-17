# UnifyPort Device API overview

[English](overview.md) | [简体中文](../zh-CN/overview.md)

## Public boundary

This Skill covers the API content published at [UnifyPort API documentation](https://www.unifyport.ai/docs/#introduction): workspace, accounts, authentication, runtime, messages, conversations, contacts, groups, API keys, webhook endpoints, provider regions, provider guides, errors, and standard webhook events.

The fixed API origin is `https://api.unifyport.ai`. Live requests authenticate with `X-Api-Key`, sourced only from the optional `UNIFYPORT_API_KEY` environment variable.

Use `../operations.json` to resolve an action and `../events.json` to resolve an event type. Those catalogs are the executable allowlists; never derive an undocumented operation from a guessed path or a server response.

## Modes

### `docs-only`

Use for explanations, request preparation, code examples, provider capability questions, error interpretation, and webhook design. Do not read the API key and do not send network traffic.

### `read`

Use only when the user explicitly requests current workspace data. Resolve one allowlisted read action, show the target and redacted parameters, then execute with the bundled runner. Use `--input-stdin` whenever the actual request contains a sensitive identifier or value. Minimize page size and summarize sensitive records.

### `write`

Use for an allowlisted state-changing action only after showing a redacted preview and obtaining the catalog-defined confirmation. Sensitive request input uses a complete `{params,query,body}` object through `--input-stdin`; the same object is supplied again for confirmed execution. The confirmation is invalid if any normalized input changes.

### `credential`

Use for allowlisted authentication, session, password, API-key, or signing-secret handling only when the user explicitly opts in. Send the complete request through `--input-stdin`. Never request a secret in chat, pass it as a command argument, or reproduce it in normal output.

Destructive actions are a stricter subset of `write` and require explicit destructive intent.

## Public concepts

- A workspace is the isolation boundary resolved by the API key.
- An account represents one provider login and exposes authentication and runtime state.
- Messages use normalized request shapes, while actual support varies by provider.
- Webhooks deliver inbound traffic and lifecycle events; verify signatures and store only what the application needs.
- Responses include a `request_id`; use it when reporting a failure without attaching sensitive bodies.

For detailed semantics, follow the English or Simplified Chinese URL stored on the selected catalog entry.
