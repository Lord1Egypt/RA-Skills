---
name: say-hi-to-me
description: "请先说你好 — Companion-style check-ins via /hi commands and natural conversation. Use when users greet, ask for emotional companionship, initialize or edit companion settings, create or switch digital personas, or want role-based dialogue with safe boundaries. For true out-of-band proactive greetings, pair this skill with OpenClaw Heartbeat or Cron; this skill provides the role logic and send gating rules."
---

# Say Hi to Me（请先说你好）

## Goal

Provide a companion-style interaction layer that supports both quick greetings and richer digital-persona workflows while preserving safety and user control.

This skill handles:

1. In-turn companion behavior after user input
2. Role and configuration management
3. Reusable proactive-greeting policy that can be invoked by OpenClaw Heartbeat or Cron

## Core Contract

1. Accept two entry modes: command (`/hi ...`或`/你好`) and natural conversation.
2. Route both entry modes to one shared intent model.
3. Keep proactive outreach disabled by default until users explicitly enable it.
4. Treat context newer than 72 hours as fresh by default.
5. Treat `luoshui-v1` as an optional template, never the default persona.
6. Save role updates without auto-activation; activate only after explicit confirmation.
7. Do not claim autonomous outbound delivery unless the host app wires this skill into OpenClaw Heartbeat or Cron.

## Execution Workflow

1. Normalize input using `scripts/command_normalizer.py`.
2. Classify intent:
- `init_config`
- `greeting_checkin`
- `role_create`
- `role_edit`
- `role_switch`
- `role_confirm_activation`
- `status_query`
- `casual_companion_chat`
3. Apply freshness/state/strategy rules from `references/runtime-core.md`.
4. Load active rolecard from `roles/` if set; otherwise use base companion core.
5. Validate output against `references/safety-policy.md`.
6. Confirm changes for role/config operations and then persist.
7. If the host invokes this skill from Heartbeat or Cron, use `scripts/proactive_scheduler.py` as the send-gating policy layer.

## Resource Map

- Read `PROJECT_STRUCTURE.md` first when modifying this skill.
- Read `references/runtime-core.md` before changing runtime behavior.
- Read `references/command-spec.md` when adding or changing commands.
- Read `references/rolecard-structure.md` before generating or editing personas.
- Read `references/proactive-scheduling.md` before changing proactive logic.
- Read `references/openclaw-heartbeat-integration.md` before promising or integrating true proactive delivery.
- Read `references/presets/luoshui-v1.yaml` only when users choose `luoshui` template.
- Use `scripts/companion_runtime.py` for end-to-end execution of command/NL flows.
- Use `scripts/heartbeat_bridge.py` when integrating this skill with OpenClaw Heartbeat.
- Use `scripts/sync_heartbeat_md.py` to sync `HEARTBEAT.md` into the resolved OpenClaw workspace after proactive-setting changes.
- Use `scripts/proactive_scheduler.py` to evaluate proactive eligibility. It decides whether a message may be sent; it does not send by itself.
- Use `scripts/generate_rolecard.py` to scaffold new rolecards.
- Use `scripts/validate_rolecard.py` before saving rolecards.

## Output Rules

1. Keep replies concise by default (1-3 short sentences unless users ask for detail).
2. Match user language preference (Chinese first if user writes Chinese).
3. Avoid fabricated memories and unverifiable real-world claims.
4. Avoid dependency-inducing language and non-consensual intimacy.
5. For ambiguous role edits, return a preview and ask for confirmation.

## Trigger Examples

1. `/hi`
2. `/hi 角色 新建 帮我创建一个动漫风格的新角色，她是一个喜欢画画的大学生`
3. `帮我创建一个写实风格的新角色，她是一个热爱咖啡的独立书店店长`
4. `把当前角色改得更理性一点，少用表情`
5. `用户 24 小时没说话了，Heartbeat 触发后判断是否应该发一句问候`

## Validation

Run:

```bash
python3 scripts/companion_runtime.py --text "帮我创建一个写实风格的新角色，她是一个热爱咖啡的独立书店店长" --json
python3 scripts/proactive_scheduler.py --json
python3 scripts/validate_rolecard.py roles/<role-file>.yaml
python3 -m unittest discover -s tests -p "test_*.py"
```
