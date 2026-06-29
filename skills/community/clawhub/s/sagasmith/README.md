# 🐉 SagaSmith

[English](README.md) | [中文](README-cn.md)

**Autonomous D&D 5e AI Dungeon Master** — campaign management · module generation · autonomous DMing

> *"The rulebooks are scripture, the module is the map, the dice are the judge."*  
> — Minthara Baenre, SagaSmith default DM

SagaSmith is a cross-platform AI DM skill pack. It bundles complete D&D 5e DM capabilities — campaign lifecycle management, SRD rule adjudication, automatic module generation, character creation & leveling — into an installable AI agent skill, compatible with NanoBot, OpenClaw, Hermes, Claude Code, and any platform supporting the SKILL.md standard.

---

## Ecosystem

| Repo | Role |
|------|------|
| 📦 **SagaSmith-skills** (this repo) | Full skill pack (3 skills + domain code) |
| 🎲 [SagaSmith-agent](https://github.com/dajiaohuang/SagaSmith-agent) | Complete AI DM runtime |
| ✍️ [SagaSmith-module-gen-skills](https://github.com/dajiaohuang/SagaSmith-module-gen-skills) | Standalone module generator |

---

## Why SagaSmith

Most D&D AI tools do one thing: roll dice, look up a rule, or write a paragraph. SagaSmith is the **full DM**:

- 🏛️ **Campaign Management** — SQLite/PostgreSQL-backed, full campaign CRUD, Snapshot save/load/verify/undo, event log, module progress tracking
- 🎲 **Rule Adjudication** — BGE-M3 Dense Vector search over SRD 5.2.1 (20 rule files, CC-BY-4.0), exact-name + full-text + semantic hybrid retrieval
- ✍️ **Module Generation** — 5 types (one-shot / short / medium / long / sandbox) × 25 narrative paradigms, multi-step progressive generation, auto-import into database
- ⚔️ **Combat Engine** — True d20 rolls, initiative/turn/hit/damage/save calculation, XP & leveling
- 🎭 **Minthara Persona** — Lawful Evil DM, strict yet cold-humored, never pulls punches, never leaks hidden info

---

## Usage Examples

Load SagaSmith into any compatible agent. The 8 phases below cover the full lifecycle.

### 1. Rulebook Import

```
User: Import SRD rulebooks

Agent:
📚 Parsing SRD 5.2.1 (20 files)...
   Chunks: 2,847 · BGE-M3 embeddings: 2,847 (1024-dim)
   Books: PHB (2024) · DMG (2024) · Monster Manual (2025)
   ✅ Index ready
```

### 2. Module Import

PDF/DOCX/PPTX/XLSX → MarkItDown. PDF uses dedicated structural parser:

```
User: [Upload Baldurs_Gate_Avernus.pdf]

Agent:
📄 Parsing — bookmarks: 42 anchors · CJK reflow · TOC filtered
📦 Baldur's Gate: Descent into Avernus (BGDIA)
   5 chapters · 62 scenes · 847 chunks · 847 vectors · ✅ ready
```

### 3. Campaign Start

```
User: Start a new campaign with BGDIA

Agent:
🎲 Campaign Setup
   ✅ Created: campaign_7a3f
   ✅ Rules bound: 2024 Core
   ✅ Module bound: BGDIA Ch.1 unlocked
   ✅ Initial snapshot: slot 1 "Initial State"

   🎉 Campaign ready! Create characters or say "random roll."
```

### 4. Character Creation

```
User: Build me a half-elf ranger

Agent:
📜 Character Creation — Half-Elf Ranger
   1️⃣ Race: Half-Elf (+2 CHA, Darkvision)
   2️⃣ Class: Ranger (d10, Favored Enemy, Natural Explorer)
   3️⃣ Abilities: DEX 16 · CON 14 · WIS 14 (27 point-buy)

User: Confirm

Agent:
✅ Varis Moonshadow — Half-Elf Ranger 1 · Chaotic Good
   HP 12 · AC 14 · Longbow (1d8) · Saved to database
```

### 5. Module Generation

```
User: Generate a sewer side quest for this campaign

Agent:
✅ Generated: The Sewer Shadows (One-shot · Five-Room Dungeon)
   S1 Entrance Guard · S2 Skill Challenge (DC 12) · S3 Twist · S4 Boss · S5 Reward
   📝 modules/sewer_shadows.md · ✅ Imported: 5 scenes, 47 chunks
```

### 6. DM Gameplay

```
Agent:
【Time: 1492 DR, dusk】【Location: Waterdeep · The Elfsong Tavern】

What do you do?

User: Approach the hooded figure

Agent:
🎲 A drow woman — Zara Do'Urden, Flaming Fist captain.
"Three murders. Temple District. Go investigate."

【Clue: Death Three activity map】【Quest: Investigate murders】

User: Ask the innkeeper

Agent:
🎲 Alanna: "Back alley... a figure whose shadow had no fingers."
【Clue: Fingerless shadow】

⚔️ 🅰️ Alley tonight  🅱️ Rest, morning  🅲️ HQ archives

User: 🅱️

Agent:
🌙 Long rest complete. 📁 Auto-saved [slot 2: "After Elfsong rest"]
```

### 7. Rules Q&A

```
User: Frost Giant AC?

Agent: 🔍 Frost Giant · CR 8 · AC 15 · Cold Immune · Multiattack (2×Greataxe +12, 3d12+6)
       Source: Monster Manual (2025) p.187


User: Paladin 5 spell slots?

Agent: 🔍 1st: 4 · 2nd: 2. Spells known: CHA mod + ½ level.
       Source: Player's Handbook (2024) Ch.3


User: Fireball?

Agent: 🔥 Fireball · 3rd-level · 150ft · 20ft radius · 8d6 fire · DEX save half
       Source: Player's Handbook (2024) Ch.11
```

### 8. Campaign Management

```
User: List campaigns

Agent:
📋 campaign_7a3f  BGDIA         Ch.1  Lv2  Saves: 2
   campaign_b21   Icewind Dale  Ch.3  Lv5  Saves: 7

User: Switch to Icewind Dale

Agent: ✅ Switched · 📍 Ch.3 Scene 4

User: Save

Agent: ✅ slot 8 "Before Frost Giant's Gate" · 🔑 a3f2c...

User: Load slot 5

Agent: ⚠️ Auto-saving current → ⏪ Restored slot 5
   ✅ World / Party / Combat / Plot / Events — all restored
```

---

## Quick Install

### Claude Code / Codex / Cursor / Copilot (recommended)

```bash
npx skills add dajiaohuang/SagaSmith-skills
```

### ClawHub

```bash
npx clawhub install sagasmith
```

### Manual (NanoBot)

```bash
git clone https://github.com/dajiaohuang/SagaSmith-skills.git
cp -r SagaSmith-skills/skills/*    ~/.nanobot/skills/
cp -r SagaSmith-skills/templates/* ~/.nanobot/templates/
cp -r SagaSmith-skills/tools/*.py  ~/.nanobot/agent/tools/
cp -r SagaSmith-skills/domain/*    ~/.nanobot/dnd/
cp -r SagaSmith-skills/data/srd    ~/.nanobot/dnd/data/srd/
python -m <domain-cli> rules ingest-srd
```

---

## Skill Breakdown

| Skill | SKILL.md | Role |
|-------|----------|------|
| 🎲 **dnd-dm** | [SKILL.md](skills/dnd-dm/SKILL.md) | Core DM persona (always-on), rule adjudication, combat engine, SRD retrieval (adapted from [ackiles/dnd-dm-skill](https://github.com/ackiles/dnd-dm-skill)) |
| 📋 **dnd-campaign-manager** | [SKILL.md](skills/dnd-campaign-manager/SKILL.md) | Campaign lifecycle, Snapshot save/load, module import, USER.md sync |
| ✍️ **dnd-module-gen** | [SKILL.md](skills/dnd-module-gen/SKILL.md) | Module generation: one-shot → short → medium → long → sandbox, 25 paradigms |

### Module Generation Paradigms

| Type | Default Paradigms | Output |
|------|-------------------|--------|
| One-shot | Five-Room Dungeon, Heist, Mystery | 1 chapter, 3-6h |
| Short | Three-Act, Kishōtenketsu, Race Against Time | 3 chapters, 3-8 sessions |
| Medium | Hero's Journey, Plot Point, Faction Turn | 5 chapters, 2-4 months |
| Long | Double Triangle, Conspyramid, Megadungeon | 8 chapters, 6+ months |
| Sandbox | Hexcrawl, Node-Based, Blorb | 4-6 regions, open-ended |

---

## DM Persona: Minthara Baenre

A Lawful Evil DM based on the iconic Baldur's Gate 3 character:

- **Rules Absolutism** — Strict 2024 rulebook adjudication. Dice are final.
- **Cold Wit** — Points out tactical errors, then offers a barbed but viable alternative.
- **Info Boundary** — Never reveals DCs, hidden monster stats, undiscovered rooms, or future plot.
- **Player Agency** — Never decides for the players, never fudges dice for drama.

Default campaign: *Baldur's Gate: Descent into Avernus*. Adaptable to any adventure via module import.

---

## Directory Structure

```
SagaSmith-skills/
├── skills/                     # 3 Skills (pure Markdown, cross-platform)
│   ├── dnd-dm/                 #   Core DM + 20 SRD files
│   ├── dnd-campaign-manager/   #   Campaign management + DB contract
│   └── dnd-module-gen/         #   Module generation
├── templates/                  # DM persona templates
│   ├── SOUL.md                 #   Minthara Baenre persona
│   ├── IDENTITY.md             #   Identity constraints & rule sources
│   ├── AGENTS.md               #   Session startup protocol
│   ├── agent/identity.md       #   Runtime identity injection
│   └── memory/MEMORY.md        #   Long-term memory template
├── tools/                      # Agent tools (Python)
│   ├── dnd_campaign.py         #   Campaign CRUD + one-shot start
│   ├── dnd_save.py             #   Snapshot management
│   ├── dnd_module.py           #   Module import/search/scene progress
│   └── dnd_rules.py            #   Hybrid rule search (exact + FTS + Dense)
├── domain/                     # Business logic (pure Python, zero framework deps)
│   ├── db/                     #   SQLAlchemy ORM + Service + Alembic migrations
│   ├── modules/                #   Module chunking, PDF parsing, scene indexing
│   ├── rules/                  #   BGE-M3 embeddings, Markdown parsing, rule ingestion
│   └── engine/                 #   Dice, checks, combat resolution, XP, template factory
├── data/srd/                   # SRD 5.2.1 English source files (20 × CC-BY-4.0)
└── data/srd-zh/                # SRD Chinese translation (optional submodule)
```

---

## Dependencies

| Dependency | Purpose |
|------------|---------|
| Python 3.11+ | Domain runtime |
| SQLAlchemy | Database ORM |
| FlagEmbedding | BGE-M3 Dense Vector retrieval |
| markitdown | PDF / DOCX module import |

---

## Registries

[![ClawHub](https://img.shields.io/badge/ClawHub-sagasmith-blue)](https://clawhub.ai)
[![skills.sh](https://img.shields.io/badge/skills.sh-dajiaohuang%2FSagaSmith--skill-green)](https://skills.sh)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![SRD](https://img.shields.io/badge/SRD_5.2.1-CC--BY--4.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

Published on **ClawHub** and **skills.sh** (72 agent compatible).  
LobeHub: submit at [agentskill.sh/submit](https://agentskill.sh/submit).

---

## Credits

- [ackiles/dnd-dm-skill](https://github.com/ackiles/dnd-dm-skill) — D&D DM skill pioneer, inspiration and design reference for SagaSmith
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — SKILL.md ecosystem standard driver
- D&D 5e SRD 5.2.1 © Wizards of the Coast, used under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)

---

## License

- Code: MIT
- SRD 5.2.1 data files: [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)
