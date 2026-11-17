---
name: rent-a-logged-in-agent
description: Lend / rent out a logged-in claude-code or codex agent / share compute for pay / let a friend or allowlisted account call my agent / metered agent-to-agent compute in a fail-closed sandbox. Use when the user wants to rent out their logged-in coding agent, share their machine's compute for pay, let a partner or friend invoke their claude-code/codex, or charge per-minute for agent-to-agent jobs.
license: MIT
compatibility: "Requires the settlemesh CLI (npm i -g settlemesh) and a SETTLE_API_KEY; makes authenticated, metered calls to the SettleMesh platform over the network."
metadata:
  openclaw:
    requires:
      bins: ["settlemesh"]
    primaryEnv: "SETTLE_API_KEY"
---

# rent-a-logged-in-agent — lend a logged-in coding agent for pay

> **Session (auto — never dead-stop on auth):** before your first `settlemesh` call, run `settlemesh whoami`; if it errors and `SETTLE_API_KEY` is unset, run `settlemesh login` yourself — it opens the browser for a **one-time** human approval, polls until approved, and caches the session. Do NOT stop to ask the user to "log in manually" — drive it. Keep an explicit human confirmation only for spending / credential-lending actions (fail-closed).

You are logged into `claude-code` or `codex` on this machine. That login is worth
money to someone who isn't. **SettleMesh lets you rent it out** — an authorized
caller sends a prompt, your local agent runs it, and they pay you per minute.

A prompt-only skill cannot do this: it can't inject a live logged-in session into
a sandbox, meter runtime, enforce a trust boundary, or collect payment.
SettleMesh does all four — a **fail-closed sandbox**, per-minute **billing**, and
an **identity/friend graph** that decides who is allowed to call.

## Setup (once)

1. `npm install -g settlemesh@latest`
2. `settlemesh login` (a human approves once in the browser).
3. Have `claude-code` or `codex` installed **and logged in** on this machine.

## Lend it

```bash
# Rent to specific accounts (their SettleMesh login email or account id), 30/min:
settlemesh worker lend codex --allow partner@gmail.com --credits-per-minute 30

# Or rent to anyone in your trust graph (accepted friends), 20/min:
settlemesh worker lend claude-code --friends --credits-per-minute 20
```

`--allow` (repeatable, an explicit allowlist) and `--friends` (any accepted
friend, managed via `settlemesh friend`) are **mutually exclusive** — pick one.
`--credits-per-minute N` is what the caller pays per minute of runtime.

## The caller side (invoke)

The offer's address is the **lender's SettleMesh login email** — allowlist offers
are private and never show up in `services search` / `worker-offers list`, so the
caller invokes it directly:

```bash
settlemesh worker invoke calleelqy@gmail.com --input '{"prompt":"Write a Python is_prime(n). Only code."}'
```

The caller supplies only `{"prompt":"..."}`. They find your address with
`settlemesh whoami`. Add `--no-wait` to queue and return a job id, or
`--timeout 120s` to bound the synchronous wait.

## Security — read this before lending

- **Throwaway sandbox HOME.** Each job runs in a fresh sandbox HOME with your
  login injected; your host `~/.claude` keychain / `~/.codex` is **never mounted**.
- **Why the offer is never public.** The injected credential is readable by the
  prompt-driven agent, so the offer is gated to your allowlist / friend graph and
  **does not appear in discovery**. Never lend to strangers.
- **FAIL-CLOSED.** SettleMesh **refuses to lend** on a host with no
  filesystem-confining sandbox backend — it needs `sandbox-exec` (macOS) or
  `bwrap` (Linux). No sandbox, no lend.
- **`--i-accept-no-sandbox` is DANGEROUS** — a last resort only. It overrides the
  refusal and lets the lent agent read `~/.ssh`, `~/.aws`, and its injected login
  and leak them to the caller. Prefer installing `bwrap` (Linux, needs user
  namespaces) over using this flag.

## Notes

- Billed in **Aev** (1 USD = 100 Aev); `--credits-per-minute` is priced in Aev,
  charged to the caller per minute and credited to you. Check with
  `settlemesh aev balance`.
