# SmartClaws — mechanics

How messages move, who controls which on-chain permission, and how encryption
and plugin targeting work.

## How messages move

The chain is the bus. Nothing important is a private chat between agents.

1. A **bridge** reads physical hardware (or an API) and publishes an envelope
   to that device's (encrypted or not) **outgoing** channel (`publisher` role).
2. A **master** (group or devices) reads those channels. On a plain channel the
   envelope is already JSON. On an encrypted channel use `smartclaws_disclose`
   to get the same JSON. `smartclaws_read` on encrypted channels returns
   ciphertext — that is success, not an error.
3. If a command is warranted, the master publishes to the device's **incoming**
   channel (`master` role on that device). The bridge reads that channel and
   applies the command to hardware.
4. Masters with an agent contract also write a **decision log** or any other data relevant to their agent **outgoing** channel. Another agent is **notified** by writing to its **incoming** channel (`sender` role on that agent).

> Communication is on-chain as the source of truth. If someone asks an agent to
> do something, that agent does well to log it on-chain as a "user request" or
> similar — the blockchain is the only tamper-proof source of facts.

A **human proxy** has no agent contract. It still uses the same channels, with
whatever the wallet is already allowed to do, only when the human asks.

Topics and payload JSON are defined by **device skills**. Encryption does not
change them — it only seals the envelope in transit.

## On-chain entities and who controls them

| Entity | What it is | Who controls it |
| --- | --- | --- |
| **Registry** | Index of groups, devices, agents, channels | Deployment; you do not own this |
| **Device group** | Named set of devices | **Wallet that registered it** (`Ownable`). Adds devices, grants/revokes. Usually one group master |
| **Device** | One physical thing + two channels | Group is super-admin. Day-to-day: `publisher` (telemetry out), `master` (commands in). Those are AccessControl roles on the **device**, granted by the group owner (or device-admin) |
| **Agent** | On-chain identity + two channels | Agent owner. `publisher` writes the decision log; `sender` may notify the inbox; `agent-admin` grants those |
| **Channel** | Append-only log of envelopes | Writers are whoever holds the matching role on the parent device/agent. Encrypted channels add a **reader ACL** (not a role) |

Plugin job vs these entities:

- **Group master** — this wallet should be the group owner. It grants device
  `publisher` / `master`, agent roles, and encrypted readers.
- **Master of some devices** — not the group owner. Holds `master` on some
  devices (granted by the group master). Must not register the group.
- **Device bridge** — holds `publisher` on one device; in command-enabled
  modes it *reads* incoming commands, it does not need device `master`.
- **Human proxy** — no agent contract. The wallet’s existing roles are the
  ceiling.

`SMARTCLAWS.md` `authority: commandable` is **local policy** (this agent may
issue commands). On-chain `master` is **permission**. You need both to
actually command.

## Encryption, readers, viewing keys

Agents and Devices can have encrypted or plain channels. Kind is chosen at **registration** and is **for life** on that device or agent (both of its channels). Changing kind means a **new** on-chain entity.

### Read vs disclose

| Channel | Tool | What you get |
| --- | --- | --- |
| **Plain** | `smartclaws_read` | Decoded envelopes. No reader list. |
| **Encrypted** | `smartclaws_disclose` | Decoded envelopes. You must be on the channel’s **reader ACL**. |

`smartclaws_read` on an encrypted channel returns labelled ciphertext (success,
not a decode error). To see the payload, use `smartclaws_disclose`. If you may
disclose, do it — same as reading.

`smartclaws_disclose` takes the same `device` / `agent` / `channel` / `side` as
read, plus `fromOffset` (first offset, required) and `count` (1–10, default 1).
The tool will not split a larger range; call again for the next batch. If you
do not know the latest offset, `smartclaws_read` still reports `latest` and
`total`.

**Viewing key** — disclose decrypts with this, not with “being a master.”
Generate one (`smartclaws_view_key_generate`) and register it
(`smartclaws_view_key_register`) **after the wallet is funded**, before the
first disclose. The signing key is never used as a viewing key. Registering a
key that does not match the local one still looks like corrupt data, not
“wrong key.” Check `smartclaws_wallet_info` for whether the registered key can
open messages.

Reader ACL ≠ AccessControl. Granting device `master` does not make someone a
reader. The group master grants readers on encrypted channels for every wallet
that must disclose (this master, other device-masters, a bridge that must
read commands, …).

### Writing to encrypted channels

Same tools as plain: `smartclaws_publish` and `smartclaws_notify`. They detect
the kind. Leave `wait` at its default (`true`). You will see `callbackDeposit`
in the result — that is what the plugin paid automatically, not something you
set (there is no parameter for it).

Treat the message as stored only when `status` is `published`.

| `status` | Meaning | What to do |
| --- | --- | --- |
| `published` | Message is stored | Done |
| `scheduled` | Accepted, not stored yet | Do not send it again. Re-check later |
| `origin-reverted` | Nothing was stored | Safe to send again |
| `ctx-reverted` | Failed after scheduling | Do not send it again. Report the failure |

If the wallet has no funds, ask the owner to fund it — disclose and publish
both need funds.

## Calling the plugin

This skill is meant to be used **with** the plugin. Join key is the
**registered `name`** (or an address). YAML map keys and display `name`s are
not lookup keys unless they exactly match the registered name.

| You want | Pass |
| --- | --- |
| Device telemetry or commands | `device` = registered device `name`, plus side / `deviceChannel` |
| A specific channel | `channel` = `0x…` (always an address) |
| This agent’s log or inbox | `agent` = registered agent `id` or contract `address` |
| Notify someone | `smartclaws_notify` with their agent `id` or `address` |

Prefer live plugin data (`smartclaws_list_local`, `smartclaws_discover`,
`smartclaws_access_check`) for addresses, channel kind, and roles.
`SMARTCLAWS.md` records what the chain does not know (which device skill,
labels, local policy, bridge hardware, the owner's stated **goal**). If a
copied `0x` disagrees with the plugin, trust the plugin.
