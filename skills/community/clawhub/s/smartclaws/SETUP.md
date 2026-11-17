# SmartClaws — Setup

Read this file only when you are setting up, onboarding, re-running setup, or
you cannot yet say you have everything as this job. For what SmartClaws is,
jobs, modes, tools, and how the pieces fit, stay in `SKILL.md`.

## Where this is going

The destination is **a working OpenClaw agent of one job** — the same
completeness as a live master workspace: plugin tools, a funded HOME, on-chain
identity, device and role skills, a `SMARTCLAWS.md` with a confirmed **goal**,
and, for master/bridge jobs, an owner-adopted `AGENTS.md` that actually lets you
operate. A user proxy is deliberately simpler: it uses plugin tools only when
the user asks and has no role skill.

It is **not** “a YAML file exists.” It is **not** copying
`open-claw-setups/shelly-master-1` (that example is CLI-era custom skills and
hardcoded channels). It is **not** the old four-tool + CLI setup either. Tools
now include initialize, register, roles, viewing keys, disclose, and
`smartclaws_setup_status`. Use those.

Work through the steps. After each one, say what is still missing for
**”I have all as a group-master agent”** (or device-master, device-bridge,
user-proxy). Iterate with the owner. Do not declare done because files exist.
You may say that sentence only when the readiness gate at the end passes.

Two bars, in order:

1. **HOME ready** — `smartclaws_setup_status` reports `state: ready` (or
   `degraded-rpc` with identity already attached). Wallet, network, attached
   identity, and viewing key if you need disclose. Follow that tool’s
   `issues[].recommendedTool`. It does **not** know the job rules below
   (create vs attach, encrypted kind, don’t invent names) — you still apply
   those.
2. **Operational as that job** — wiring, goal, operating contract, skills,
   extra sources the goal needs, cadence, and a real read that works.

Confirm each owner decision before writes. Stop for secrets, funding, or
anything you can’t decide.

## 1. Is the plugin installed?

Call `smartclaws_setup_status`. If the tool exists, the plugin is installed —
read `state` and continue (even `uninitialized` is a valid start). An address
in `smartclaws_wallet_info` means a wallet exists; still do 1.1 before
generating, registering, or publishing.

If the tool is missing, guide the owner to install the plugin and set, at
minimum, the network in the plugin config:

```bash
openclaw plugins install clawhub:smartclaws-openclaw-plugin
openclaw plugins inspect smartclaws --runtime
```

Restart or reload the OpenClaw Gateway after installing or updating the plugin.

```jsonc
// plugin config
{ "network": "base-testnet" }
// or an explicit endpoint:
{ "rpcUrl": "https://…", "chainId": 324705682, "registryAddress": "0x…" }
```

You might not be able to install a plugin into your own host from a skill — if
so, guide the owner, then continue once `openclaw plugins inspect smartclaws
--runtime` shows it loaded.

## 1.1 Tool permissions

Read-only tools load without an allowlist grant. Guided setup also needs the
optional write tools (`initialize`, register, roles, keys, disclose, publish,
backups, …); allowing the plugin id `smartclaws` enables that tool set.

If the owner wants you to run setup, ask them to allow **all SmartClaws plugin
tools**, merge with any existing allowlist, then restart:

```bash
if ! existing="$(openclaw config get tools.alsoAllow --json 2>/dev/null)"; then existing='[]'; fi
merged="$(node -e 'const current=JSON.parse(process.argv[1]); if (!Array.isArray(current)) throw new Error("tools.alsoAllow is not an array"); console.log(JSON.stringify([...new Set([...current,"smartclaws"])]))' "$existing")"
openclaw config set tools.alsoAllow "$merged" --strict-json
openclaw gateway restart
```

Prefer the same list on this agent's `tools.alsoAllow` (or the OpenClaw UI/tool
policy equivalent) rather than globally. Do not replace other plugins already in
the allowlist.

Then test with `smartclaws_setup_status` and `smartclaws_wallet_info`. If those
work but a later write tool is missing, the allowlist still does not cover
optional tools — stop and ask the owner to fix 1.1 before continuing.

This is a temporary setup grant. After you can declare “I have all as …”,
remind the owner to review the allowlist and drop tools they do not want left
on.

## 2. Which network, and which job?

Do not pick a network or a mode yourself. Use the jobs and mode table in
`SKILL.md`. Explain them in plain language, then wait for the owner to confirm.
Generating a wallet needs the network and the job (which sets the plugin mode).
Group create-vs-attach comes after there is a wallet. The owner's **goal** is
a later step — do not skip it, and do not treat the job name as the goal.

**Network.** Named networks today: `base-testnet` (SKALE Base Testnet, chain id
`324705682`) — currently the only named network. If the plugin config already
has a `network`, report it and confirm. Do not invent a custom RPC unless the
owner explicitly wants one.

