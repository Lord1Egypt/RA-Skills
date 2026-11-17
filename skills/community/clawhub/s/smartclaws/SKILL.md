---
name: smartclaws
description: >
  Entry point for SmartClaws on OpenClaw: teaches what SmartClaws is (publish/read
  IoT telemetry on the SKALE blockchain), jobs and plugin modes, and how its
  plugin tools work. When the owner wants to start, set up, onboard, or when
  this agent cannot yet say it has everything as its job, read SETUP.md and
  iterate until it can. For how messages, roles, and encryption work in depth,
  read MECHANICS.md.
license: LGPL-3.0-or-later
metadata:
  openclaw:
    emoji: "🦾"
    homepage: https://github.com/skalenetwork/smartclaws
---

# SmartClaws

This skill teaches you what SmartClaws is. Unlike the other SmartClaws skills,
it does **not** require the plugin to already be installed. Day to day it is
used **alongside** the plugin tools.

**If you are setting up, onboarding, nothing is configured yet, or you cannot
yet say “I have all as a group-master agent” (or the confirmed job), read
`SETUP.md` and follow it.** Do not load `SETUP.md` just to explain SmartClaws.

**If you need how messages move, who controls which on-chain role, or viewing
keys in depth, read `MECHANICS.md`.** Do not load it to answer “what is a
device.”

Setup is finished when you can truthfully say that sentence for the confirmed
job (group-master, device-master, device-bridge, or user-proxy). Until then,
keep iterating with the owner. You uninstall nothing when you get there; you
hand off to the role and device skills. This skill stays for re-setup.

## What SmartClaws Is

SmartClaws publishes and reads IoT sensor/command data **on-chain** on SKALE.
The chain is the message bus and the source of truth. The pieces:

- **Registry** — one contract that tracks device groups, agents, and channels.
- **Device group** — a named collection of devices. The **wallet that
  registered it owns it** (add devices, grant who may command). Usually one
  group master.
- **Device** — one physical thing (a sensor, a plug). Two channels: *outgoing*
  (telemetry, role `publisher`) and *incoming* (commands, role `master`).
  On-chain `master` means “may send commands to this device,” not “owns the
  group.”
- **Agent** — on-chain identity for an AI. *Outgoing* is a decision log
  (`publisher`); *incoming* is an inbox others may notify (`sender`).
- **Channel** — append-only log of envelopes `{ v, ts, dev, topic, p }`.
  `p` is JSON; topics/payloads come from device skills.
- **Plain or encrypted** — chosen **once at registration**, for both channels,
  **for life**. Changing kind means a **new** device or agent on-chain. Plain
  stores readable JSON. Encrypted stores sealed ciphertext; only wallets on
  that channel’s **reader list** can open it. Encryption does not change
  topics or payloads.

A **bridge** publishes hardware readings to outgoing and, if configured,
applies commands from incoming. A **master** reads those readings, may
command, and (if it has an agent) logs decisions. Agents coordinate by
notifying each other’s inboxes. Details: `MECHANICS.md`.

