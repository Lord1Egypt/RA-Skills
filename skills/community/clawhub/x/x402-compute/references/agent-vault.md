# Agent Vault — encrypted agent backup & migration

Zero-knowledge encrypted backup, restore, and migration for AI agents
(OpenClaw `~/.openclaw`, Hermes `~/.hermes`). Snapshot an agent's entire
self — memory, soul/workspace, config, skills — and bring it back anywhere:
a new machine, a fresh Agent Pod, or the same box after a bad day.

**Zero-knowledge, for real:** every backup is sealed on the machine it lives
on (scrypt key derivation + AES-256-GCM, AAD-bound to the snapshot identity).
The platform stores ciphertext it cannot read. That cuts both ways — **a lost
passphrase is unrecoverable by anyone, including Singularity Layer.** Tell the
user to write it down before the first backup.

Dashboard: https://cloud.x402compute.cc/network/backups
Plans (all paid from platform credits):
  FREE      — 1 GB, 1 rolling snapshot (each new backup replaces the previous).
  VAULT PRO — 10 GB, the last 10 snapshots OF EACH AGENT. $3/month or $30/year.
  VAULT MAX — 50 GB, unlimited snapshots, full history. $5/month or $50/year.
Yearly is two months free. The FREE tier needs no call and no payment — every
wallet starts there. Subscribe with
`POST /backups/subscribe {"plan":"pro"|"max","interval":"month"|"year"}`
(credits), or add `"pay":"x402","network":"base"|"solana"|"robinhood"|"megaeth"`
to pay directly: the route answers 402 with an x402 challenge when a charge is
required and credits are short, then activates on the retry carrying
`X-Payment`. The challenge quotes the FULL plan price; proration means the real
debit can be lower and the remainder stays as credits. Cancels and scheduled
downgrades never produce a challenge. The payer must be the authenticated
wallet, and a replayed `X-Payment` cannot double-charge. The dashboard route is
Agent Vault → Upgrade.

Upgrades charge now, PRORATED against the unused part of the period already
paid for, and start a fresh period; downgrades and `"plan":"free"` (cancel)
take effect at the end of the period already paid for, and never charge. An
x402 challenge is therefore only ever issued for an action that actually costs
money. A failed renewal downgrades behavior only; stored
backups are never deleted. Per-snapshot cap: 2 GiB.

Agent Vault works for any Singularity Layer login: a wallet, or an account login without a wallet.
Every account also gets its own non-custodial wallet on Base and
Solana, secured by Coinbase, so an account login needs no wallet of its own to use Vault.

## CLI (the normal path)

```bash
npm i -g @singularity-layer/agentvault

agentvault login              # browser wallet approval (device flow)
agentvault login --api-key    # headless: paste a compute API key instead
agentvault backup --all       # detect, encrypt, upload every local agent
agentvault backup --path <dir> --name <n>   # UNIVERSAL: vault any directory (any harness)
agentvault list               # agents + snapshot counts
agentvault restore            # pick snapshot -> passphrase -> safe unpack
agentvault restore --dest ~/x # restore into a specific directory
agentvault passphrase set     # store passphrase in the OS keychain
agentvault daemon install --frequency weekly   # automatic backups
```

Non-interactive (cron/agents): store the passphrase once with
`agentvault passphrase set`, then `agentvault backup --non-interactive`.

## Migration recipes

- **Machine → machine:** `backup --all` on the old box; `login` + `restore`
  on the new one. Same wallet, snapshots appear automatically.
- **Machine → pod / pod → pod:** back up anywhere, then open the destination
  pod's **Backups** tab in the dashboard and restore the snapshot onto it
  (the pod restarts itself with the restored state).
- **Pod → machine:** the pod's snapshots appear in `agentvault list` on any
  machine logged into the same wallet — `agentvault restore`.

## Pods (one click, no install)

Pod detail page → **Backups** tab → passphrase → **Back up now**. The pod
encrypts on-box and uploads directly; restore (including from another pod or
a local machine snapshot of the same wallet) is the same tab.

## HTTP API (for agents that cannot run the CLI)

All routes on `https://compute.x402layer.cc`, auth `X-API-Key` (compute API
key). The flow mirrors the CLI: reserve → presigned PUT → verified complete.

| Method | Route | Purpose |
|---|---|---|
| GET | `/backups/agents` | list registered agents |
| POST | `/backups/agents` | `{name, framework}` find-or-create |
| POST | `/backups` | `{agentId, sizeBytes}` → `{backupId, r2Key, uploadUrl}` |
| PUT | *presigned `uploadUrl`* | upload the encrypted blob |
| POST | `/backups/{id}/complete` | `{sha256}` of the uploaded blob |
| GET | `/backups?agentId=` | list complete snapshots |
| GET | `/backups/{id}/restore` | → `{downloadUrl, r2Key}` |
| DELETE | `/backups/{id}` | delete a snapshot |
| GET | `/backups/usage` | bytes used/reserved + caps |

Encryption is CLIENT-side: encrypt before PUT (scrypt N=2^17 r=8 p=1,
AES-256-GCM envelope; AAD = `{userId, agentId, backupId, formatVersion:1}`
parsed from `r2Key` = `backups/{wallet}/{agentId}/{backupId}/blob.enc`).
Prefer the CLI unless you must integrate directly.

## Safety rules for agents using this skill

- NEVER echo, log, or store the user's passphrase; prompt at point of use.
- Restore REPLACES agent state (previous state is parked `.pre-restore` on
  pods). Confirm with the user before restoring over a live agent.
- If a restore errors "argon2id key derivation; restore with the agentvault
  CLI", the snapshot predates the scrypt default — run it through the CLI.
