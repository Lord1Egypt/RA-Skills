# openclaw-telos

![version](https://img.shields.io/badge/version-1.0.1-blue)

**TELOS** (Telic Evolution and Life Operating System) — A personal life OS skill for [OpenClaw](https://openclaw.ai) and [Claude Code](https://claude.com/claude-code).

Captures who you are across missions, goals, beliefs, challenges, and wisdom. Gives your AI a persistent understanding of *you* — so it can give life-aligned advice, not just generic answers.

Based on [Daniel Miessler's PAI Framework](https://github.com/danielmiessler/Personal_AI_Infrastructure).

---

## What It Does

| Feature | Description |
|---|---|
| 📁 **20 Templates** | Full TELOS file set — fill at your own pace |
| 🧭 **Guided Onboarding** | Step-by-step Q&A to fill your core files (Missions → Goals → Beliefs) |
| 🔄 **Safe Updates** | TypeScript scripts handle backup → append → changelog automatically |
| 🧠 **Session Context** | AI reads your TELOS at session start, knows your missions and goals throughout |
| 💡 **Personal Analysis** | When you ask about decisions, career, or investments — AI cross-references your telos |
| 💬 **Conversational** | AI engages with your insights before recording — not just a database, a thinking partner |

---

## Quick Start

### 1. Install

**OpenClaw:**
```bash
openclaw skills install ./telos.skill
```

**Claude Code:**
```bash
git clone https://github.com/sauldataman/openclaw-telos.git
cp -r openclaw-telos ~/.claude/skills/telos
```

### 2. Initialize

Say:
```
setup telos
```

This runs the init script, copies all 20 templates to `~/clawd/telos/`, and walks you through filling the core files.

Or initialize manually:
```bash
bun ~/.claude/skills/telos/scripts/init-telos.ts
```

### 3. Start Filling

The AI guides you through the essentials:
1. **Missions** — What are you ultimately trying to achieve?
2. **Goals** — Specific objectives supporting your missions
3. **Beliefs** — Core beliefs that guide your decisions

No pressure to fill everything at once — TELOS grows with you. The AI learns from your conversations and suggests additions over time.

### 4. Use It

Once set up, the AI automatically:
- Reads your telos at session start
- References your goals and beliefs when advising on decisions
- Flags conflicts between suggestions and your stated missions
- Suggests telos additions when relevant topics come up naturally

Trigger updates anytime:
```
add this book to telos — The Psychology of Money by Morgan Housel
I learned something, add to telos — consistency beats intensity
add to my wisdom — [principle or insight]
I was wrong about [X]
update my goals
telos status
```

---

## Skill Structure

```
openclaw-telos/
├── SKILL.md                    ← Main skill instructions
├── telos.skill                 ← OpenClaw package
├── assets/templates/           ← 20 template files
├── references/
│   ├── onboarding.md           ← Guided setup workflow
│   └── update-workflow.md      ← Update format rules per file
├── scripts/
│   ├── init-telos.ts           ← Initialize ~/clawd/telos/ from templates
│   └── update-telos.ts         ← Safe update: backup → append → changelog
└── evals/
    └── evals.json              ← Test cases for skill evaluation
```

### Scripts

**`init-telos.ts`** — Copies templates to `~/clawd/telos/`. Skips files that already exist (safe to rerun).

```bash
bun scripts/init-telos.ts
```

**`update-telos.ts`** — Updates a telos file with automatic backup and changelog.

```bash
bun scripts/update-telos.ts <file> "<content>" "<description>"

# Example:
bun scripts/update-telos.ts BOOKS.md \
  "- *Dune* by Frank Herbert — power, ecology, and the danger of messiahs" \
  "Added book: Dune"
```

The script:
1. Validates the filename against the allowed list
2. Creates a timestamped backup in `~/clawd/telos/backups/`
3. Appends content (never overwrites)
4. Logs the change in `~/clawd/telos/updates.md`

---

## User Data Structure

```
~/clawd/telos/              ← Your personal data (never shared)
├── TELOS.md                ← Master overview (start here)
├── MISSION.md              ← M0, M1, M2...
├── GOALS.md                ← G0, G1, G2...
├── BELIEFS.md              ← B0, B1, B2...
├── CHALLENGES.md           ← C0, C1...
├── STRATEGIES.md           ← S0, S1...
├── FRAMES.md               ← FR0, FR1...
├── MODELS.md               ← MO0, MO1...
├── NARRATIVES.md           ← N0, N1...
├── PROBLEMS.md             ← P0, P1...
├── PREDICTIONS.md
├── PROJECTS.md
├── TRAUMAS.md              ← TR0, TR1...
├── IDEAS.md                ← I0, I1...
├── BOOKS.md
├── MOVIES.md
├── STATUS.md
├── LEARNED.md
├── WISDOM.md
├── WRONG.md
├── updates.md              ← Append-only changelog
└── backups/                ← Auto-created timestamped backups
```

### Priority Guide

Start with these, fill the rest over time:

| Priority | Files |
|---|---|
| ⭐⭐⭐ Core (fill first) | MISSION.md + GOALS.md + BELIEFS.md |
| ⭐⭐ Important | CHALLENGES.md, STRATEGIES.md, STATUS.md |
| ⭐ Accumulate over time | WISDOM.md, LEARNED.md, BOOKS.md, MODELS.md, FRAMES.md, WRONG.md |
| Optional | TRAUMAS.md, PREDICTIONS.md, MOVIES.md, NARRATIVES.md, PROBLEMS.md |

---

## Numbering System

All entries use cross-referenceable prefixes:

```
M#   Missions      G#   Goals         C#   Challenges
S#   Strategies    B#   Beliefs       FR#  Frames
MO#  Models        N#   Narratives    P#   Problems
TR#  Traumas       I#   Ideas
```

Relationships:
```
MISSIONS (M#)
    └─ supported by → GOALS (G#)
                          └─ blocked by → CHALLENGES (C#)
                                              └─ solved by → STRATEGIES (S#)

BELIEFS (B#)  → guide all decisions
PROBLEMS (P#) → drive GOALS
MODELS (MO#)  → shape understanding
```

---

## OpenClaw Hook (Optional)

For automatic context injection, install the included hook:

```bash
cp hooks/telos-context.js ~/.openclaw/hooks/
```

This gives you:
- **Session start:** AI automatically knows your missions, goals, beliefs from the first message
- **Personal questions:** Relevant TELOS files injected before the AI responds (career question → loads STRATEGIES, book question → loads BOOKS.md, coding question → nothing loaded)
- **Zero overhead:** Non-personal conversations get no TELOS context at all

Without the hook, the skill still works — the AI follows the SKILL.md instructions to load files on demand. The hook just makes it seamless.

---

## Privacy

- `~/clawd/telos/` is **never committed to git** by default
- Templates in this repo contain no personal data
- All personal data stays local on your machine

---

## Compatibility

- **OpenClaw** — Primary target (`.skill` install format)
- **Claude Code** — Copy to `~/.claude/skills/telos/`; compatible with the [Agent Skills](https://agentskills.io) specification
- **PAI** — Templates can be used directly in `~/.claude/PAI/USER/TELOS/`

---

## Credits

- **Original concept**: [Daniel Miessler](https://github.com/danielmiessler) — [Personal_AI_Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure)
- **OpenClaw adaptation**: Saul Dataman ([@sauldataman](https://twitter.com/sauldataman))

---

## License

MIT — see [LICENSE](LICENSE)

---

*"Most people don't believe they have valuable contributions to make. They've never asked who they are, what they're about, and have never articulated or written it down."*

— Daniel Miessler