**Job.** Ask the four jobs from `SKILL.md`. Do not invent a fifth.

## 3. HOME — follow `smartclaws_setup_status`

Call it again. Walk `state` / `issues` until HOME is ready. Do not skip
funding, identity, or (when encrypted) the viewing key because a later file
step looks more interesting.

### Wallet

- **Generate (no CLI).** `smartclaws_initialize` with the **confirmed** network
  and mode from step 2. It creates the wallet locally and never returns the
  private key.
- **Import (needs the `smartclaws` CLI).** The plugin has no import tool — a
  private key must never go through chat. If they want to import, they install
  the CLI and run this in **their** terminal:

```bash
smartclaws init --mode <mode> --network base-testnet --private-key 0x… --yes
```

If they do not want to install the CLI, generate instead.

### Fund

Writes need a funded wallet. Show the address from `smartclaws_wallet_info`
and ask the owner to fund it on the confirmed network. Re-check before writes.
`state: wallet-unfunded` means wait here.

### On-chain identity

Never invent names or addresses. If a write tool is missing, go back to 1.1.

**Plain or encrypted.** If you are **creating** a device or agent, ask before
registering: plain (readable on-chain) or encrypted (sealed; disclose to open).
Kind is **for life** on that entity — changing it means a new device/agent.
Pass `encrypted: true` only when they chose encrypted. If you are only
**attaching** existing entities, do not re-register; look up kind with the
plugin.

If they chose **master of a group**, ask:

> Does the device group already exist, or should I create a new one with this
> wallet (`<address>`)?

Create → this wallet becomes the group owner (`smartclaws_register_group`).
Attach → they give you the group name or address.

If they chose **master of some devices**, do not offer to create a group. If
none exists yet, tell them to create it with another wallet (or another
master/controller agent), then come back with the name or address so this agent
can attach.

Then:

- **User proxy (`controller`):** no agent contract. Attach existing group and
  devices only. Never `smartclaws_register_group` unless they later change the
  job to group master.
- **Device bridge (`bridge-agent`):** exactly one agent and exactly one device.
  Register or attach the agent, but only **pick an existing device** by name or
  address. Do not create a group or device with the bridge wallet. If the
  intended device does not exist, stop: a group owner must deploy it first,
  then grant this bridge wallet `publisher` on that device. The bridge cannot
  grant that role to itself.
- **Master of a group (`master-agent`):** one agent + one group. Create the
  group only if they just confirmed that. Then register devices, then the agent.
  Grant this wallet `master` on devices it must command, and `publisher` on the
  agent if it logs decisions. If the group already exists, attach it; do not
  register a second one.
- **Master of some devices (`master-agent`):** one agent + attach the existing
  group (and those devices). **Never** register a group with this wallet — that
  would make it the owner. After attach, the group master must grant this wallet
  `master` on the devices it should command. Do not call `smartclaws_role_grant`
  / `register_device` unless this wallet is actually the group owner — it
  should not be.

**Encrypted follow-through** (skip if everything is plain — `setup_status` may
still ask for a viewing key; generate and register it if you will disclose):

- After funding, **generate a viewing key** (`smartclaws_view_key_generate`),
  then **register** it (`smartclaws_view_key_register`). Disclose will not
  fall back to the signing key.
- Reader ACL is separate from roles. If this agent is **group master**, grant
  this wallet (and every other wallet that must disclose — device-masters,
  bridges that read encrypted commands) with `smartclaws_reader_grant` on the
  encrypted channels. If this agent is **not** group master, ask the owner /
  group master to grant readers; do not invent grants.

CLI can do identity in one shot if the owner prefers (ask for names):

```bash
# master (master-1) of a new group:
smartclaws init --mode master-agent --create-group home --create-agent master-1 --create-device plug

# same, encrypted device+agent:
smartclaws init --mode master-agent --create-group home --create-agent master-1 --create-device plug --encrypted

# master of some devices (group already exists):
smartclaws init --mode master-agent --group home --create-agent controller-1 --device plug

# user proxy (wallet only, no agent):
smartclaws init --mode controller --group home --device plug

# bridge for one existing device (its group owner grants publisher separately):
smartclaws init --mode bridge-agent --create-agent bridge-1 --device novapm
```

(`smartclaws init --help` for attaching by name/address.)

HOME is not the whole destination. When `setup_status` is `ready`, you still
owe the owner a workspace that can actually run as this job.

## 4. Install the skills you need

Install your role skill and a device contract skill for **every** device you read
or command. From ClawHub:

```bash
clawhub install smartclaws-master-agent      # group/device master only
clawhub install smartclaws-bridge-agent      # device bridge only
clawhub install smartclaws-device-shelly-plug-s-gen3 # if you command/bridge to a shelly plug device

## Others may exist. If some is missing, ask the user.
```

