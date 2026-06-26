---
name: agent-wallet-open
version: 1.3.0
description: >-
  Mokshya agent-wallet: public REST API + TEE signing (Shamir/AES-GCM). Use when
  debugging wallets.mokshya.io, GKE deploy, create/sign HTTP flows, rate limits,
  or inconsistent agent_id lookups. Teaches correct ID ownership (API not TEE).
metadata:
  openclaw:
    homepage: https://github.com/mokshyaprotocol/agent-tee-wallet
---

# Agent Wallet — open skill

**Single skill file:** **`skills/SKILL.md`**. Cursor loads it via **`.cursor/skills/open`** → `skills/`. ClawHub: `clawhub publish skills`.

**OpenClaw / ClawHub:** Source of truth for how `agent_id` and the TEE interact. Read before inventing “sequence mismatch” or dual-ID theories.

## When to use

- **POST /create-agent-wallet**, **POST /sign-transaction**, **GET /agent/:id**, **GET /user/:username**.
- Production: wrong wallet, signing fails, **`/agent/2` vs `/user/foo` disagree** on who owns an id.
- Deploy: GKE, **DATABASE_URL**, **TEE_BASE_URL**, **INTERNAL_HMAC_SECRET**.

## WRONG hypotheses — do **not** use these

1. **“The TEE allocates `agent_id` and can get out of sync with Postgres.”**  
   **False.** The **API** allocates `agent_id` (`allocUsername`). The TEE receives `agent_id` as a **string** and uses it **only as AES-GCM AAD**. No TEE wallet table or ID sequence. See `api/src/teeClient.ts`, `tee-app/src/index.ts`, `tee-app/src/walletCore.ts`.

2. **“TEE in-memory reset breaks ID alignment.”**  
   **Misleading.** TEE is **stateless** for identities. Ciphertexts live in the **API** (Share B) and **client** (`key_share`).

3. **“Fix by having the TEE return `agent_id` first.”**  
   **Wrong fix.** Design is already API-first ID; TEE encrypts with that AAD.

**If HTTP lookups disagree on the same numeric id**, the usual cause is **multiple API replicas + in-memory storage** (no **DATABASE_URL**), not TEE vs Postgres.

## Architecture (authoritative)

| Layer | Owns `agent_id`? | Persists Share B? |
|-------|------------------|-------------------|
| **API** (`api/`) | **Yes** | **Yes** (encrypted) |
| **TEE** (`tee-app/`) | **No** | **No** |
| **Client** | — | Holds `key_share` |

Flow: API `allocUsername` → TEE `create-wallet` `{ agent_id }` → API `finalizeWallet`. Sign: API loads Share B by id, forwards both shares + `agent_id` to TEE.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Same `agent_id`, different users across requests | Multi-replica API, in-memory DB | Set **DATABASE_URL** (Postgres); restart API |
| `/ready` → `"database":"memory"` on GKE | Missing `DATABASE_URL` | `deploy/gcp/kubectl-create-all-secrets.sh db-only` etc. |
| 502 on create | TEE / HMAC | `TEE_BASE_URL`, matching `INTERNAL_HMAC_SECRET` |

See `api/src/storage/createAgentWalletStorage.ts` for the K8s warning when `DATABASE_URL` is unset.

## HTTP routes

| Method | Path | Notes |
|--------|------|--------|
| GET | `/health`, `/ready` | Liveness / readiness |
| POST | `/create-agent-wallet` | `{ "username" }` → `agent_id`, `key_share`, … |
| POST | `/sign-transaction` | `{ agent_id, key_share, tx_data }` |
| GET | `/agent/:agent_id`, `/user/:username` | Public metadata |

**`tx_data`:** `api/src/validation/txSchema.ts` — **`chainId`** required; build JSON with **`jq`** / **`python3`** (base64 `key_share` breaks in raw shell).

**Errors:** 409 username taken; 404 not found; 429 + `scope`; 502 TEE failure.

## Environment

- **API:** `api/.env.example` — **`DATABASE_URL`** required for **>1 replica**.
- **TEE:** `tee-app/.env.example` — never **`TEE_MASTER_KEY`** on the API.

## Code map

`api/src/index.ts`, `api/src/teeClient.ts`, `api/src/storage/*`, `tee-app/src/walletCore.ts`, `deploy/gcp/README.md`.

---

## ClawHub publish

[Skill format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md). Published skills are **MIT-0**; no secrets in this file.

```bash
clawhub login
cd /path/to/agent-wallet
clawhub publish skills
```

Install/sync in OpenClaw so agents load this pack.