You never invent addresses. Resolve them with the plugin (`list_local`,
`discover`) using registered **names**. `SMARTCLAWS.md` holds what the chain
does not know (which device skill, labels, local policy, the owner's **goal**).

## Jobs and plugin modes

Four jobs. Plugin `mode` is the HOME shape, not the English word.

| Job | What you do | Plugin mode | Agent contract | Group |
| --- | --- | --- | --- | --- |
| **User proxy** | Act for a human, only when asked. Can only do what that wallet is already allowed to do. Not for unsupervised agents. | `controller` | none | Do not create one. Attach only what that wallet already belongs to. |
| **Device bridge** | Sit next to one physical device: publish readings, apply commands a master sent. | `bridge-agent` | yes | Do not create one. One device only. |
| **Master of a group** | Own the group: add devices, grant who may command, and may command devices. Usually one per group. | `master-agent` | yes | Attach existing, or this wallet registers a new one (and owns it). |
| **Master of some devices** | Command some devices in a group you do **not** own. Do not add devices or change group config. | `master-agent` | yes | Must already exist (or the owner deploys it with a **separate** wallet). This wallet must not register it. |

A group is owned by the wallet that registered it. Several device-masters can
hold `master` on devices in the same group. Registering a group with this
wallet makes it the owner — never do that for “master of some devices.”

## Roles, readers, viewing keys

Three different permission systems — do not mix them:

| Kind | Where | What it allows |
| --- | --- | --- |
| Group **owner** | Group contract | Add devices, grant/revoke. One wallet. |
| AccessControl **roles** | Device: `publisher`, `master`. Agent: `publisher`, `sender`, `agent-admin` | Who may **write** a channel |
| Encrypted **reader ACL** | Encrypted channel only | Who may **disclose** (decrypt). Not a role |

**Viewing key** — used only to open disclosures. Required, and separate from
the signing key: generate and register it after funding, before the first
disclose. A mismatched registered key looks like corrupt data, not “wrong
key.” `smartclaws_wallet_info` reports whether the registered key can open
disclosures.

## Reading, publishing, encryption

- **Plain** — `smartclaws_read` returns decoded envelopes.
- **Encrypted** — use `smartclaws_disclose` to get the same decoded envelopes.
  `smartclaws_read` still works, but returns labelled **ciphertext** (success,
  not an error). If you may disclose, do it — same as reading. Disclose takes
  `fromOffset` plus `count` 1–10.
- Encrypted publish/notify uses the **same tools**. Leave `wait` at default.
  `callbackDeposit` in the result is what the plugin paid automatically —
  there is no parameter for it, nothing to set. Treat as stored only
  when `status` is `published` (`scheduled` is not stored; do not send again).

## Calling the plugin

Join key is the **registered `name`** (or a `0x` address). YAML map keys and
display names are not lookup keys unless they match.

- Device: pass `device` = registered name (see `SMARTCLAWS.md` `name:`).
- Agent: pass `agent` = `id` or contract `address`, not display `name`.
- `channel` is always an address.

If `SMARTCLAWS.md` has a copied address that disagrees with
`smartclaws_list_local` / `discover`, trust the plugin.

## The Plugin Tools (your runtime)

Once the SmartClaws plugin is installed and configured:

| Tool | What it does |
| --- | --- |
| `smartclaws_setup_status` | HOME/setup state, issues, and recommended next tools. Start here. Follow it until HOME is `ready`. Necessary, not sufficient, for “I have all as …” |
| `smartclaws_wallet_info` | Address, balance, network, and whether the registered key can open disclosures. Never the private key. |
| `smartclaws_list_local` | Cached groups, devices, and agents. |
| `smartclaws_discover` | Paginated on-chain discovery. |
| `smartclaws_access_check` | Whether this wallet can read each named channel. |
| `smartclaws_read` | View read. Plain → decoded envelopes; encrypted → ciphertext. |
| `smartclaws_disclose` | Open encrypted messages (1–10 offsets). The encrypted equivalent of read. |
| `smartclaws_publish` | Publish an envelope through a device, your agent, or a channel. Encrypted: treat as stored only when `status` is `published`. |
| `smartclaws_notify` | Send a message to another agent's incoming channel (needs `SENDER_ROLE`). |
| `smartclaws_initialize` | Create or configure a HOME; generate a wallet if missing. |
| `smartclaws_configure` | Patch HOME config. |
| `smartclaws_attach` | Attach existing on-chain identity locally. |
| `smartclaws_sync` | Refresh the local cache. |
| `smartclaws_home_reset` | Clear deployment-bound local state; keep the wallet. |
| `smartclaws_register_group` | Register a named device group. |
| `smartclaws_register_device` | Register a device (plain or encrypted). Kind is for life. |
| `smartclaws_register_agent` | Register an agent (plain or encrypted). Kind is for life. |
| `smartclaws_role_grant` / `smartclaws_role_revoke` | AccessControl roles (`publisher`, `master`, `sender`, …). |
| `smartclaws_reader_list` | Reader ACL on an encrypted channel. Not the same as roles. |
| `smartclaws_reader_grant` / `smartclaws_reader_revoke` | Add or remove encrypted-channel readers. |
| `smartclaws_view_key_generate` | Create a local viewing key (separate from the signing key). Required for encrypted disclose. |
| `smartclaws_view_key_rotate` | Replace the local viewing key. |
| `smartclaws_view_key_register` | Register the active viewing public key on-chain. After funding. |
| `smartclaws_view_key_forget` | Drop the local viewing key. Disclose/register fail until generate. |
| `smartclaws_view_key_remove` | Remove the on-chain public key; local key unchanged. |
| `smartclaws_backup_list` | Named local backups. |
| `smartclaws_backup_create` | Snapshot the HOME (contains the signing key). |
| `smartclaws_backup_clean` | Delete old backups. |
| `smartclaws_backup_restore` | Restore a named backup. |

Read-only tools come with the plugin. Write tools are optional and must be
allowlisted. Guided setup — from this skill to a working agent of one job — is
in `SETUP.md`.

## How the layers fit

The destination of setup is a **working agent of one job**, not a wiring file.
`SETUP.md` is how you get there with the current plugin tools.

- **Plugin tools** — the runtime. Source of truth for addresses, kind, roles.
  `smartclaws_setup_status` is the HOME bar (`ready`).
- **Role skill** — one control or bridge cycle, then it yields. Use it only
  once you can operate as this job, or you will half-run a cycle and guess.
- **Device skills** — topics, payloads, safety. Never guess a payload shape.
- **`SMARTCLAWS.md`** — off-chain wiring: job, which skill per device, labels,
  `authority`, bridge hardware, extra sources, and the owner's **`goal`**.
  Template: `templates/SMARTCLAWS.example.md`. Join on registered `name`. The
  goal is defined during setup and updated when the owner says the mission
  changed — never invented.
- **`AGENTS.md`** — persistent identity, behaviour, authority. Templates:
  `templates/AGENTS.controller.md` and `templates/AGENTS.bridge.md`. Guidelines
  there are extra constraints; they must not contradict `SMARTCLAWS.md` `goal`.

A role skill without an owner-edited `AGENTS.md` has no authority allowlist and
refuses writes. If you cannot yet say you have all as this job, go back to
`SETUP.md` rather than inventing the missing pieces.

## Safety

- Never read, print, or hand-copy wallet files, private keys, or `config.json`
  secrets. `smartclaws_wallet_info` gives you the address — that's all you need.
- Never fabricate transaction hashes, balances, or "registered" / "published"
  confirmations. Report only what a tool actually returned. Encrypted writes
  are stored only when `status` is `published`.
- Don't run destructive commands or wander outside your workspace to "help".
