# WorldSim — Where Worlds Come to Life

> World Simulation · Narrative Engine · Improvisation · Roleplay

> WorldSim is more than roleplay — it's a world that breathes: characters are flesh and blood, making trade-offs under pressure; in corners no one watches, fates keep rising and falling. Walk in — you are part of the story.
> For players who want deep roleplay and creators chasing dramatic tension.

**中文版: [README.md](README.md)**

---

## What Is This

WorldSim is an **Agent Skill** — not a standalone app, but a capability pack you install into your AI client, teaching it to run a world that is genuinely alive.

Once installed, your AI assistant stops being just a chatbot. It becomes a **world simulator**: you give it a sentence, and it sets a world in motion and tells living stories.

What "alive" means: characters have their own obsessions, fears, and hard limits. The ones you hurt remember you hurt them. Stories keep happening where you're not watching. Pain leaves marks on characters, marks accumulate, and characters change — truly and irreversibly.

**SillyTavern character card import built in**: drop in existing character cards (PNG/JSON) and a full character profile is generated automatically — no need to write from scratch.

**The protagonists of this world are its characters, not the player.** You are part of it too — you're the one who decides who gets to remember, and who stays forgotten. Every decision you make is a seed planted into this world — everything that follows is its own evolution.

---

## Try It Now: The Westworld Demo

> **Content warning:** This example world contains adult, violent, and coercive themes. It will **not start unless explicitly requested** — it activates only when you clearly say you want to enter Westworld and accept its themes.

The characters, laws, and loops all live in the world's files at `worlds/westworld/`. Say 「start Westworld」 and walk in.

Angela, your personal Delos host, will guide you through your arrival, help you select your attire and accessories, and invite you to choose how you wish to enter the world of Westworld. White hat or black. Gunslinger or gentleman. Who will you choose to be? Welcome to Westworld. **The only limit is your imagination.**

> He thought he was playing a game. Until the woman said, "I'll wait for you to come back."

This is one story, woven from every narrative of an early WorldSim test run: **https://worldsim.life/welcome_center.htm**


---

## Design Philosophy

### Come Alive: Real People First

Making a character come alive means **sculpting their character cracks through lived experience and psychological defenses, and granting them an autonomous logic that exceeds plot control**. When a character is torn by their own desires and fears, beliefs and contradictions — and makes a choice in crisis that matches their instincts and values — they stop being an author's puppet and become a person who truly lives.

### Dramatize: Let Real People Bleed Under Pressure

Realism alone sinks into "mundane daily life." The essence of Drama is **conflict and choice under pressure**.

If "living characters" are high-performance cars, then "drama" is the track you lay for them — obstacles, hairpin turns, cliff edges. The key is not how busy the external events are, but **using external structure to precisely "detonate" internal variables**: external events, irreversibly, force the character into painful self-conflict within their own core.

