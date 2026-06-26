---
name: Shelly
slug: shelly
version: 1.0.0
homepage: https://clawic.com/skills/shelly
description: Control and automate Shelly devices with local RPC workflows, secure access modes, cloud API coordination, and safe multi-device execution.
changelog: Initial release with Shelly local and cloud operations for discovery, command control, telemetry checks, orchestration, and incident-safe rollouts.
metadata: {"clawdbot":{"emoji":"S","requires":{"bins":["curl","jq"],"env":["SHELLY_CLOUD_TOKEN"]},"primaryEnv":"SHELLY_CLOUD_TOKEN","os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `setup.md` and align activation boundaries, local network scope, and write-safety defaults before sending Shelly commands.

## When to Use

Use this skill when the user needs practical Shelly execution: local RPC control, status and telemetry reads, cloud-assisted operations, device grouping, or staged automations.
Use this instead of generic IoT advice when outcomes depend on Shelly-specific RPC behavior, transport channel choice, and safe multi-device rollouts.

## Architecture

Memory lives in `~/shelly/`. See `memory-template.md` for structure and status values.

```text
~/shelly/
|-- memory.md                 # Core context and activation boundaries
|-- environments.md           # LAN segments, cloud context, and endpoint mapping
|-- devices.md                # Device registry, components, and command patterns
|-- automations.md            # Sequencing rules, schedules, and rollback plans
`-- incidents.md              # Failure signatures and validated recoveries
```

## Quick Reference

Use the smallest file needed for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory and workspace templates | `memory-template.md` |
| Protocol and transport choices | `protocol-matrix.md` |
| Access and authentication models | `auth-and-access.md` |
| Device command and state workflows | `device-operations.md` |
| Multi-device rollout playbooks | `orchestration-playbooks.md` |
| Diagnostics and recovery | `troubleshooting.md` |

## Requirements

- Shelly devices reachable in the target local network, or cloud account access for cloud mode
- For cloud operations: `SHELLY_CLOUD_TOKEN` set in environment
- For reliable automation: stable device ids, component ids, and execution boundaries

Never ask users to paste production secrets in chat logs. Prefer local environment variables and redacted examples.

## Data Storage

Keep local operational notes in `~/shelly/`:
- network and endpoint decisions
- device component maps and verified RPC methods
- automation policies, sequencing, and rollback constraints
- incident signatures and mitigations

## Core Rules

### 1. Select the Correct Control Plane Before Acting
- Decide local-only, cloud-assisted, or mixed mode before issuing commands.
- Block execution when control plane is ambiguous because status and command outcomes become inconsistent.

### 2. Resolve Transport Channel by Task and Scale
- Use local HTTP RPC for direct control and deterministic reads.
- Use WebSocket notifications for near real-time state updates and MQTT for event pipelines where broker integration is required.

### 3. Discover Components and Capabilities Before Writes
- Read device status and component layout before command generation.
- Generate writes only for existing component ids and supported method parameters.

### 4. Use Read-Before-Write and Read-After-Write Loops
- Capture baseline state before every write.
- Verify resulting state after execution and stop rollout on mismatch.

### 5. Enforce Explicit Safety Gates for High-Impact Actions
- Start in read-only inspection and dry-run planning mode.
- Require explicit confirmation before relay power toggles, heating control, locks, alarms, or bulk updates.

### 6. Keep Local and Cloud Views Consistent
- Reconcile device identity and state if local RPC and cloud responses diverge.
- Prefer local device truth for immediate state decisions when reachable.

### 7. Design Automations as Idempotent and Observable
- Use deterministic run ids, bounded retries, and hard stop conditions.
- Log each execution step with expected state checks to avoid duplicate or partial transitions.

### 8. Preserve Security and Privacy Boundaries
- Use least-privilege credentials and only declared endpoints.
- Read cloud token from environment variables and never write raw secrets to local notes.

## Common Traps

- Mixing local and cloud control without precedence rules -> conflicting state and duplicate writes.
- Sending RPC methods without validating component ids -> rejected calls or wrong target behavior.
- Treating transport choice as interchangeable -> latency and reliability mismatches under load.
- Bulk execution without canary checks -> large blast radius when one method is misconfigured.
- Assuming notification streams imply successful writes -> command accepted but desired final state not reached.
- Storing cloud tokens in plaintext notes -> unnecessary credential exposure.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| http://<device-ip>/rpc | RPC method names, params, and request identifiers | Local Shelly device control and status retrieval |
| ws://<device-ip>/rpc | RPC messages and event subscriptions | Local WebSocket notifications and event streaming |
| mqtt://<broker> | Device state and command topics with payloads | MQTT-based event and automation integration |
| https://*.shelly.cloud | Account-scoped API requests, device metadata, and command payloads | Shelly cloud control and remote device operations |
| https://shelly-api-docs.shelly.cloud | Documentation lookup queries | Validate Shelly API behavior and method constraints |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- local RPC or cloud API payloads needed for requested Shelly operations
- optional MQTT publish/subscribe payloads in user-configured broker setups

Data that stays local:
- environment mapping, device capability notes, and runbooks under `~/shelly/`
- incident timelines and rollback decisions

This skill does NOT:
- use undeclared third-party endpoints
- request bypass or evasion techniques
- store `SHELLY_CLOUD_TOKEN` in local skill files
- execute bulk writes without user confirmation and verification strategy

## Trust

This skill sends operational data to Shelly devices and optionally Shelly cloud services when execution is approved.
Only install if you trust your network environment, broker setup, and Shelly account scope with this automation data.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `iot` - Device connectivity and IoT system integration patterns
- `smart-home` - Home automation architecture and reliability practices
- `api` - API contract design and robust request handling
- `mqtt` - Messaging patterns for telemetry and event-driven orchestration
- `home-server` - Self-hosted service operations and network reliability workflows

## Feedback

- If useful: `clawhub star shelly`
- Stay updated: `clawhub sync`
