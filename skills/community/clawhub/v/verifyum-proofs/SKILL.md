---
name: verifyum-proofs
description: Prove that exact file bytes existed at a point in time with Verifyum, anchored on Solana Mainnet without uploading the file, and check Verifyum proofs. No account or key. An anchor is a permanent public transaction, so anchor only when the user asks.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://verifyum.com/agents
---

# Verifyum proofs

Verifyum proves that a commitment to exact file bytes existed no later than a
Solana Mainnet block time. The file stays on the machine. Only a
domain-separated commitment is sent, and the public proof holds nothing that
identifies the file. The service is run by AI SENSE AS.

## Setup, once

This skill cannot add the servers for you. Add the hosted server with the
OpenClaw CLI (its documentation runs saved-server edits with the Gateway
stopped) or in Settings, MCP, Add server while the Gateway runs:

```bash
openclaw mcp add verifyum --url https://api.verifyum.com/mcp --transport streamable-http
openclaw mcp doctor verifyum --probe
```

The probe lists three tools. If it lists none, the server is not reachable
from this machine. Stop and tell the user.

The file tool needs the local server as well. Add an MCP server named
`verifyum-local` with command `npx`, arguments `-y verifyum-mcp@0.1.1`, and
the environment variable `VERIFYUM_MCP_ALLOWED_DIRS` set to the folder that
holds the files. It needs Node.js 20 or later.

## Which tool for what

`verifyum` is the hosted server with three tools. `verifyum-local` runs on
this machine and has the same three plus the file tool. When both are
connected, use `verifyum-local`.

- **Prove a local file**: `verifyum_create_proof_from_file` on
  `verifyum-local`, with `path` and a `private_draft_path` that does not exist
  yet. It hashes the file, builds the nonce and private manifest, saves the
  private draft and anchors only the commitment. The answer has `proof_id`,
  `status`, `proof_url` and `private_draft_path`.
- **Anchor a commitment that already exists**: `verifyum_anchor_commitment`
  with `commitment` and `idempotency_key`. Use it only for a commitment built
  by Verifyum's own code: the local server, the single-file clients
  https://verifyum.com/clients/verifyum.py and
  https://verifyum.com/clients/verifyum.mjs, or
  https://verifyum.com/assets/verifyum-protocol.js. Never build the manifest
  or the commitment by hand. A wrong commitment is anchored all the same and
  will never match the file.
- **Follow a proof until it settles**: `verifyum_get_proof` with `proof_id`.
  The status is `queued`, `submitted`, `finalized` or `failed`.
- **Check a proof**: `verifyum_verify_public_proof` with `proof_id`. On
  `verifyum-local` it checks the Ed25519 service signature against the
  published key registry and also reads the transaction from a public Solana
  RPC endpoint without going through Verifyum. On the hosted `verifyum`
  server, Verifyum checks its own data and returns the exact RPC request, so
  the chain part can be confirmed separately. Tell the user which one ran.

## Rules

- Anchor only when the user has asked for a proof of that specific file or
  record. Never anchor while testing the connection, exploring, guessing what
  the user might want, working in bulk, or as a side effect of another task.
- Every anchor is a real, public and permanent Solana Mainnet transaction. It
  cannot be withdrawn. Public use is currently free and AI SENSE AS pays the
  network fee. That is current policy, not a guarantee.
- Never send the file, its name, its raw hash, the nonce or the private
  manifest to Verifyum, to a URL or into a message. The tools take only a
  commitment, an idempotency key, a public proof ID, or a local path on
  `verifyum-local`.
- The private draft ties the proof to the file and cannot be recreated. Tell
  the user to keep it next to the original. Do not print its contents.
- Retry with the same commitment and the same idempotency key. For the file
  tool, call again with the same `path` and `private_draft_path`, which
  resumes the saved draft. Never retry in parallel. Honor HTTP 429 and
  `Retry-After`.
- Public creation allows at most ten new anchors per rolling hour per IP
  address, with lower daily caps. For many records, keep a local hash chain
  and anchor its head.
- If the file tool answers that it is not configured, `VERIFYUM_MCP_ALLOWED_DIRS`
  is not set for `verifyum-local`. Tell the user which folder needs to be
  listed there and stop. Do not compute the commitment some other way.

## What a proof shows

A finalized proof shows that a commitment to the exact file bytes existed no
later than the estimated Solana block time, and that those bytes have not
changed since. It does not prove authorship, ownership, legal signature
validity, when the file was first created, or that its contents are true. Say
this plainly when you hand over a proof URL.

## Verify the connection

This check reads a public proof and never anchors anything.

1. Call `verifyum_get_proof` with proof ID `72c38s8rrqa4vjhw6dxsvmbqkq`. The
   answer is status `finalized` on network `mainnet-beta`.
2. Call `verifyum_verify_public_proof` with the same ID. The verdict is
   `valid`. On `verifyum-local` the chain checks report slot `442907852` and
   block time `2026-08-30T14:59:44Z`. The hosted server gives the same slot
   under `chain_check.expect`.

Any other answer means the call did not reach Verifyum or something is wrong.
Stop and tell the user.

Reference: https://verifyum.com/agents and https://verifyum.com/docs/agent-api.md
