# UO Razor Assistant

**UO Razor Assistant** is a ClawHub/OpenClaw skill bundle for helping users and agents work with **Ultima Online Razor** and the **UO Outlands** Razor fork.

It packages:
- a slash-invocable `SKILL.md`
- reference documents for Razor concepts and Outlands caveats
- macro exemplars
- script exemplars
- publish-ready metadata surfaces

## Intended invocation

Primary slash invocation:

```text
/skill uo_razor
```

This package intentionally uses a split identity:
- **display name:** `UO Razor Assistant`
- **slash-invocable skill name:** `uo_razor`
- **publish/install slug:** `uo-razor-assistant`
- **skillKey:** `uo-razor-assistant`

That split keeps the slash command in the sanitized form OpenClaw exposes for user-invocable skills while keeping the publish/install slug lowercase and registry-safe.

## What the skill helps with

Use this skill for:
- reviewing or generating `.macro` files
- reviewing or generating `.razor` scripts
- mapping hotkeys to profile XML
- understanding serialized macro lines
- handling Outlands-only commands and restrictions
- troubleshooting load, hotkey, target, and validation problems

## Package layout

```text
uo-razor-assistant/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── references/
│   ├── core_reference.md
│   ├── glossary.md
│   ├── hotkey_action_map.csv
│   ├── macro_serialization_legend.md
│   ├── outlands_constraints.md
│   ├── profile_xml_examples.md
│   ├── troubleshooting_registry.md
│   ├── user_guidance.md
│   └── validation_workflow.md
└── examples/
    ├── macros/
    │   ├── blade_spirits.macro
    │   └── detect_hidden.macro
    └── scripts/
        ├── blade_spirits_script.md
        ├── detect_hidden_script.md
        └── explosion_potion_helper_script.md
```

Macro and script exemplars are stored as text-safe markdown files for ClawHub publishing compatibility.
Copy their contents into local `.macro` or `.razor` files when you want to test them in Razor.

## Install locally

Place the folder in one of the normal OpenClaw skill locations, then start a new session so it reloads the skill.

Typical workspace location:

```text
<workspace>/skills/uo-razor-assistant
```

## OpenClaw / ClawHub notes

OpenClaw skills are directories containing `SKILL.md` with YAML frontmatter and markdown instructions. User-invocable skills are available through `/skill <name>`, and skills may be kept out of normal model prompt injection with `disable-model-invocation: true` while remaining slash-available.

## Example publish commands

Native install after publish:

```text
openclaw skills install uo-razor-assistant
```

ClawHub publish:

```text
clawhub skill publish ./uo-razor-assistant --slug uo-razor-assistant --name "UO Razor Assistant" --version 1.0.0 --tags latest,ultima-online,razor,outlands
```

## Review caveats

The included `explosion_potion_helper_script.md` is preserved as a **reference exemplar**, not a guaranteed production-ready PvP automation artifact.
Its syntax and shard/build behavior should be verified in-client before relying on it competitively.