Use `smartclaws-master-agent` for group master and master of some devices. Use
`smartclaws-bridge-agent` for a device bridge. A user proxy installs **no role
skill**: it calls plugin tools only in response to the user's request. The
NovaPM device skill is not published until its executable serial adapter is
restored.

Device skills define exact topics, payloads, and safety rules. Never guess a
payload shape — install and follow the device contract so that different agents work under the same contract.

## 5. What is this agent trying to achieve?

The job (step 2) is *what kind of agent this is*. The **goal** is *what it
should optimize for and how it should operate* — comfort vs cost, ask-first vs
act-ahead, what "good" looks like. These are not the same. Do not skip this,
and do not invent a mission from the device list.

Ask in plain language and wait. Cover at least:

- **Outcome.** What should be true if this agent is doing its job well?
- **Tradeoffs.** When aims conflict (comfort vs savings, freshness vs
  hardware wear, act now vs ask first), which side wins?
- **How it should operate.** Autonomous on a cadence, only when asked, act
  ahead of a limit, fail closed, … — in the owner's words.
- **Hard nos.** Anything it must never do, even if it would help the outcome.

Draft a short `goal:` block from *their* words. Show it. Confirm. Then write
it into `SMARTCLAWS.md` in the next step. If they want to skip, record that
explicitly (`goal` blank or "no standing mission — ask before acting") — that
is not permission to invent a policy later.

A user proxy still needs a goal (often: only act when asked). A bridge's goal
is usually about fidelity and cadence, not control strategy.

This is also how you **change** the mission later: the owner says the
priorities moved; you propose an updated `goal`; they confirm; you write
`SMARTCLAWS.md`. After setup, treat that write like any other setting change
— honor `AGENTS.md` authority. Never silently rewrite the goal.

If the workspace already has OpenClaw `USER.md` / `IDENTITY.md` / `MEMORY.md`,
do **not** leave the mission only in those notes. They can hold who you serve
and what to call people. The SmartClaws mission belongs in `SMARTCLAWS.md`
`goal`.

## 6. Record your deployment facts

Create a `SMARTCLAWS.md` at your workspace root. This file is **off-chain
wiring** — what the chain cannot tell you: job, which device **skill** to
load, labels, whether this agent may command (`authority`), bridge hardware,
other agents you may notify, extra local sources the goal needs, and the
confirmed **`goal`** from step 5.

**Do not treat copied `0x` addresses as source of truth.** Join on registered
`name`. Resolve addresses, channels, encrypted kind, and roles with the plugin
(`smartclaws_list_local`, `smartclaws_discover`, `smartclaws_access_check`).
If YAML and plugin disagree, trust the plugin and fix the file.

Use `templates/SMARTCLAWS.example.md` as the shape. Keep it accurate and never
put secrets in it. For a **user proxy**, omit the `agent` block (`role:
user-proxy`). Record `encrypted: true/false` on each device/agent you list so the
agent does not have to guess kind — it must match registration. Do not omit
`goal` unless the owner confirmed there is no standing mission.

The role skills read this file for skills, policy, and the mission; they
should still pass registered `name` / agent `id` into plugin tools.

## 7. Adopt an operating contract (master/bridge, owner-owned)

This is the step that actually makes you a master or device bridge: unlike a
skill (which applies only when triggered), `AGENTS.md` loads every session, so
identity, behaviour, and authority live there. We ship example contracts —
behaviour and structure only, with an empty owner slot:

- `templates/AGENTS.controller.md` — group-master / device-master agents.
- `templates/AGENTS.bridge.md` — bridge/publisher agents.

A user proxy does **not** adopt either SmartClaws role template. Keep its normal
owner instructions; it has no cycle, decision log, or schedule and uses the
plugin only when the user asks.

Offer the matching one. **Interview** the owner for:

- what people should call you
- who you serve (operator of record)
- who may make you act or change `goal` vs who is read-only
- cadence: only when asked, or scheduled (OpenClaw cron / HEARTBEAT) — the
  role skill runs **one cycle** per invocation and does not loop
- extra knobs that are not already in `goal` (comfort band, cooldowns)

Place the result at the workspace root as `AGENTS.md`. **Don't invent rules,
policies, allowlists, or a second competing mission.** Point *Your Guidelines*
at the `goal` already written; only add constraints the owner actually stated.
Without an adopted `AGENTS.md`, a role skill will run a cycle but has no
authority allowlist to defer to — so it refuses writes.

If `IDENTITY.md` / `SOUL.md` / `USER.md` exist, fill name and who you serve
there too so OpenClaw session context matches. Empty HEARTBEAT is fine when
cron is the clock.

## 8. Extra context the goal needs

