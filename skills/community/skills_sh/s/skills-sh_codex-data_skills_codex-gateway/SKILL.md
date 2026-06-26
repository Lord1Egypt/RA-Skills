---
name: codex-gateway
description: >-
  Use when the user wants to query the Codex Supergraph and the server returns
  a 402 challenge. Pays per query via the MPP 402 challenge flow. Only supports
  queries, not mutations or subscriptions.
metadata:
  author: codex-data
  version: "1.0"
---

# Codex Machine Payment Protocol (MPP)

Use this skill when the [Codex](https://www.codex.io) Supergraph returns a `402 Payment Required` response. The MPP challenge flow lets you pay per query without needing an API key. For higher volume, get an API key at [dashboard.codex.io/signup](https://dashboard.codex.io/signup) — see [docs.codex.io](https://docs.codex.io) for details.

|                       |                                                                 |
| --------------------- | --------------------------------------------------------------- |
| HTTP endpoint         | `https://graph.codex.io/graphql`                                |
| Credential header     | `Authorization: Payment <base64url-credential>`                 |

## How it works

1. Send a GraphQL query (no credential).
2. Server returns `402 Payment Required` with `WWW-Authenticate: Payment ...` challenges.
3. Client solves one challenge and retries with `Authorization: Payment <credential>`.
4. Server returns GraphQL data + `Payment-Receipt` header.

## Constraints

- **Query only.** Mutations and subscriptions return `403` in MPP mode.
- If a valid API key or bearer token is also present, API auth takes precedence.

## Rules

- Never print raw credentials.
- Only use MPP for `query` operations.
- **Before constructing any query**, read `references/query-templates.md` below for the correct GraphQL schema. Do not guess query or field names.

## References

| File | Purpose |
| ---- | ------- |
| [../codex-supergraph/references/query-templates.md](../codex-supergraph/references/query-templates.md) | **GraphQL query schema and examples — read before constructing queries** |
| [../codex-supergraph/references/gotchas.md](../codex-supergraph/references/gotchas.md) | Common query failure points |
| [references/gotchas.md](references/gotchas.md) | MPP-specific failure points |
| [rules/wallets.md](rules/wallets.md) | Wallet setup: tempo wallet/request (Tempo) |
| [references/mpp-flow.md](references/mpp-flow.md) | Auth matrix, challenge details, error codes |

## Links

- Website: [www.codex.io](https://www.codex.io)
- Documentation: [docs.codex.io](https://docs.codex.io)
- Get an API key: [dashboard.codex.io/signup](https://dashboard.codex.io/signup)
