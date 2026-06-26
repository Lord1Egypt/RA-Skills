# Skill Router

> Automatically route Claude to the right specialized skill — with a usage report at the end of every answer.

---

## What It Does

Every Claude user has a different set of skills installed (from [anthropics/skills](https://github.com/anthropics/skills) or elsewhere). The problem: Claude doesn't always use them on its own.

Skill Router solves three problems:

1. **Index** — Lists all your skills so Claude knows what's available
2. **Route** — Auto-matches your question to the right skill
3. **Audit** — Reports which skills were used at the end of every answer

```
User Question → Skill Router matches skills → Skills loaded → Answer delivered → Usage report
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/skill-router.git
cd skill-router
```

### 2. Auto-generate index

```bash
python scripts/generate.py
```

This scans your local `~/.claude/skills/` directory, reads each skill's name and description, auto-categorizes them, and generates a complete skill index table.

### 3. Install

```bash
# Linux / macOS
cp SKILL.md ~/.claude/skills/skill-router/SKILL.md

# Windows
xcopy SKILL.md "%USERPROFILE%\.claude\skills\skill-router\SKILL.md*" /Y
```

### 4. Verify

Open Claude, ask any question — you should see a skill usage report at the end of the reply.

---

## How It Works

```
                   ┌──────────────────────────┐
                   │  Your skills directory    │
                   │  ~/.claude/skills/        │
                   │  ├── golang-patterns/     │
                   │  ├── frontend-design/     │
                   │  ├── deep-research/       │
                   │  └── ... (N skills)       │
                   └──────────┬───────────────┘
                              │
                   ┌──────────▼───────────────┐
                   │  generate.py              │
                   │  - Reads each SKILL.md    │
                   │  - Extracts name + desc   │
                   │  - Auto-categorizes       │
                   └──────────┬───────────────┘
                              │
                   ┌──────────▼───────────────┐
                   │  skill-router/SKILL.md    │
                   │  ├── Skill index table    │
                   │  ├── Routing rules        │
                   │  └── Reporting directive  │
                   └──────────────────────────┘
```

`generate.py` reads YOUR local skills, so the generated index only contains what YOU have installed. Everyone's Skill Router is unique.

### Auto-categorization

Skills are categorized by keyword matching against name + description:

| Category | Keywords |
|------|---------------|
| Architecture | architect, blueprint, hexagonal |
| Code Quality | code review, onboarding, refactor |
| Git & Version Control | git, github, commit, branch |
| API & Backend | api, rest, backend, middleware |
| Database | database, sql, migration, orm |
| DevOps & Deploy | docker, deploy, ci/cd, pipeline |
| Testing | test, e2e, playwright, benchmark |
| Frontend | react, vue, ui, css, accessibility |
| Mobile | android, ios, flutter, mobile |
| Language-specific | golang, java, python, rust, cpp |
| AI / Agent | agent, llm, rag, prompt, eval |
| Content | writing, blog, article, content |
| Research | research, scraper, crawl |
| Security | security, hipaa, compliance |
| System Tools | context, token, optimization |

Unmatched skills go into "Other".

---

## Usage

### Update after adding new skills

```bash
cd skill-router
python scripts/generate.py
# Then re-copy to skills directory
```

### Custom skills directory

```bash
python scripts/generate.py --skills-dir /path/to/your/.claude/skills
```

### Custom output path

```bash
python scripts/generate.py --output ~/custom-router/SKILL.md
```

### Manual index maintenance

If you prefer not to use the generator, just edit the content between `<!-- SKILL_INDEX_START -->` and `<!-- SKILL_INDEX_END -->` in SKILL.md directly. Any format works.

---

## Usage Report

After every answer, you'll see at the end:

```
---
**Skill Usage Report：**
- golang-patterns — Loaded — User mentioned Go concurrency
- coding-standards — Loaded — Code review context
- deep-research — Not triggered — Matched but not needed
```

Now you'll know: which skills are actually working, and which are collecting dust?

---

## Design Philosophy

| You | Skill Router |
|----------|--------------------------|
| Decide which skills to install | Auto-discovers what you've installed |
| Decide how to organize skills | Auto-categorizes by keyword |
| Decide whether to use a skill | Routes questions to the right skill |
| Want to know which skills were used | Reports after every answer |

You just **install and maintain skills**. Indexing, matching, and reporting is fully automatic.

---

## License

MIT