If the confirmed goal depends on something that is not a SmartClaws device
(for example a local tariff snapshot), install that source skill and wire it
in `SMARTCLAWS.md` the way that skill documents — e.g.
`smartclaws-tariff-file-source` adds a `tariff:` block. Do not invent a data
source the owner did not ask for. If the goal does not need one, skip.

## 9. Decide whether to schedule (optional)

Ask whether recurring operation is pertinent for this master or bridge. The
owner may choose on-request only, create a schedule now, use another automation
system, or defer the decision. Do not schedule a user proxy.

For OpenClaw, recommend cron with one isolated but stable dedicated session.
`--session-key` routes every recurrence back to the same cron session instead
of creating a fresh session each time:

```bash
openclaw cron add \
  --name smartclaws-<job>-cycle \
  --every <duration> \
  --agent <OPENCLAW_AGENT_ID> \
  --session isolated \
  --session-key agent:<OPENCLAW_AGENT_ID>:smartclaws-cron \
  --no-deliver \
  --message "Run exactly one SmartClaws <master-or-bridge> cycle as specified in the installed role and device skills."
```

Ask the owner to confirm the cadence and delivery before running it. Delivery
options are:

- **None (default/recommended):** keep `--no-deliver`; the dedicated session
  retains the recurring work without sending each result to chat.
- **Last active chat:** replace `--no-deliver` with `--announce --channel last`.
- **Specific destination:** replace it with
  `--announce --channel <channel> --to <destination>`.

Run `openclaw cron list` first. If the intended job already exists, do not add a
duplicate; ask before changing it. If OpenClaw rejects an option, report the
error instead of inventing alternative flags. Record the confirmed choice in
`AGENTS.md`; choosing on-request or deferring scheduling is valid.

## 10. Prove it

Do not publish a command “to test” unless the owner asked. Check, then report
gaps and loop back.

- `smartclaws_setup_status` — HOME `ready` (or `degraded-rpc` with identity
  already attached).
- `smartclaws_list_local` / `smartclaws_access_check` — every device and agent
  in `SMARTCLAWS.md` resolves; `authority: commandable` matches on-chain
  `master` for this wallet.
- For each device you will read: plain → `smartclaws_read` on outgoing;
  encrypted → `smartclaws_disclose` (you must be a reader with a viewing key).
- Encrypted: `smartclaws_wallet_info` says the registered key can open
  disclosures.
- Bridge: local hardware/API fields in `SMARTCLAWS.md` are present; you are
  not guessing a port or URL.
- Master/bridge: role + device (+ source) skills are installed and `AGENTS.md`
  has a real allowlist, not the template comment placeholders.
- User proxy: no role skill or SmartClaws role template is installed; an
  on-request plugin read works.
- Scheduling was discussed when pertinent; on-request or deferred is valid.

## You may say “I have all as a \<job\> agent”

Only when every line for that job is true. Use the job name from step 2
(`group-master`, `device-master`, `device-bridge`, `user-proxy`). Until then,
you are still setting up — say what is left.

| Job | HOME | Identity | Skills | Workspace |
| --- | --- | --- | --- | --- |
| **Group master** | `ready` | This wallet owns the group; devices + agent attached; `master` on devices it commands; `publisher` on the agent if it logs | `smartclaws-master-agent` + a device skill per device + any source the goal needs | `SMARTCLAWS.md` with `goal`, `AGENTS.md` adopted, cadence decided, a live read works |
| **Device master** | `ready` | Group attached (not registered by this wallet); `master` granted by the group owner on the devices it commands; agent attached | same as group master | same |
| **Device bridge** | `ready` | Exactly one agent + one device; `publisher` on that device | `smartclaws-bridge-agent` + that device skill | `SMARTCLAWS.md` with bridge `mode` + `goal` + local hardware; `AGENTS.md`; cadence decided |
| **User proxy** | `ready` | No agent contract; only attached what this wallet already belongs to | No role skill; uses plugin tools on request | `SMARTCLAWS.md` with `goal` (often ask-first); one requested plugin read works |

Then hand a master/bridge off to its role skill. A user proxy simply returns to
normal conversation and uses plugin tools when requested. Re-run any step when
the setup or the goal changes. This skill stays for that.

If 1.1 opened all SmartClaws tools for guided setup, remind the owner to review
`tools.alsoAllow` (and this agent's tool policy) now and remove anything they do
not want left on — especially disclose, register, roles, keys, and backups.

## Safety during setup

- Never read, print, or hand-copy wallet files, private keys, or `config.json`
  secrets. `smartclaws_wallet_info` gives you the address — that's all you need.
  To snapshot a HOME, use `smartclaws_backup_create` or `smartclaws backup` (you
  never read the wallet file). Backups contain the private key, so they are
  owner-managed and stay local.
- Never fabricate transaction hashes, balances, or "registered" confirmations.
  Report only what a tool/CLI actually returned; fail loud otherwise.
- Don't run destructive commands or wander outside your workspace to "help".
