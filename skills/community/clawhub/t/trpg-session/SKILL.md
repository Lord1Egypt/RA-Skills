---
name: trpg-session
description: "Set up and run TRPG (tabletop RPG) campaigns using OpenClaw multi-agent framework. Creates DM and PC agents with independent personalities, memories, and rule knowledge. Integrates with Discord or Feishu for group play — AI and human players coexist in the same channel, triggered by @mentions. Use when: (1) setting up a new TRPG campaign, (2) creating DM or player character agents, (3) indexing rulebooks or world settings, (4) configuring session logging and memory for ongoing campaigns, (5) managing in-game sessions (initiative, dice, narrative). Triggers: 跑团, TRPG, DND, COC, dungeon master, 开团, 建团, 角色扮演, tabletop RPG, campaign setup."
---

# TRPG Session Framework

Run tabletop RPGs through OpenClaw's multi-agent system — a DM agent narrates and adjudicates,
PC agents roleplay with distinct personalities, and human players join the same Discord channel.

## Architecture Overview

```
Discord Channel (#campaign-name)
├── @DM Agent        — narration, NPCs, rules, dice
├── @PC-AgentA       — AI character with own personality & memory
├── @PC-AgentB       — AI character with own personality & memory
└── Human players    — type freely, @DM for actions
```

**Key principle:** each agent has its own workspace, SOUL.md (personality), and memory scope.
Rules/lore are shared via reference files or vector DB; character secrets stay private.

## Setup Workflow

### 1. Choose a System

Determine the rule system (D&D 5e, Call of Cthulhu, Fate, homebrew, etc.).
This affects which reference files to create. See `references/systems.md` for supported presets.

### 2. Create the Campaign Workspace

```bash
mkdir -p ~/.openclaw/trpg/<campaign-slug>/{rules,lore,characters,sessions}
```

- `rules/` — indexed rulebook excerpts (core mechanics, spells, items)
- `lore/` — world setting, maps, factions, NPCs
- `characters/` — one .md per PC/NPC with stats, backstory, bonds
- `sessions/` — auto-generated session logs

### 3. Create Agents

#### DM Agent

Create via OpenClaw config. Minimal agent definition:

```yaml
# In openclaw config agents section
dm-<campaign-slug>:
  model: anthropic/claude-sonnet-4-6   # or preferred model
  systemPrompt: |
    You are the Dungeon Master for campaign "<Campaign Name>".
    System: <rule-system>
    Your responsibilities:
    - Narrate scenes vividly but concisely
    - Voice all NPCs with distinct personalities
    - Adjudicate rules fairly; roll dice when needed
    - Track initiative, HP, conditions
    - Never act for player characters without permission
    Read your SOUL.md and campaign files for world details.
  soul: ~/.openclaw/trpg/<campaign-slug>/dm-soul.md
  workspace: ~/.openclaw/trpg/<campaign-slug>
  memory:
    scope: agent:dm-<campaign-slug>
  triggers:
    - pattern: ".*"
      channels: ["discord:#<campaign-channel>"]
      mentionOnly: true
```

#### PC Agent (per AI character)

```yaml
pc-<character-name>:
  model: anthropic/claude-haiku-4-5   # lighter model for PCs is fine
  systemPrompt: |
    You are <Character Name>, a <race> <class> in campaign "<Campaign Name>".
    Stay in character. Respond to the DM and other players as your character would.
    You may describe actions, dialogue, and internal thoughts.
    Do NOT roll dice or adjudicate rules — that's the DM's job.
    Read your character sheet and SOUL.md for personality details.
  soul: ~/.openclaw/trpg/<campaign-slug>/characters/<character-name>-soul.md
  workspace: ~/.openclaw/trpg/<campaign-slug>
  memory:
    scope: agent:pc-<character-name>
  triggers:
    - pattern: ".*"
      channels: ["discord:#<campaign-channel>"]
      mentionOnly: true
```

### 4. Write Character Files

Each character gets a `.md` file in `characters/`:

```markdown
# <Character Name>

## Basic Info
- **Race:** Human
- **Class:** Wizard (Level 3)
- **Background:** Sage
- **Alignment:** Neutral Good

## Stats
| STR | DEX | CON | INT | WIS | CHA |
|-----|-----|-----|-----|-----|-----|
| 8   | 14  | 12  | 18  | 13  | 10  |

## HP / AC / Speed
- HP: 18 / Max: 18
- AC: 12 (Mage Armor: 15)
- Speed: 30ft

## Personality
- **Traits:** Curious, bookish, absent-minded
- **Bonds:** Searching for a lost mentor
- **Flaws:** Overconfident in magical solutions

## Backstory
(2-3 paragraphs)

## Inventory
- Quarterstaff, spellbook, component pouch, scholar's pack

## Spells
(list prepared spells)
```

### 5. Index Rules

Convert rulebook excerpts into structured .md files under `rules/`.
Keep each file focused: `rules/combat.md`, `rules/magic.md`, `rules/skills.md`, etc.

For large rule sets, prefer a vector DB plugin (lancedb-pro) for semantic retrieval.
For smaller/homebrew games, .md references with clear headers are sufficient.

### 6. Configure the Discord Channel

- Create a dedicated channel (e.g., `#campaign-name`)
- Add all agents (DM + PCs) to that channel via triggers
- Set `mentionOnly: true` so agents only respond when @mentioned
- Human players just talk normally; @DM to take actions

### 7. Session Management

#### Starting a Session

DM opens with a scene-setting message. The DM agent should:
1. Read the latest session log for continuity
2. Summarize "last time on..." if resuming
3. Set the scene

#### During Play

- Players (human or AI) describe actions
- @DM to request dice rolls or adjudication
- DM agent rolls dice using format: `🎲 d20 + 5 = [roll] + 5 = total`
- DM tracks initiative in pinned message when in combat

#### Ending a Session

Tell the DM: "End session." The DM agent should:
1. Write a session summary to `sessions/session-NNN.md`
2. Update character states (HP, inventory, conditions)
3. Note any plot threads for next session

## Dice Rolling

DM agent uses pseudo-random dice. Format:

```
🎲 <dice>: [result] → total (context)
🎲 d20+5: [14] + 5 = 19 (Athletics check)
🎲 2d6+3: [4, 2] + 3 = 9 (Greatsword damage)
```

Implement via simple random generation in the DM's system prompt instructions,
or use a `scripts/roll.sh` helper for verifiable randomness.

## Memory Architecture

| Layer | Mechanism | Scope |
|-------|-----------|-------|
| **Long-term** | Vector DB (lancedb-pro) or indexed .md files | Rules, lore, backstories |
| **Medium-term** | Session logs in `sessions/` | Campaign continuity |
| **Short-term** | Agent memory scope + LCM | Current session context |
| **Private** | Per-agent memory scope | Character secrets, hidden motives |

## Reference Files

- `references/systems.md` — Rule system presets and quick-start configs
- `references/dm-guide.md` — DM agent behavior guidelines and narrative techniques
- `references/session-template.md` — Template for session log files

## Quick Start Checklist

1. [ ] Decide campaign name, rule system, and setting
2. [ ] Create campaign workspace directory structure
3. [ ] Write or import rule reference files
4. [ ] Write lore/setting files
5. [ ] Create character sheets for AI PCs
6. [ ] Write SOUL.md files for DM and each PC
7. [ ] Add agent configs to OpenClaw
8. [ ] Create Discord channel and configure triggers
9. [ ] Run a test scene to verify all agents respond correctly
10. [ ] Start Session 1!
