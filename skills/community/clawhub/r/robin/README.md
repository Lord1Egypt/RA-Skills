<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=250&color=gradient&text=Robin&section=header&desc=agent%20assisted%20digital%20commonplace%20book&descAlign=64&descAlignY=60&fontAlign=39&fontAlignY=41&reversal=false" width="100%"/>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/gniting/robin" alt="License"/></a>
  <a href="https://agentskills.io/"><img src="https://img.shields.io/badge/Skill-blue?label=AI" alt="ai skill" /></a>
</p>

---

# Robin

Robin is a skill for your AI agent to help you keep a digital commonplace book. When you share something worth remembering, your agent can use Robin to save it in a well-organized Robin library and bring it back later when it is useful.

> Dedicated to and named for [Robin Williams'](https://en.wikipedia.org/wiki/Robin_Williams) portrayal of Sean Maguire in [Good Will Hunting](https://en.wikipedia.org/wiki/Good_Will_Hunting) — a therapist who helped a brilliant but lost young man find his voice.

## What is a Commonplace Book?

A [commonplace book](https://ryanholiday.net/how-and-why-to-keep-a-commonplace-book/) is a personal collection of ideas, phrases, and passages worth keeping. Traditionally, it is a notebook where one gathers quotations, observations, arguments, anecdotes, and striking turns of phrase from what they read or hear, then organizes them so those pieces can be revisited and used later. 
One of its most practical benefits is that it sharpens vocabulary: by repeatedly noticing, recording, and returning to precise language, a reader begins to absorb better words, clearer sentence patterns, and more nuanced ways of expressing ideas. That expanded command of language tends to improve communication, because stronger vocabulary makes it easier to speak and write with accuracy, persuasion, and confidence. 
Over time, a commonplace book becomes more than a record of reading. It turns into a tool for better thinking, better communication, and, by extension, better work, relationships, and decision-making.

## Features

- Filing — Send Robin any content and it determines the right topic, files it away, and confirms
- Media-aware filing — Local images are copied into Robin, video URLs are stored but uploaded/local video files are rejected
- Topic management — Creates new topics on demand, suggests topic names, resolves conflicts
- Spaced repetition review — Surfaces items on a configurable schedule so you reinforce learning
- Rating — Rate surfaced items 1–5; Robin tracks what you care about most over time
- Searchable library — All entries live in plain markdown topic files; open in Obsidian, Logseq, or any editor
- Entry management — Move or delete entries by stable id while keeping review state in sync
- Health check — Diagnose config, topic files, media references, and review-index drift without changing data
- Agent-agnostic — Works with any agent that can read/write local files, run Python scripts, and pass CLI arguments or environment variables

## Before You Start

You need:

- an AI agent that can read/write local files and run Python scripts
- Python 3.11+
- a local folder in your agent workspace where Robin can store its files

Important: Robin requires Python 3.11 or newer. Older Python versions are not supported.

## Install Robin With Your Agent

The easiest path is to ask your agent to install Robin for you and choose a Robin state directory for this skill.

### Option 1 - Ask your agent directly

Just copy-paste this prompt to your agent:

```
Install the Robin skill from https://github.com/gniting/robin
```

### Option 2 - Via Skills.sh

If your agent platform supports `npx skills`, run:

```
npx skills add https://github.com/gniting/robin
```

then prompt your agent to set Robin up:

```
Set up the Robin skill
```

### Configuration

Your agent should handle Robin's setup and configuration automatically. As part of setup, your agent should create:

- `<agent workspace>/data/robin/topics/` for topic files
- `<agent workspace>/data/robin/media/` for copied images
- required `<agent workspace>/data/robin/robin-config.json` for Robin settings
- optionally `<agent workspace>/data/robin/robin-review-index.json` for review state

Your agent should pass Robin one of these every time it runs a Robin command:

- `--state-dir <agent-workspace>/data/robin`
- `ROBIN_STATE_DIR=<agent-workspace>/data/robin`

Typical host examples:

- Hermes: `~/.hermes/data/robin/`
- OpenClaw: `~/.openclaw/workspace/data/robin/`

By default, an agent can run Robin immediately through the repo-local Python scripts in `scripts/`. No `pip install -e .` or manual path setup is required. Installing the package to get the `robin-add`, `robin-doctor`, `robin-entries`, `robin-review`, and related entry points is optional.

After setup, your agent can run `python3 scripts/doctor.py --state-dir <state-dir> --json` for a read-only health check, or `python3 scripts/selftest.py` to verify Robin's doctor, entries, add, search, review, rate, duplicate, failure, and reindex paths in a temporary state directory without touching your real Robin library.

If your agent supports file indexing, it should index Robin's topic files like any other Markdown content. Use your agent's normal search for broad recall across your whole workspace.

## Use Robin Through Your Agent

Example prompts:

- `Save this quote using Robin.`
- `Use Robin to store this article under a good topic.`
- `Use Robin to save this image and include the author and context.`
- `Review my Robin items.`
- `Search what Robin has saved about clear thinking.`

Robin's own search is useful when your agent needs Robin-specific structure such as topic filters, tags, stable ids, ratings, and structured JSON output.

## Resurfacing items for reinforcement learning

As part of setup, your agent should ask you how often recall should happen and when you want it to run. Robin does not run a scheduler itself; your agent or host environment should trigger recall on that schedule, or keep active review available on demand if you prefer not to automate it.

Scheduled recall means Robin resurfaces an item for learning. It is not an active review session, and it should not ask you to reply with a bare 1-5 rating. Ratings are still supported in active review sessions; agents should use Robin's active-review mode only when they are in a live conversation and can intentionally collect and submit a rating.

## Need More Detail?

See [docs/guide.md](docs/guide.md) for the advanced guide, including:

- manual setup with `--state-dir` or `ROBIN_STATE_DIR`
- the difference between repo-local scripts and optional installed entry points
- file format and media rules
- storage layout and runtime behavior
- CLI usage and manual workflows
- review/index behavior
- selftest verification
- host-specific examples
- troubleshooting and compatibility notes

## License

MIT — see [LICENSE](LICENSE)