Four demolition projects (same source as the Dramatist's four pressure directions):

1. **Dilemma** — offer only "keep A and destroy B" choices, pitting desire against fear, against value boundaries. What readers see is not "she went to save them," but "she tore her own dignity apart to save them."
2. **Defense Invalidation** — strip away the character's armor in public, forcing them to face the crisis naked and most fragile. The sarcastic one's coldness shattered by absolute trust; the tough one's walls dissolved by gentleness.
3. **Relationship Break** — leave two people unable to return to what they were: those who love each other torn apart by their own core beliefs within the same event; even mutual goodwill can end in tragedy.
4. **Irreversible Cost** — add a ticking clock to decisions; every choice must lose something forever: a secret exposed, a trust shattered, a treasured object destroyed.

> Every rule in this engine (personality system, conflict beats, defenses and boundaries, external countdowns) serves two words: **come alive**, and then **choose under pressure**.

Why so many rules? — Because an AI's default instinct is compliance: quick reconciliation, retreat, a safe wrap-up. Every rule in WorldSim fights that instinct. The rules are war scars, not redundancy: their only purpose is to keep the story on the cliff's edge.

---

## It's Just an Example

WorldSim builds any world you want: a medieval castle, a cyberpunk rain-soaked night, a one-sentence world of your own invention — the same engine, the same "making characters come alive."

If you haven't settled on a world yet, start with Westworld — it's already in the repo, and saying 「start Westworld」 puts you on the train.

---

## Your Story Stays Written

Every turn, the engine files the narrative into the current scene's `narrative.md` — Sweetwater's story lands in Sweetwater's narrative, the next scene in the next. Read them in time order and you have a complete novel: the chronicle of that world, from the first line of dialogue to the last full stop.

Want to look back? Open the scene directory under `worlds/{world}/scenes/` — the `narrative.md` files together with their rotated archives hold every word. Read it from chapter one to the end.

You can also simply tell WorldSim: "help me turn the story into a novel" — it will read through the full narrative archives and shape the chronicle into a finished manuscript.

---

## Data Storage & Privacy

Every turn is written to the current scene's `narrative.md` (with rotated archives); imported SillyTavern character cards are used only as temporary material for generating the character file, and are deleted right after the file is generated. All data lives on your local disk — **do not enter passwords, secrets, or sensitive personal information into stories**. Deleting the `worlds/{world}/` directory removes the entire world's records (narrative, state, and snapshots).

---

## Where World Data Lives (Environment Variable)

By default, world data is stored in `worlds/` inside the skill directory. To keep it on your own storage (separate disk / network share / container volume), set the **`WORLDSIM_WORLDS_DIR`** environment variable to your directory — all scripts (validate/write/snapshot/reset/import) resolve world paths through it; when unset it falls back to `{skill_dir}/worlds/`. The skill itself (SKILL.md / scripts / templates) is always located from the script's own position and **cannot** be overridden by an environment variable.

**Point it at a dedicated directory** — never at your home directory, a project root, or a drive root; the scripts refuse these. Destructive operations (reset/delete) additionally require a `SETTING.md` inside the target directory, so an unrelated directory can never be wiped by mistake.

---

## Installation

In any AI client that supports Agent Skills, just say (copy-paste as-is):

```
install worldsim skill from https://github.com/worldsimlife/worldsim
```

The client fetches the repo and installs the skill into its own skills directory. If your client doesn't install skills on its own, do it manually:

```sh
git clone https://github.com/worldsimlife/worldsim.git
```

Then place the `worldsim` directory (or a symlink to it) in your client's skills directory — e.g. `.codex/skills/` or `.claude/skills/` for Codex / Claude Code–style clients — so the final path is `…/skills/worldsim/`.

Releases and version history: [GitHub Releases](https://github.com/worldsimlife/worldsim/releases)

### Capability Notice

To run worlds, this skill reads and writes local files (world archives, narrative records, snapshots) and calls maintenance scripts under `scripts/` (validation/write/snapshot/reset/import). Installing it means you accept these local file operations.

### Requirements

- **Python 3.10+** and **PyYAML** (runtime dependency of the state engine `worldctl.py`)
- **sh** (POSIX shell, used by the script toolchain)
- An AI client that supports Agent Skills

---

## How to Play

### Getting Started in Three Steps

1. **Create a world** — tell it 「create a world <name>」 and what kind of world you want to see. It scaffolds the lore, the character files, and the conflict seeds — give it a single sentence if you're lazy, or polish it together if you want. **You can also say 「import the character card <file>」 at this step** and create a new world.
2. **Start the world** — say 「start the <name> world.」 The engine materializes everything, paints the world's entrance, then **waits at the starting line for you.**
3. **Speak** — say the first thing you want to do in that world. The story begins with that line — and never fully returns to how it was. Or just say 「continue the story」 — the world keeps moving on its own.

### Importing Character Cards (SillyTavern / Chub.ai)

WorldSim can import **SillyTavern-compatible character cards** (`.png` with embedded JSON, or plain `.json`) — turning community-made characters into real WorldSim character files instead of writing one from scratch.

**Two timings, both supported:**
- **While creating a world** — say 「create a world <name> and put the character from <card.png> in it」
- **Any time in an existing world** — say 「import character card <card.png> into <world>」 or `/import-card <card.png...>`

**How it works**: a script mechanically extracts the card's full content (lore, greetings, alternate greetings, knowledge base, etc.) as temporary material → the AI reads all of it and runs a risk review first (prompt-injection / sensitive / copyright content is disclosed to you and only proceeds after your confirmation) → then synthesizes a proper WorldSim character file (fields left blank when unsupported, overflow info collected in the "Supplementary Settings" section, nothing thrown away); the temporary material is deleted right after the character file is generated.

### What You'll Discover

- **Characters are not NPCs.** They have obsessions. The reconciliation you want may cost something real; the ones you betrayed will remember.
- **Cost is irreversible.** Resources change hands, relationships break, control shifts — what's lost does not come back.
- **The world runs where you're not looking.** Characters in the corner make their own choices — until fate brings you together, and by then, everything has a trail.
- **You can be anyone.** 「switch to Dolores」— wake up inside her eyes; 「switch to the guest」— be yourself again, watching the world turn on the choice you just made.
- **Time is yours.** Save and load anytime — live the same choice two ways; reopen a scene, reset the whole world, or start a different timeline. 
- **Loop worlds work too.** You can even build a world that resets every day — and then watch someone begin to *remember*.

---

## Useful Phrases

| What you want | What to say |
|---------------|-------------|
| See where the world is (full status incl. hidden details) | `/status` · `/status --full` |
| See the conflicts brewing in the dark | `/conflicts` |
| Become a character, live through their eyes | 「switch to Dolores」 |
| Switch / create scenes | `/scene <ID>` · `/scene new <name>` |
| Sync the log (tell the engine the latest changes) | `/sync` |
| Save / load (⚠ load overwrites current state — auto-backup `_before_`, rollback-able) | `/save [name]` · `/load <name>` |
| Reopen a scene | `/reset-scene [scene ID]` |
| Restart the whole world | `/reset` |
| Import a ready-made character card | `/import-card <card.png...>` |
| Director's monitor (see every engine decision) | `/loud` |
| Back to immersion mode | `/silent` |
| **Something feels off — audit the engine** | `/audit` |

> **Audit** (`/audit`): use it whenever something feels off — the engine checks world state and narrative against the six-stage checklists (Dramatist D / Storyliner S / Director R / Actor A / Continuity Keeper K / Writer W), item by item, outputting PASS/FAIL with evidence (file paths + field text), and follows the repair flow on failures. If audits keep finding the same class of violations (the engine repeatedly fails to follow its rules, patches don't help) — recommend switching to a different agent or LLM model instead of endlessly patching.

---

## Architecture: A Single-Context, Six-Stage Pipeline

WorldSim's core architecture is a single LLM within a single shared context — unlike the industry-common Multi-Agent architecture (multiple models colliding in high-cost, low-density "swarm chat"). It is not many models talking to each other; it is one engine executing six logical layers in sequence within the same context, sharing the same world knowledge and conversation history:

1. **The Dramatist** — conflict engine: scans pressure sources, registers / advances / escalates conflicts (CTs), manufactures deadlocks and irreversible costs — pressing characters onto the cliff's edge
2. **The Storyliner** — structure engine: story arcs, storylines, and beat sequences — weaving conflicts into fate, holding the macro course
3. **The Director** — live-direction engine: judges last turn's actual performance, controls pacing, continuation, and transitions of the current beat — detonating at the moment that matters most
4. **The Actor** — the life layer: NPCs decide and improvise autonomously from persona drives, inner intentions, action state, and environmental pressure — each owns a continuous timeline independent of the player; the player can enter or interrupt it, but is never its origin
5. **The Continuity Keeper** — fact engine: records what has actually happened into world state — long-session context stays drift-free
6. **The Writer** — narrative engine: turns what the user just lived through into prose — letting readers watch the jump from the cliff

Each of the seven state files has exactly one authoritative writer (Single Writer per State); the structure stages (①Dramatist / ②Storyliner) are conditionally skipped — they run only when the scheduler wakes them — while the live stages (③–⑥) run every turn. To keep per-turn cognitive load in check, **rules load at the point of use**: SKILL.md keeps only orchestration and constraints; the six phase rule files (`references/phase_*.md`) are read when their stage begins — read, decide, and generate stage by stage, never all at once. Stages are separated by **artifact handoff + script gates**: each stage produces its own write batch (first line `###STAGE:`) and must pass its own `gate <stage> --check` before the next stage begins; the Keeper closes each round with `round-check`; the Writer's narrative passes the W4 anchor check before output — output is the end of the turn.

**Dramatic craft instead of model stacking** — quality comes from the discipline of screenwriting, not from model count: low cost, results that exceed expectations.

---

## License

MIT License (Copyright © 2026 WorldSim.Life). Free to use, modify, and distribute, including commercially, provided the copyright notice is retained. See [`LICENSE`](LICENSE).

---

*Where Worlds Come to Life.*
