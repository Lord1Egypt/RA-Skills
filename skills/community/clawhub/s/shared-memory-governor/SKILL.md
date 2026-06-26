---
name: shared-memory-governor
description: Govern a file-based shared-memory layer for OpenClaw multi-agent and subagent systems. Preserve each agent’s private memory while adding a separate, reviewable shared layer for stable user preferences, shared rules, and durable cross-agent facts. Use when designing, initializing, registering, attaching, maintaining, or reviewing a shared-memory system with strict identity isolation, explicit local guidance, and conservative shared promotion.
---

# Shared Memory Governor

Preserve each agent’s private long-term memory.

Add a separate, reviewable shared-memory layer for durable user preferences, shared rules, and cross-agent facts.

Keep assistant-specific identity context private.

## What this skill is for

Use this skill to govern a shared-memory layer across multiple agents while preserving each agent’s private memory system.

This skill helps define:

- what kinds of information may be shared
- what kinds of information must remain private
- how shared-memory files should be organized
- how attached agents should read shared memory in a safe order
- how shared-memory updates should remain reviewable and reversible

This skill is for workspace-scoped shared-memory design and maintenance. It is not a credential tool, not a hidden prompt tool, and not a system-level persistence mechanism.

## Safety boundaries

Follow these boundaries at all times:

- Operate only within user-designated workspace paths
- Process only explicitly approved memory files
- Treat shared memory as supplemental context, not identity-defining context
- Keep assistant-specific identity context private
- Keep shared-memory updates reviewable and reversible
- Keep recurring schedules disabled by default unless the user explicitly enables them

Never:

- read credentials, SSH keys, browser sessions, or unrelated local files
- collect plaintext secrets into shared memory
- alter hidden system prompts or hidden runtime policy layers
- treat assistant identity files as shared-memory sources in v1
- silently enable recurring background schedules

## Core model

Use a two-layer long-term memory model:

1. **Private memory layer**
   - Each agent keeps its own curated memory notes
   - Each agent keeps its own daily memory files
   - Each agent keeps its own local assistant-specific context

2. **Shared memory layer**
   - Store shared files under the shared root directory
   - Use this layer for stable user preferences, shared rules, and durable cross-agent facts
   - Treat this layer as part of the long-term memory workflow
   - Do not use this layer for assistant-specific identity context

## Core principles

Follow these rules at all times:

1. Preserve private memory systems
2. Share user-level and cross-agent durable context, not assistant-specific identity context
3. Read private memory first, then shared memory
4. Treat shared memory as supplemental background
5. Never let shared memory override assistant-specific identity context or private identity guidance
6. Do not auto-delete private entries after promotion to shared memory
7. Require explicit local guidance for participating agents
8. Keep assistant identity context private in v1
9. Prefer conservative promotion decisions

## Shared memory structure

Use the shared root with this default structure:

```text
<sharedRoot>/
├── shared-user.md
├── shared-memory.md
├── shared-rules.md
├── shared-sync-log/
│   ├── YYYY-MM-DD_HHMM_scan.md
│   └── YYYY-MM-DD_HHMM_maintenance.md
└── archived/
    └── <agent>/
```

### File roles

- `shared-user.md` → stable user preferences, habits, and constraints
- `shared-memory.md` → durable facts reusable across agents
- `shared-rules.md` → governance rules for the shared-memory system
- `shared-sync-log/` → operational logs for review and traceability
- `archived/<agent>/` → archived local shared-memory guidance after detach

For detailed file-boundary examples, read:
- `references/shared-promotion-rules.md`

## High-level workflows

### 1) Initialize the shared-memory system

Use when the shared layer does not exist yet.

Goal:
- create the shared root structure
- create base shared files
- create the default config
- prepare shared scan and shared maintenance schedules in a disabled-by-default state

Use:
- `init`

For config details, read:
- `references/config-reference.md`

### 2) Register and attach an agent

Use when an agent should participate in the shared-memory system.

Goal:
- add the agent to the participant set
- create or update local shared-memory guidance
- make the shared read path explicit and reviewable

Use:
- `register <agent>`
- `attach <agent>`

For startup guidance placement and cleanup rules, read:
- `references/startup-guidance-rules.md`

Important:
- `register` does not automatically mean `attach`
- updating local guidance files does not retroactively change what an already-running session has loaded

### 3) Review status and local readiness

Use when checking whether the shared-memory system is set up correctly.

Goal:
- inspect global shared-memory status
- review whether each attached agent has complete local guidance
- review schedule consistency against config

Use:
- `show-status`
- `review-attachments`
- `show-config`
- `validate-config`

For status and reporting fields, read:
- `references/status-review-fields.md`

### 4) Run shared promotion

Use when updating the shared layer from approved upstream memory sources.

Goal:
- review approved local memory sources
- identify cautiously promotable shared candidates
- update shared-memory files conservatively
- record a scan log and summary

Use:
- `run-shared-scan`

Default rule in v1:
- shared promotion should be conservative
- single-agent local items should be skipped by default unless they have explicit shared-scope justification

For promotion decisions and target-file boundaries, read:
- `references/shared-promotion-rules.md`

### 5) Run shared maintenance

Use when reviewing and refining the shared layer itself.

Goal:
- deduplicate shared entries
- merge or refine overlapping entries when appropriate
- prune outdated shared content
- update governance notes when needed

Use:
- `run-shared-maintenance`

For reporting fields and maintenance review structure, read:
- `references/status-review-fields.md`
- `references/config-reference.md`

### 6) Repair, detach, or remove an agent

Use when local shared-memory guidance is incomplete, stale, or no longer needed.

Use:
- `repair-attachment <agent>`
- `detach <agent>`
- `unregister <agent>`

Rules:
- detach should remove local shared-memory guidance, not private memory
- unregister should normally happen after detach when local guidance is still active

For startup guidance repair and detach cleanup rules, read:
- `references/startup-guidance-rules.md`

## Reference map

Read these files only when needed:

- `references/startup-guidance-rules.md`
  - local startup guidance placement
  - fallback placement
  - attach success criteria
  - detach cleanup behavior

- `references/shared-promotion-rules.md`
  - shared-scope validation
  - promotion categories
  - target-file boundaries
  - promotion report fields

- `references/status-review-fields.md`
  - status display fields
  - attachment review fields
  - schedule consistency outcomes
  - maintenance report section order

- `references/config-reference.md`
  - config schema
  - field meanings
  - config-related command behavior
  - schedule/config consistency rules

## Commands

V1 supports:

- `init`
- `show-config`
- `validate-config`
- `update-config`
- `register <agent>`
- `unregister <agent>`
- `attach <agent>`
- `detach <agent>`
- `repair-attachment <agent>`
- `run-shared-scan`
- `run-shared-maintenance`
- `show-status`
- `review-attachments`
- `show-sync-logs`
- `prune-sync-logs`

Config-related commands may support explicit config paths.

## Default operating stance

Keep this skill:

- low-intrusion
- explicit
- auditable
- configuration-driven
- strict about identity isolation
- conservative about write authority
- centered on governance rather than hidden magic
