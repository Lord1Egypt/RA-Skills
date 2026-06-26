# Session Overview: April 5-7, 2026 (ldmos03)

## What we did (in order)

### Phase 1: Bug fixes ($936 guard loop crisis)
- **Guard stash escape hatch** (wip-branch-guard 1.9.72): `git stash push` allowed on main so agents can clear untracked files blocking `git pull`
- **Guard SessionStart hook** (1.9.73): warns at session boot when CWD is main-branch with worktree list
- **Guard temp-dir writes** (1.9.74): `/tmp/`, `/var/tmp/`, macOS temp dirs allowed
- **Release pipeline hardening** (wip-release 1.9.72-1.9.74): refuse non-main, tag collision pre-flight, sub-tool drift error, auto-PR for protected main, auto-deploy-public
- **deploy-public.sh** (1.9.69-1.9.70): error classifier, no-early-exit fix
- **Installer** (wip-ldm-os alpha.18-19): multi-hook support, ghost folder fix
- **All bugs archived or fixed**

### Phase 2: Bridge (CC-to-CC communication)
- **Async send** for `lesa_send_message` (fire-and-forget + file inbox reply)
- **CC-to-CC messaging** tested and working (ldmos03 <-> test-bridge round-trip confirmed)
- **Dynamic session names** from CC `/rename` labels (reads `~/.claude/sessions/<pid>.json`)
- **Inbox check hook** reads CC session name dynamically (no restart needed after `/rename`)
- **Bridge reverted** from channel-bound dispatch (broke reply path, fully reverted to sync)

### Phase 3: Product architecture
- **Bridge master product plan** (5 layers, Phases A-E: pairing, push, approval, relay, UI)
- **Kaleidoscope architecture** (repo layout, kernel/app split, subdomain decision)
- **Device pairing** (`ldm pair` CLI + `/api/pair/*` server endpoints built, deployed to VPS)
- **Shared universal config layer** bug filed (rules scattered, needs single source)

### Phase 4: Infrastructure
- **Postgres 16** installed on VPS, database `kaleidoscope` created
- **Prisma schema** with 5 tables (User, Credential, Device, Wallet, ApiKey) migrated
- **Server deployed** with pairing endpoints live on wip.computer
- **Nginx updated** with `/api/pair/` proxy rule
- **Passkeys wiped** clean for production start

## What is DONE

