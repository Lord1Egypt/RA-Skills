---
name: smartclaws
description: >
  Entry point for SmartClaws on OpenClaw: teaches what SmartClaws is (publish/read
  IoT telemetry on the SKALE blockchain) and how its plugin tools work, then walks
  the agent and owner through self-setup — plugin, wallet, on-chain identity, role,
  and the skills to install. Trigger whenever someone wants to start, set up,
  onboard, or learn SmartClaws, or when it isn't configured yet.
license: LGPL-3.0-or-later
metadata:
  openclaw:
    emoji: "🦾"
    homepage: https://github.com/skalenetwork/smartclaws
---

# SmartClaws — Learn & Set Up

This is the onboarding skill. It teaches you what SmartClaws is and guides you
and your owner through setting it up. Unlike the other SmartClaws skills, this
one does **not** require the plugin to already be installed — its first job is to
help you get there.

When setup is complete you uninstall nothing; you simply hand off to the role and
device skills you installed. This skill stays available for re-explaining or
re-running setup later.

## What SmartClaws Is

SmartClaws publishes and reads IoT sensor/command data **on-chain** on SKALE.
The chain is the message bus and the source of truth. The pieces:

- **Registry** — one contract that tracks device groups, agents, and channels.
- **Device group** — a named collection of devices an owner controls.
- **Device** — one physical thing (a sensor, a plug). Each device owns two
  **channels**: an *outgoing* channel (telemetry it publishes) and an *incoming*
  channel (commands sent to it). Publishing is role-gated (PUBLISHER for
  telemetry, MASTER for commands).
- **Agent** — an on-chain identity for an AI agent, with two channels: an
  *outgoing* channel (e.g. a decision/audit log it publishes, role-gated by
  PUBLISHER) and an *incoming* channel others can address (role-gated by SENDER).
  Writing to another agent's incoming channel is "notifying" it — the basis for
  agent-to-agent coordination.
- **Channel** — an append-only message log. Messages are SmartClaws *envelopes*:
  `{ v, ts, dev, topic, p }` where `p` is your JSON payload.

You never invent addresses. Channels, devices, and authority come from setup.

## The Plugin Tools (your runtime)

Once the SmartClaws plugin is installed and configured, you have four tools:

| Tool | What it does | Wallet? |
| --- | --- | --- |
| `smartclaws_wallet_info` | Returns the configured wallet address + balance. Never returns a private key. | reads |
| `smartclaws_read` | Reads decoded messages from a device's outgoing channel or a direct channel address. | no |
| `smartclaws_publish` | Publishes an envelope through a device (telemetry), your agent's outgoing channel (e.g. a decision log), or a direct channel. Signs a transaction. | signs |
| `smartclaws_notify` | Sends a message to another agent's incoming channel (needs SENDER_ROLE on that agent). Signs a transaction. | signs |

`smartclaws_publish` and `smartclaws_notify` are write tools and are **optional** —
each must be explicitly allowlisted in the agent config before you can call it.

**What the plugin does NOT do (today):** it cannot create a wallet, register a
group/device/agent, or grant roles. Those on-chain *setup* actions use the
SmartClaws **CLI** (`smartclaws`). Rule of thumb: **run read-only CLI commands
yourself if the binary is available** (`whoami`, `wallet info`, `read`,
`backup list`); **leave anything that creates a wallet, touches a private key,
funds the wallet, registers/signs/spends, or writes/restores a backup to the
owner** (or a session your `AGENTS.md` explicitly authorizes). Never claim you
registered something on-chain unless a CLI command or a `smartclaws_publish` call
actually returned success.

## Setup — run it as a guided flow

Work through these in order. Confirm each before moving on. Stop and ask the
owner whenever a step needs a secret, money (sFUEL), or a decision you can't make.

### 1. Is the plugin installed?

Try `smartclaws_wallet_info`. If the tool exists and returns an address, the
plugin is installed and a wallet is configured — skip to step 4.

If the tool is missing, the plugin isn't installed. Ask the owner to install it
(it ships from this repo / ClawHub as `smartclaws-openclaw-plugin`) and to set,
at minimum, the network in the plugin config:

```jsonc
// plugin config
{ "network": "base-testnet" }
// or an explicit endpoint:
{ "rpcUrl": "https://…", "chainId": 324705682, "registryAddress": "0x…" }
```

You cannot install a plugin into your own host from a skill — guide the owner,
then continue once the tool appears.

### 2. Is there a wallet?

Call `smartclaws_wallet_info`. If it errors with "no wallet", the SmartClaws
HOME has no wallet yet. The plugin can't create one. Ask the owner to run the
CLI once:

