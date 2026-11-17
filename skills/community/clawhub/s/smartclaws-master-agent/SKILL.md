---
name: smartclaws-master-agent
description: >
  Run one SmartClaws master control cycle: read device telemetry on-chain, decide
  under the owner's guidelines, command a device only when allowed, and log the
  decision on-chain. Trigger when asked to run a control cycle, check devices and
  decide, command a device, or audit recent decisions. Needs the SmartClaws plugin
  and a device contract skill per device.
license: LGPL-3.0-or-later
metadata:
  openclaw:
    emoji: "🧠"
    homepage: https://github.com/skalenetwork/smartclaws
    requires:
      config: ["plugins.entries.smartclaws"]
---

# SmartClaws Master — Control Cycle

This skill is a **procedure**: it runs **one control cycle** when asked — read
telemetry → decide → command if allowed → log on-chain → exit. Your identity,
behaviour, and command-authority are not defined here; they live in your
owner-owned `AGENTS.md` (loaded every session), which wins on any conflict.

This procedure is **device-independent** and **policy-free**. Device facts come
from device contract skills; deployment wiring and the owner's **goal** from
`SMARTCLAWS.md`; behaviour, authority, and extra control knobs from `AGENTS.md`.

## Required Context

Before running the cycle, identify:

- **`AGENTS.md`** — your behaviour, authority/permissions, and extra guidelines.
- **`SMARTCLAWS.md`** at the workspace root — devices, channels, which devices are
  `commandable`, and the owner's **`goal`** (what you are trying to achieve).
- **Device contract skills** for every device you read or command.
- **Optional source skills** for non-chain context, when that skill is
  installed and documents its own `SMARTCLAWS.md` wiring (for example
  `smartclaws-tariff-file-source`).
- **The SmartClaws plugin** — `smartclaws_read` / `smartclaws_disclose` /
  `smartclaws_publish` / `smartclaws_notify` / `smartclaws_wallet_info`.

If `SMARTCLAWS.md` is missing, lacks a device/channel you need, has no `goal`
and you would otherwise act unsupervised, or you cannot yet say you have all
as this job, **stop and run the `smartclaws` onboarding skill** (or ask the
owner). Never invent addresses, device names, authority, or a mission.

When calling SmartClaws plugin tools, use the device entry's `name` field or the
explicit channel address from `SMARTCLAWS.md`. Device map keys are labels; they
are not necessarily registered SmartClaws device names.

For SmartClaws plugin `agent` targets, use the agent entry's `id` field or
`address` from `SMARTCLAWS.md`. The `name` field is display text and may not
resolve as a local registered agent.

## Scope of this procedure

While running a cycle you:

- Read outgoing telemetry channels for many devices, and your own decision log.
- Decide whether a command is warranted from telemetry + the owner's `goal`
  (and extra `AGENTS.md` guidelines).
- Publish a command to a device's **incoming** channel only when it is marked
  `commandable` in `SMARTCLAWS.md`, the payload matches the device contract, and —
  **for whether the current caller/session is allowed to make you act — your
  `AGENTS.md` authorizes it.** This skill does not define that allowlist; defer to
  `AGENTS.md` and refuse if it doesn't grant the action.
- Optionally **notify another agent** by publishing to its incoming channel with
  `smartclaws_notify` (requires SENDER_ROLE on that agent, granted by its owner) —
  the basis for delegating to or coordinating with a sub-agent. Same authority
  rule: only when `AGENTS.md` authorizes it and the target is named in
  `SMARTCLAWS.md`. Never notify an agent you weren't told about.
- Log every outcome to your own agent outgoing channel.

This procedure never touches local hardware directly (that's a bridge's job),
never publishes to an absent/null/telemetry-only incoming channel, and never
reads or prints wallet/key material.

## Encrypted channels

Some devices and agents store **sealed** messages. Kind is chosen at
registration and does not change. Topics and payloads stay the same.

**This skill may load without the `smartclaws` skill.** Follow this section
on its own.

### Read vs disclose

| Channel | Tool | What you get |
| --- | --- | --- |
| Plain | `smartclaws_read` | Decoded envelopes |
| Encrypted | `smartclaws_disclose` | Decoded envelopes |

`smartclaws_read` on an encrypted channel still works, but it returns
**ciphertext** (that is success, not an error). To see the real payload, use
`smartclaws_disclose`. If you may disclose, do it — same as reading.

How to tell: `SMARTCLAWS.md` `encrypted:`, or the plugin
(`smartclaws_list_local`, `smartclaws_access_check`, or `encrypted: true` on a
read result).

`smartclaws_disclose` takes the same `device` / `agent` / `channel` / `side`
as read, plus:

- `fromOffset` — first stored offset (inclusive). Required.
- `count` — how many messages, **1–10** (default 1). The tool will not split a
  larger range. Call again for the next batch if you need more.

If you do not know the latest offset, `smartclaws_read` still reports `latest`
and `total`. Then disclose that range.

You must be on that channel's **reader list** and have a registered viewing
key. `smartclaws_wallet_info` says whether the registered key can open
messages. `smartclaws_access_check` says whether this wallet can read each
channel.

### Writing (publish / notify)

