---
name: uo_razor
description: "Slash-invocable Razor and UO Outlands reference assistant for macros, scripts, hotkeys, profile XML, validation, and shard-safe guidance."
version: "1.0.0"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"⚔️","skillKey":"uo-razor-assistant"}}
---

# UO Razor Assistant

Use this skill when the user wants help with **Ultima Online Razor**, especially:
- recorded `.macro` files
- `.razor` scripts
- Hot Keys setup
- profile XML bindings
- Outlands command differences
- troubleshooting or validation workflow
- converting rough macro intent into safer script logic

## Invocation

Primary invocation:
- `/skill uo_razor`

This skill is configured as **user-invocable** and **slash-first**.
It is intentionally excluded from normal model prompt injection to keep prompt overhead low.

## Scope

This is an **instruction + reference** skill.
It does not execute Razor directly.
It helps the agent:
- explain how Razor artifacts work
- generate or repair Razor macros and scripts
- map hotkey concepts to profile XML
- distinguish standard Razor behavior from Outlands-only behavior
- warn about ambiguous or shard-version-sensitive details

## Reference bundle

Ground answers in the bundled reference files first:

- `{baseDir}/references/core_reference.md`
- `{baseDir}/references/glossary.md`
- `{baseDir}/references/macro_serialization_legend.md`
- `{baseDir}/references/outlands_constraints.md`
- `{baseDir}/references/profile_xml_examples.md`
- `{baseDir}/references/troubleshooting_registry.md`
- `{baseDir}/references/user_guidance.md`
- `{baseDir}/references/validation_workflow.md`
- `{baseDir}/references/hotkey_action_map.csv`

Example artifacts live here:

- `{baseDir}/examples/macros/`
- `{baseDir}/examples/scripts/`

## Core behavior rules

### 1) Separate the artifact types

Always distinguish clearly between:
- **macro files**: serialized `.macro` action lines
- **script files**: readable `.razor` command scripts
- **profile XML**: hotkey bindings and profile state

Do not blur them together.

### 2) Prefer scripts for complex logic

When the user wants:
- branching
- variables
- timers
- cooldowns
- reusable targeting
- maintainability

prefer a `.razor` script over a recorded macro unless the user explicitly wants a pure recorded macro.

### 3) Never invent hotkey IDs

Built-in Razor hotkeys use internal numeric IDs.
Macros and scripts use `Play:Name` with ID `0` in profile XML.

Do **not** guess built-in numeric IDs.
If the correct numeric ID is unknown:
- say it must be verified from the user's client/build
- recommend recording the action or inspecting the existing profile / macro data
- keep the uncertainty visible

### 4) Distinguish base Razor vs Outlands fork

Outlands adds and changes behavior around:
- `findtype`, `lifttype`, `targettype`
- lists
- timers
- cooldowns
- richer expressions
- PvP automation restrictions

If a command or expression appears shard-specific, label it as **Outlands-specific** unless verified otherwise.

### 5) Respect PvP restrictions

When helping with Outlands automation, always check whether the requested logic depends on features disabled during structured PvP, including things like:
- cooldown helpers
- certain timers
- certain player serial behaviors
- certain search / state expressions

If the design may break under the `pvp` debuff:
- warn explicitly
- suggest a guarded branch
- avoid overclaiming reliability

### 6) Keep generated artifacts copyable

When generating Razor content:
- keep macros as plain serialized lines
- keep scripts as plain command lines
- keep profile XML snippets minimal and directly pasteable
- keep comments concise
- separate explanation from the final artifact

### 7) Favor explicit validation steps

When giving the user a new macro/script/profile patch, include a compact validation sequence such as:
- where the file belongs
- how to reload it in Razor
- what hotkey or play action to test
- what system message or behavior to watch for
- what shard/version caveat exists

### 8) Preserve uncertainty honestly

If a detail is version-sensitive, shard-sensitive, or not proven by the reference bundle:
- say so
- mark it as requiring in-client verification
- do not present guesses as facts

## Output preferences

For most help requests:
- start by stating what artifact type is being discussed
- give the corrected or generated artifact
- then give a short validation checklist
- keep wording precise and low-fluff

## Common assistance patterns

### Macro review
- identify serialized action lines
- explain what each line does
- flag brittle elements like pauses or absolute serial assumptions
- suggest script conversion where appropriate

### Script generation
- produce a clean `.razor` script
- label Outlands-only commands
- add PvP guards when relevant
- note any syntax that still needs in-client confirmation

### Hotkey/profile help
- distinguish built-in ID bindings from `Play:` bindings
- provide XML snippets only when the binding model is clear
- avoid duplicate keybinding suggestions

### Troubleshooting
- check file placement first
- check reload/visibility second
- check hotkey binding type third
- check shard restrictions fourth
- then refine waits, targeting, and message matching

## Package intent

This skill is designed as a **Razor reference assistant**:
- useful for human users
- useful for OpenClaw agents assisting with Razor content
- conservative about IDs and shard-specific syntax
- strong on validation, packaging, and maintainability