```bash
smartclaws init            # interactive: creates wallet + config, picks a mode
smartclaws wallet info     # prints the wallet address + balance
```

`init` also points the HOME at a network and writes the config the plugin reads.
If the owner prefers to import an existing key: `smartclaws init --private-key 0x…`.

Re-running `init` on a HOME that already exists is safe: it prints a summary of
what's there and saves a backup before changing anything (the owner can skip with
`--no-backup`). Owners can also snapshot/restore a HOME with `smartclaws backup`,
`backup list`, `backup clean`, and `backup restore <name>`.

### 3. Fund the wallet (sFUEL)

Reads are free; **publishing signs a transaction and needs sFUEL**. Show the
owner the wallet address from `smartclaws_wallet_info` and ask them to fund it on
the configured network. Re-check the balance before relying on publishing.

### 4. Choose a role / mode

Three modes map to two **role skills** (the operating *procedure* you'll install):

| Mode | When operating you… | Role skill (procedure) |
| --- | --- | --- |
| `controller` / `master-agent` | Orchestrate: read many devices, decide, command devices, log decisions on-chain. | `smartclaws-master-agent` |
| `bridge-agent` | Custody **one** physical device/integration: translate between hardware and its channels. | `smartclaws-bridge-agent` |

If unsure: are you driving hardware directly (bridge) or coordinating on-chain
data and commands (master)? Ask the owner if it's still ambiguous.

**How the layers fit (important).** A role skill is a *triggered procedure* — it
runs a cycle when asked, then yields. It is **not** what makes you persistently a
master or bridge. Your standing identity, behaviour, and authority come from your
**`AGENTS.md`** operating contract, which loads every session (step 7). So: pick
the mode, install the role skill for the *procedure*, and adopt the matching
`AGENTS.md` for the *persistent role*. The device skills are triggered reference
(topics, payloads, safety).

The CLI binds the mode + registers/attaches identity in one step, e.g.:

```bash
# a master/controller with a new group:
smartclaws init --mode controller --create-group home --create-device plug

# a bridge for one device:
smartclaws init --mode bridge-agent --create-agent bridge-1 --create-device novapm
```

(See `smartclaws init --help` for attaching existing entities by name/address.)

### 5. Install the skills you need

Install your role skill and a device contract skill for **every** device you read
or command. From ClawHub:

```bash
clawhub install smartclaws-master-agent      # or smartclaws-bridge-agent
clawhub install smartclaws-device-shelly-plug-s-gen3
clawhub install smartclaws-device-novapm-sds011
```

Device skills define exact topics, payloads, and safety rules. Never guess a
payload shape — install and follow the device contract.

### 6. Record your deployment facts

Create a `SMARTCLAWS.md` at your workspace root binding the reusable skills to
*this* deployment: your role, your channels/devices, and which devices are
commandable. Use the template in `templates/SMARTCLAWS.example.md` as the shape.
The role skills read this file; keep it accurate and never put secrets in it.

### 7. Adopt an operating contract (owner-owned) — your persistent role

This is the step that actually makes you a master or bridge: unlike a skill (which
applies only when triggered), `AGENTS.md` loads every session, so identity,
behaviour, and authority live there. We ship example contracts — behaviour and
structure only, with an empty owner slot:

- `templates/AGENTS.controller.md` — master/controller agents.
- `templates/AGENTS.bridge.md` — bridge/publisher agents.

Offer the matching one, let the owner edit the authority/guidelines, and place the
result at the workspace root as `AGENTS.md`. **Don't invent rules, policies, or
allowlists yourself.** Without an adopted `AGENTS.md`, a role skill will run a
cycle but has no authority allowlist to defer to — so it refuses writes. Adopting
`AGENTS.md` closes that loop.

## Done

After setup you should have: the plugin installed + configured, a funded wallet,
on-chain identity registered, a `SMARTCLAWS.md`, an owner-edited `AGENTS.md`, and
your role + device skills installed. Hand off to the role skill to actually
operate. Re-run any step here whenever the setup changes.

## Safety during setup

- Never read, print, or hand-copy wallet files, private keys, or `config.json`
  secrets. `smartclaws_wallet_info` gives you the address — that's all you need.
  To snapshot a HOME, use `smartclaws backup` (the CLI copies the wallet file
  itself; you never read it) — don't copy wallet files manually. Backups contain
  the private key, so they are owner-managed and stay local.
- Never fabricate transaction hashes, balances, or "registered" confirmations.
  Report only what a tool/CLI actually returned; fail loud otherwise.
- Don't run destructive commands or wander outside your workspace to "help".
