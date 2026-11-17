# tech-to-skill

Convert technical long-form content into agent-callable skills that preserve actionable detail and trace back to source evidence.

**[中文文档](./README.zh.md)**

## Install

```bash
npx skills add LeoGoat2004/tech-to-skill
```

## Why this exists

Reading a great engineering article, paper, or project retrospective is one thing; being able to apply that knowledge weeks later in a real task is another. Most content stays inert after the first read. tech-to-skill bridges that gap by distilling technical content into structured skills an AI agent can load on demand.

The goal is practical: skills that an agent can actually use to solve a problem, not summaries that sound impressive but lack the detail to act on.

## What it does

Takes three types of technical content as input:

- **Engineering long-form** (source code notes, technical ebooks, architecture guides)
- **Papers and technical blog posts** (with method, algorithm, and experimental content)
- **Project development docs** (ADRs, retrospectives, postmortems, commit history)

For each, it produces skills with three core sections:

- **What** — the problem this skill solves, when to trigger it, when not to
- **How** — the method, at a granularity the agent can act on
- **Why** — the rationale from the source, including alternatives considered

Plus an **Evidence Index** that points to source material the agent can load for more detail when the skill's guidance isn't enough, and timestamps recording when the skill was created and verified.

## How to use

**Step 1: Tell your agent what you want to distill**

Examples:
- "Distill this article into skills: `<path-or-url>`"
- "Convert this paper into a skill: `<path-or-url>`"
- "Extract development experience from this project into skills: `<repo-path>`"

**Step 2: Provide the source**

- A file path (HTML, PDF, Markdown)
- A URL (web article, blog post)
- A directory or repo path (for project docs)

**Step 3: Specify an output directory**

Tell the agent where to write the generated skills. You choose; tech-to-skill does not auto-install.

**Step 4: Review the candidate list**

The agent will show you the candidate skills it plans to build and ask for confirmation. This is where you can add, remove, or merge candidates before construction begins.

**Step 5: Review the generated skills**

After construction, review the output. Each skill's `SKILL.md` is standalone. The `references/` subfolder holds source-evidence files the agent loads only when the skill's compressed guidance isn't enough.

## Design principles

- **Faithful to source.** Every claim traces back to the original material. If the source doesn't discuss something, the skill says so rather than fabricating.
- **Actionable detail.** The How section contains the specifics needed to act — API names, config fields, file paths, algorithm steps — not abstract methodology.
- **Evidence Index.** When a skill's compressed guidance isn't enough, the agent follows pointers to the original source material for the full context.
- **Real experience, not theory.** Project-doc skills capture what actually happened (postmortems, ADR consequences, retrospective outcomes), not generic best-practice lists.
- **Three input types, three W/H/W flavors.** Long-form extracts design tradeoffs. Papers extract research gaps and method insights. Project docs extract real stories and debugging lessons. The structure adapts to the source.

## License

MIT