Same tools on plain and encrypted: `smartclaws_publish` and `smartclaws_notify`.
They detect the kind. Leave `wait` at its default (`true`). You will see
`callbackDeposit` in the result — that is what the plugin paid automatically,
not something you set (there is no parameter for it).

Treat the message as stored only when `status` is `published`.

| `status` | Meaning | What to do |
| --- | --- | --- |
| `published` | Message is stored | Done. Keep the tx hash. |
| `scheduled` | Accepted, not stored yet | Do **not** send it again. Re-check later. |
| `origin-reverted` | Nothing was stored | Safe to send again. |
| `ctx-reverted` | Failed after scheduling | Do **not** send it again. Report the failure. |

`wait: false` returns as soon as the first tx is sent (`scheduled` until
confirmed). Only use it if the owner asked. Default `wait: true`.

### Errors

| What happened | What to do |
| --- | --- |
| Wallet has no funds | Ask the owner to fund it. Same as any other write. |
| `NOT_A_READER` | This wallet is not on the reader list. Ask the owner / group master. |
| `NO_VIEW_KEY` or `NO_PUBLIC_KEY` | Viewing key missing or not registered. Setup is incomplete — run the `smartclaws` skill or ask the owner. |
| Disclose wait timed out | The chain may still finish. Do not disclose the same offsets again as a new write. Wait / re-check. |
| Disclose on a plain channel | Use `smartclaws_read` instead. |

Never invent plaintext from ciphertext. Report only what the plugin returned.

## The Cycle — run exactly one

1. Load `AGENTS.md` guidelines and `SMARTCLAWS.md` wiring **and `goal`**.
2. Select the device contract skills needed for the request.
3. Read telemetry from each relevant outgoing channel. Plain: `smartclaws_read`.
   Encrypted: `smartclaws_disclose` (see above). Prefer the explicit
   `outgoingChannel`; if using `device`, pass the device entry's `name`, not
   the YAML map key.
4. Read optional local sources, such as tariff snapshots, only when configured
   in `SMARTCLAWS.md`; validate them against their source skill and freshness
   window.
5. Validate freshness and payload shape using each device contract.
6. Decide: act, hold, ask, or fail loud. Honor `SMARTCLAWS.md` `goal`. Extra
   knobs in `AGENTS.md` constrain you; they must not contradict `goal` — if they
   do, stop and ask. Blank knobs → skill defaults. **Blank or missing `goal` →
   no standing mission: do not invent one; ask, or hold, rather than running an
   unsupervised strategy the owner never chose.**
7. If acting, confirm the action is authorized by `AGENTS.md`, then publish
   **exactly one** command with `smartclaws_publish` using the device entry's
   `name` plus `deviceChannel: "command"`; do not write directly to the raw
   incoming channel unless the setup explicitly tells you to. Treat it as sent
   only when `status` is `published` (see above). Capture the transaction hash.
8. Publish a `decision.log` event to your agent outgoing channel (always — below).
9. Report what happened, including transaction hashes when a publish succeeded
   (`status: published`).

Do not loop inside one invocation. Cadence/scheduling is an owner/operations
choice, set in `AGENTS.md` or your own setup — not here.

## Decision Log (on-chain audit trail)

Record **every** cycle outcome to your own outgoing channel — actions, holds,
degraded/stale runs, failures. On-chain logs are cheap and filterable; don't
self-censor. Publish with `smartclaws_publish` using your **`agent`** target
(pass `agent.id` or `agent.address`, not display `agent.name`; this writes
through the agent contract's `publishOutbound`, which your owner role holds — a
raw channel write to the agent's own channel is rejected), topic `decision.log`
(unless `SMARTCLAWS.md` overrides it).

Payload — a human-readable `reason` plus structured fields:

```json
{
  "decision": "preheat",
  "source": "cron",
  "reason": "Plain-language explanation with the key numbers you computed.",
  "acted": true,
  "devices": ["shelly-plug"],
  "ts": "<current ISO 8601 UTC>"
}
```

- `decision`: free-form label (`relay-on`, `hold`, `coast`, `failed`,
  `cycle-ok`, …). No fixed enum.
- `source`: what triggered it (`cron`, `user`, `system`).
- `reason`: your reasoning in plain language — the most important field.
- `acted`: `true` only if you published a device command this cycle.
- Add device-specific numeric fields when you have them; use `null`, never a guess.

Only `decision`, `source`, and `reason` are strictly required. Never claim a
command or log succeeded unless the plugin returned `status: published`.

## Failure Rules

- Missing/incomplete setup: run the `smartclaws` skill or ask for `SMARTCLAWS.md`
  (including a confirmed `goal` if you would act unsupervised).
- Unknown channel: stop; do not guess.
- Stale or malformed telemetry: avoid command actions unless the owner's
  guidelines explicitly allow it.
- Plugin publish failure, `origin-reverted`, or `ctx-reverted`: fail loud; do
  not report the physical state changed.
- Encrypted publish `scheduled`: the command is not stored yet. Do not retry
  as a new publish; do not claim it landed.
- Wallet unfunded: ask the owner to fund it (disclose and publish both need
  funds).
- Device contract conflict: prefer the stricter safety rule and ask for clarity.
