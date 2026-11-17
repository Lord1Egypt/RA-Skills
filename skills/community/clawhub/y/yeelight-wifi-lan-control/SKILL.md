---
name: yeelight-wifi-lan-control
description: Control, organize, refresh, and troubleshoot Yeelight WiFi product-line lights through the official local LAN protocol. Use when the user asks to discover or control WiFi lights, rename devices, manage rooms, create overlapping compatible light groups, save/apply scenes, recover a partial write, or create a Host-managed schedule. This Skill is independent of the Yeelight Pro yeelight-home system and never uses cloud, MCP, OAuth, accounts, or Pro homes.
---

# Yeelight WiFi LAN Control

This Skill gives the AI Host a quiet, local-first workflow for Yeelight WiFi lights.
It uses the bundled Node runtime and speaks the public Yeelight WiFi
Inter-Operation Specification over the user's LAN. The user should talk about
lights, rooms, groups, scenes, and schedules; the Host keeps UDP, TCP, CRLF,
support tokens, and numeric protocol parameters invisible.

## Host Contract

The Host must execute the wrapper itself and parse its single JSON response:

```sh
printf '%s' '{"operation":"discover"}' | sh scripts/invoke.sh
```

PowerShell uses `scripts/invoke.ps1` with the same stdin/stdout contract. Never ask
the user to paste protocol commands, IP addresses, raw JSON, credentials, or
network packets. Never call `yeelight-home`, cloud APIs, MCP, OAuth, or a Pro home.

Every physical write request sent to the wrapper must include
`executionRequested: true` and `preview: false`. Persistent or special operations
such as device-side naming, timers, defaults, music mode, recovery, endpoint
rebinding, and store reset also require the user's explicit confirmation. A preview
must never open a control connection that writes.

## First Conversation

1. Explain only the prerequisite that matters: the light must already be powered,
   provisioned into the user's router, on the same LAN, and have LAN control enabled
   when its official app/firmware exposes that setting.
2. Run `discover`. Summarize friendly names, models, online state, and useful
   capabilities. Do not expose raw protocol IDs, endpoints, sender addresses, or
   packet headers.
3. If there are no devices, explain same-network, multicast, and OS local-network
   permission checks. Do not subnet-scan or guess an address.
4. If a saved device's address changed, refresh automatically but pause at
   `rebind_pending`. Show the friendly model/name context and ask once to confirm
   the one-time rebind. Existing aliases, rooms, groups, scenes, and schedules stay
   attached to the stable device identity.
5. For an explicitly supplied private IPv4 address, perform the read-only Yeelight
   handshake and show friendly identity context before saving or writing. Reject
   addresses outside an enabled local interface subnet.

## Everyday Control

Resolve a friendly alias, room, group, or saved scene first. Refresh stale or
unreachable saved targets before writing. Use capability-aware operations such as
power, brightness, RGB, HSV, color temperature, relative adjustment, flow,
foreground/background light, timer, default, name, combined toggle, or music when
the device advertises the required support.

Before any LAN write, expand every selector (device, room, group, scene, and
schedule) into one global device plan. De-duplicate one identical idempotent action.
Reject conflicting actions or repeated `toggle`, relative, and flow actions before
the first network write and ask the user to clarify. Report `verified`,
`acknowledged`, `partial`, `uncertain`, `not_supported`, or `error` exactly as
returned. A TCP acknowledgement is not proof of visible light output.

## Local Home Organization

Persist only explicit user choices in the private local store:

- one named home and user-defined rooms;
- local Unicode aliases, separate from the device's optional protocol name;
- stable device records keyed by protocol identity, with observed endpoint metadata;
- compatible light groups, custom scenes, snapshots, schedules, and bounded recovery
  records.

Devices may belong to multiple groups. A group requires at least two devices with
the same normalized foreground/background control-capability fingerprint. Rooms and
groups are independent. Group writes refresh and revalidate every member. If a
member is offline, awaiting rebind, or lacks fresh capability data, do not write by
default; ask whether to control online members only and report skipped members.
Capability drift puts the group in `needs_review` until membership is repaired.

## Scenes And Recovery

Offer the recommended scenes only as capability-adapted templates. Never infer
presence, tiredness, mood, sleep, occupancy, or routine. Custom scenes can target
the home, room, group, explicit device set, or one device. A snapshot reads fresh
state and stores stable device IDs; dynamic flows that cannot be reconstructed are
reported as omitted rather than guessed.

Multi-device scene application is not transactional. The runtime persists a
pre-state/recovery record before writing, verifies every device, and reports exact
success, skipped, failed, or uncertain rows. Offer `operation.recover` only after
explicit confirmation. Recovery re-reads first and refuses to overwrite state that
has drifted outside the known transition.

## Scheduling

If the Host exposes a scheduler, create a local draft, return the structured
`hostSchedulerRequest`, and let the Host create the exact owned task. Bind only the
returned immutable task ID with `createdBy: yeelight-wifi-lan-control`. If no Host
scheduler exists, keep an inactive local draft and explain that automatic execution
is unavailable. Never install cron, launchd, systemd, Windows Task Scheduler, or a
daemon. Schedule runs pin scene revision/hash, require Host-provided UTC/local/DST
occurrence metadata, derive a private canonical occurrence key, and use a lease.
Malformed or cadence-inconsistent metadata fails before any store lease or device
write; caller-supplied occurrence keys never control deduplication. Runs fail
closed for binding/delete errors or uncertain previous runs.

## Response And Troubleshooting

Keep responses concise and useful: what changed, how it was verified, which devices
were skipped or uncertain, and one next action. Load [workflow.md](references/workflow.md)
for operation routing, [protocol.md](references/protocol.md) for PDF details,
[local-home.md](references/local-home.md) for persistence and refresh behavior,
[scenes.md](references/scenes.md) for scene/recovery semantics,
[scheduling.md](references/scheduling.md) for Host task contracts, and
[troubleshooting.md](references/troubleshooting.md) for stable error guidance.

Never claim physical, firmware, Windows, Host-scheduler, or visual-state evidence
that the current response does not contain. Real-device testing is a separate
authorized activity; package tests use isolated UDP/TCP/music mocks only.
