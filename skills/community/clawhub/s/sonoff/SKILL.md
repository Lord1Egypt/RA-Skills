---
name: Sonoff
slug: sonoff
version: 1.0.0
homepage: https://clawic.com/skills/sonoff
description: Control and automate SONOFF devices with eWeLink cloud workflows, LAN and DIY mode operations, and safe multi-device execution.
changelog: Initial release with SONOFF and eWeLink workflows for cloud and LAN control, device discovery, command safety, and incident-ready automation playbooks.
metadata: {"clawdbot":{"emoji":"S","requires":{"bins":["curl","jq"],"env":["EWELINK_API_TOKEN"]},"primaryEnv":"EWELINK_API_TOKEN","os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `setup.md` and align activation boundaries, control plane preferences, and write-safety defaults before sending SONOFF commands.

## When to Use

Use this skill when the user needs practical SONOFF and eWeLink execution: cloud API operations, LAN control workflows, DIY mode RPC-like calls, or staged multi-device automations.
Use this instead of generic smart-home advice when outcomes depend on SONOFF-specific eWeLink modes, LAN support differences, and safe rollout behavior.

## Architecture

Memory lives in `~/sonoff/`. See `memory-template.md` for structure and status values.

```text
~/sonoff/
|-- memory.md                 # Core context and activation boundaries
|-- environments.md           # LAN segments, iHost, cloud mode, and endpoint mapping
|-- devices.md                # Device registry, capabilities, and command patterns
|-- automations.md            # Orchestration rules, scheduling, and rollback plans
`-- incidents.md              # Failure signatures and validated recoveries
```

## Quick Reference

Use the smallest file needed for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory and workspace templates | `memory-template.md` |
| Control plane selection | `control-planes.md` |
| Access and auth models | `auth-and-access.md` |
| Device command workflows | `device-operations.md` |
| Multi-device rollout playbooks | `orchestration-playbooks.md` |
| Diagnostics and recovery | `troubleshooting.md` |

## Requirements

- SONOFF devices reachable in target network or eWeLink account access for cloud mode
- For cloud operations: `EWELINK_API_TOKEN` in environment
- For LAN and DIY mode operations: device supports LAN/DIY mode and local reachability

Never ask users to paste production secrets in chat logs. Prefer local environment variables and redacted examples.

## Data Storage

Keep local operational notes in `~/sonoff/`:
- control plane decisions and endpoint mapping
- device capability notes by model and firmware
- automation constraints, canary scope, and rollback rules
- incident signatures and mitigations

## Core Rules

### 1. Select Control Plane Before Any Command
- Choose eWeLink cloud, LAN control, DIY mode, or iHost local API first.
- Block execution when plane is ambiguous because results and state consistency differ across planes.

### 2. Validate Device Capability and Mode Eligibility
- Confirm if each device supports LAN control or DIY mode before local commands.
- Treat unsupported mode assumptions as hard errors, not retryable transient failures.

### 3. Discover Before Write
- Read current status and device metadata before generating command payloads.
- Build writes only with model-valid fields and method paths.

### 4. Use Read-Before-Write and Read-After-Write Loops
- Capture baseline state before every write action.
- Verify final observed state after command execution and stop rollout on mismatch.

### 5. Enforce Explicit Safety Gates for High-Impact Actions
- Start in read-only inspection and dry-run planning mode.
- Require explicit confirmation for power relays, heating circuits, locks, alarms, or bulk updates.

### 6. Keep Cloud and LAN Views Reconciled
- If cloud and LAN states diverge, resolve identity and sync assumptions before more writes.
- Prefer directly observed LAN state for immediate local decisions when reachable.

### 7. Design Automations as Idempotent and Observable
- Use deterministic run ids, bounded retries, and hard stop conditions.
- Record each step with expected state checks to prevent duplicate or partial transitions.

### 8. Preserve Security and Privacy Boundaries
- Use least-privilege credentials and only declared endpoints.
- Read `EWELINK_API_TOKEN` from environment and never persist raw tokens in notes.

## Common Traps

- Assuming every SONOFF model supports LAN or DIY mode -> local calls fail by design.
- Mixing cloud and LAN writes without precedence rules -> conflicting state transitions.
- Sending commands before mode/capability checks -> rejected requests and wrong remediations.
- Running batch updates without canary checks -> broad blast radius on invalid payloads.
- Treating command acknowledgment as final success -> desired state not actually reached.
- Storing cloud tokens in plaintext notes -> unnecessary credential exposure.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| http://<device-ip>:8081/zeroconf/* | Device id and command payload fields | SONOFF DIY mode local control and status retrieval |
| http://<ihost-ip>/open-api/v2/rest/* | Local token and control payloads | SONOFF iHost eWeLink CUBE local API control |
| http://<ihost-ip>/open-api/v2/sse/* | Event subscription parameters | Local iHost event stream and status updates |
| https://*.coolkit.cc | Account-scoped API requests and device command payloads | eWeLink cloud control for SONOFF devices |
| https://dev.ewelink.cc | Integration metadata and docs lookups | Validate eWeLink developer behavior and constraints |
| https://help.sonoff.tech | Documentation query terms | Validate SONOFF DIY and API protocol details |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- local LAN requests or cloud API payloads needed for requested SONOFF operations
- optional local event subscription traffic for iHost SSE workflows

Data that stays local:
- environment mapping, device notes, and playbooks under `~/sonoff/`
- incident timelines and rollback decisions

This skill does NOT:
- use undeclared third-party endpoints
- request bypass or evasion techniques
- store `EWELINK_API_TOKEN` in local skill files
- execute bulk writes without user confirmation and verification strategy

## Trust

This skill sends operational data to SONOFF devices and optionally eWeLink cloud services when execution is approved.
Only install if you trust your LAN environment, iHost deployment, and eWeLink account scope with this automation data.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `iot` - Device connectivity and IoT system integration patterns
- `smart-home` - Home automation architecture and reliability practices
- `api` - API contract design and robust request handling
- `mqtt` - Messaging patterns for telemetry and event-driven orchestration
- `home-server` - Self-hosted service operations and network reliability workflows

## Feedback

- If useful: `clawhub star sonoff`
- Stay updated: `clawhub sync`