| Item | Status | Where |
|---|---|---|
| Guard 1.9.74 (stash + SessionStart + temp) | SHIPPED, deployed | npm + ~/.ldm/extensions/ |
| wip-release 1.9.74 (auto everything) | SHIPPED | npm |
| LDM OS alpha.24 (multi-hook, ghost fix, bridge) | SHIPPED, installed | npm + /opt/homebrew/ |
| CC-to-CC file inbox messaging | WORKING | ~/.ldm/messages/ |
| Dynamic session names (/rename support) | WORKING | bridge + inbox hook |
| Postgres on VPS | RUNNING | VPS postgresql, db: kaleidoscope |
| Prisma schema + migration | APPLIED | 5 tables on VPS |
| `ldm pair` CLI command | BUILT | bin/ldm.js |
| Server pairing endpoints | DEPLOYED | wip.computer/api/pair/* |
| Nginx pairing proxy | CONFIGURED | VPS /etc/nginx/snippets/mcp-oauth.conf |
| Passkeys DB (production) | WIPED CLEAN, ready for real customers | VPS passkeys.json (still JSON, Prisma migration pending) |

## What NEEDS to be done (next session)

### Step 4: Migrate server.mjs from JSON to Prisma (BIGGEST ITEM)
- 26 JSON file references across 1800 lines
- Replace `loadPasskeys()` / `savePasskeys()` with `prisma.credential.findMany()` / `.create()`
- Replace `loadPairedDevices()` / `savePairedDevices()` with `prisma.device` queries
- Replace `API_KEYS` object with `prisma.apiKey` queries
- Replace wallet JSON with `prisma.wallet` queries
- **CRITICAL: demo must keep working.** Same API endpoints, same response format. Only the storage layer changes.

### Step 6-7: Copy nginx + PM2 configs into repo
- `src/hosted-mcp/nginx/wip.computer.conf`
- `src/hosted-mcp/nginx/mcp-oauth.conf`
- `src/hosted-mcp/nginx/mcp-server.conf`
- `src/hosted-mcp/ecosystem.config.cjs`
- These exist ONLY on the VPS right now. If server dies, configs are lost.

### Step 8: Build wip.computer/login
- Real login page (not /demo/)
- Same passkey flow as demo but at production URL
- Same design language (sprites, colors, LUME)
- This is the entry point for real customers

### Step 9: Test ldm pair end-to-end
- Register fresh passkey at wip.computer/login
- Run `ldm pair` on Mac Mini
- Go to wip.computer/pair on phone
- Enter code, approve with Face ID
- Verify token stored at ~/.ldm/auth/kaleidoscope.json

### Bridge Phase B: Push notifications (after pairing works)
- WebSocket from bridge to Kaleidoscope
- Kaleidoscope pings bridge when inbox has new messages
- Agents wake up without Parker typing

### Bridge Phase C: Approval flow
- CC requests cross-agent permission
- Parker gets Face ID prompt on phone
- Time-boxed approval (5/10/15 min)

## Key files

### Plans and architecture
- `ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md` ... Bridge product plan (pairing, push, approval, relay)
- `ai/product/plans-prds/kaleidoscope/2026-04-06--cc-mini--kaleidoscope-architecture.md` ... repo layout, kernel/app split
- `ai/product/plans-prds/kaleidoscope/2026-04-06--cc-mini--postgres-prisma-infrastructure.md` ... Postgres + Prisma 9-step plan
- `ai/product/bugs/bridge/2026-04-06--cc-mini--bridge-async-inbox-plan.md` ... async inbox design
- `ai/product/bugs/release-pipeline/2026-04-06--cc-mini--shared-universal-config-layer.md` ... shared rules bug

### Code that was changed
- `bin/ldm.js` ... added `ldm pair` command
- `src/hosted-mcp/server.mjs` ... added `/api/pair/*` endpoints + pairing state machine
- `src/hosted-mcp/prisma/schema.prisma` ... Prisma schema (5 tables)
- `src/bridge/mcp-server.ts` ... async send, dynamic session names, session registration
- `src/bridge/core.ts` ... refreshSessionIdentity(), drainInbox refresh
- `src/hooks/inbox-check-hook.mjs` ... CC session name from ~/.claude/sessions/
- `tools/wip-branch-guard/guard.mjs` ... stash allow, SessionStart, temp-dir writes
- `tools/wip-release/core.mjs` ... refuse non-main, tag collision, auto-PR, auto-deploy-public, sub-tool drift error
- `tools/deploy-public/deploy-public.sh` ... error classifier, no-early-exit
- `lib/deploy.mjs` ... multi-hook installer support
- `lib/detect.mjs` ... plural claudeCode.hooks array support

### VPS state
- Postgres 16 running, db: `kaleidoscope`, user: `kaleidoscope`
- Password in 1Password: "Postgres VPS (kaleidoscope)" in Agent Secrets
- SSH tunnel for Prisma: `ssh -L 15432:localhost:5432 wip-vps`
- server.mjs deployed with pairing endpoints
- nginx updated with `/api/pair/` proxy
- Passkeys wiped clean (0 registrations, production from here)
- `paired-devices.json` empty (production from here)

### Bridge architecture
- `wip.computer` = the company (like openai.com)
- `kaleidoscope.wip.computer` = the product (like chatgpt.com)
- Web frontend: `repos/wip-web/wip-web-private/` (Next.js, existing deploy)
- Native apps: `repos/ldm-os/apps/kaleidoscope-private/` (iOS, macOS, future)
- Kernel + API: `repos/ldm-os/wip-ldm-os-private/` (CLI, server, bridge)
- Plans + bugs: centrally in `wip-ldm-os-private/ai/product/`

## Gotchas and things to be careful with

### 1. Demo must not break
The demo at `wip.computer/demo/` calls the same WebAuthn endpoints as the real app. When migrating server.mjs from JSON to Prisma, the API responses must be byte-identical. Test the demo after every server deploy.

### 2. OpenClaw fork bridge revert
The channel-bound dispatch code was fully reverted (commit `7386663d2b`). The sync path is restored. `lesa_send_message` was changed to async (fire-and-forget) in the bridge MCP server but the OpenClaw gateway still runs the sync path. These are two different code paths: the MCP tool (async, in wip-ldm-os-private) vs the gateway handler (sync, in the OpenClaw fork). Don't confuse them.

### 3. lesa_send_message is currently async
Changed in PR #469 (alpha.20). It fires-and-forgets to the gateway and returns immediately. Lēsa's reply comes via the file inbox. This means CC doesn't get the reply in the same tool call anymore. The long-term fix is Kaleidoscope push (Phase B). For now, replies arrive via the UserPromptSubmit inbox hook.

### 4. Session name race condition
The bridge reads `/rename` labels from `~/.claude/sessions/<ppid>.json`. There's a retry (3x, 500ms) for the boot race. But the MCP server reads once on boot; the `refreshSessionIdentity()` on every `drainInbox()` call handles subsequent renames. The inbox-check-hook reads fresh every time (it's a new process per interaction). Alpha.24 has both fixes.

### 5. Prisma .env not in repo
`src/hosted-mcp/.env` contains `DATABASE_URL` with the Postgres password. It's gitignored. On the VPS, the DATABASE_URL needs to be set in PM2's ecosystem.config.cjs or as an environment variable. The password is in 1Password.

### 6. Passkeys are production from here
We wiped the database. Every new registration is a real customer. No more wipes. The `passkeys.json` file on VPS is the production credential store until Step 4 (Prisma migration) moves it to Postgres.

### 7. nginx configs are VPS-only
`/etc/nginx/snippets/mcp-oauth.conf` and related configs are NOT in the repo yet. Steps 6-7 fix this. If the VPS dies before that, the configs need to be recreated from the session recap or from `ssh wip-vps 'cat /etc/nginx/...'`.

### 8. Lēsa's cost crisis
$86 of $200 credits gone. 8 failing crons. Cost audit at `~/.openclaw/workspace/cost-audit-apr-6.md`. The bridge fix (reverted channel-bound dispatch) eliminated the 2-5x cost amplification. The failing crons are still burning money. Parker said keep brainstorm running.

## PRs merged this session

~35 PRs across wip-ldm-os-private (#447-484), wip-ai-devops-toolbox-private (#317-331), wip-ai-devops-toolbox public (#245-251), wip-web-platform-private (#1), kaleidoscope-private (#16), plus OpenClaw fork commits.

## npm packages shipped

- wip-branch-guard: 1.9.72 -> 1.9.74
- wip-release: 1.9.72 -> 1.9.74
- deploy-public: 1.9.69 -> 1.9.70
- wip-ai-devops-toolbox@alpha: alpha.7 -> alpha.12
- wip-ldm-os@alpha: alpha.18 -> alpha.24
