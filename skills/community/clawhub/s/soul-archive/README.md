# 🧬 Soul Archive

> *"Every conversation is a slice of the soul. Enough slices, and you can rebuild a complete you."*

[中文版](README_CN.md) · **English** · MIT License

---

A digital personality persistence system + agentic memory engine, working as a [Claude Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/getting-started) / WorkBuddy Skill / generic Python toolkit.

It builds a **digital soul clone** of you through everyday AI conversations, and at the same time gives the AI itself a **proactive long-term memory** so it can stop repeating the same mistakes.

![Soul Archive Header](docs/en/screenshot_header.png)

## Design Principles

- 🔒 **Local-first** — data lives in `~/.agent-commons/skills_data/soul-archive/`, never uploaded
- 📂 **Readable & editable** — plaintext JSON, open and edit anytime
- 🤖 **Active companion** — the AI extracts and recalls automatically as you chat
- 🎯 **Single-user simplicity** — one user, one machine, one soul

## What It Captures

| Axis | Captures |
|---|---|
| 👤 **Identity** | name / age / occupation / location / lifestyle / digital identity |
| 💫 **Personality** | MBTI / Big Five / traits / values / decision style |
| 🗣️ **Language** | catchphrases / sentence patterns / humor / filler words / analogies |
| 🧠 **Knowledge & Views** | topics, stances, belief frameworks (e.g. *first principles*) |
| 📝 **Memory** | episodic events + emotional triggers (12 emotions) |
| ⚙️ **Workflow** | tools / tech stack / hard rules / output preferences |
| 🎯 **Aspirations** | long-term goals / active projects / skills to learn / knowledge gaps |

The result is a **digital soul clone** that can act as you, plus a **persistent context layer** for any AI agent on your machine.

## Six Modes

| Mode | What it does | Trigger |
|---|---|---|
| 🔍 **Soul Extract** | Pull persona info from a conversation into the archive | "soul extract" / "灵魂沉淀" / auto on conversation end |
| 💬 **Soul Chat** | Build a role-play system prompt so the AI talks *as you* | "soul chat" / "灵魂对话" |
| 📊 **Soul Report** | Generate an interactive HTML personality portrait | "soul report" / "灵魂报告" |
| 🎯 **Soul Context Inject** | Output an ≤800-token persona summary for any agent's system prompt | session start |
| 🤖 **Agent Memory** | Recall related patterns / warn on failure-match / distill new patterns | task start |
| 🔄 **AI Self-Improvement** | Reflect, critique, learn from corrections | task completion / user correction |

## Quick Start

```bash
git clone https://github.com/dqsjqian/soul-archive.git
cd soul-archive

# 1. Initialize
python3 scripts/soul.py init

# 2. Check status
python3 scripts/soul.py status

# 3. Inject persona summary at session start
python3 scripts/soul.py context

# 4. Recall related patterns before a task
python3 scripts/soul.py recall --task "the thing I'm about to do"

# 5. Generate the HTML report
python3 scripts/soul.py report --output ~/soul-report.html
```

> **Requirements**: Python 3.10+, no third-party dependencies.

## Architecture

```
{SKILL_DIR}/                  ← Skill engine
<soul_dir>/  ← Your soul data (resolved by scripts/soul_paths.py — see SKILL.md)
```

The skill is the engine; the soul data lives in your home directory so any IDE / AI tool / workspace on the same machine can access the same soul.

```
<soul_dir>/
├── profile.json
├── config.json
├── identity/{basic_info,personality}.json
├── memory/
│   ├── episodic/YYYY-MM-DD.jsonl
│   ├── semantic/{topics,knowledge}.json
│   └── emotional/patterns.json
├── style/{language,communication}.json
├── workflow/preferences.json
├── aspirations.json
├── agent/{patterns.json,episodes/,corrections.jsonl,reflections.jsonl,distill_log.jsonl}
└── soul_changelog.jsonl
```

## Privacy

- Data lives in `~/.agent-commons/skills_data/soul-archive/`, plaintext JSON, **never uploaded**.
- The data directory has a `.gitignore` that blocks accidental commits.
- Soul Chat builds prompts locally; whether they're sent to an external LLM depends on **your** agent / platform.
- Sensitive topics (health / finance / intimate relationships) require explicit confirmation by default.
- Per-dimension toggles in `config.json` — turn off any axis you don't want.

For details see [PRIVACY.md](PRIVACY.md).

## Identity

![Identity](docs/en/screenshot_identity.png)

## Language Fingerprint

![Language](docs/en/screenshot_language.png)

## Topics & Beliefs

![Topics](docs/en/screenshot_topics.png)

## License

MIT — Soul Archive is yours, code and data alike.
