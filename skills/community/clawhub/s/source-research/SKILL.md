---
name: source-research
description: "Build and maintain a reusable source-research system for discovering source pools, evaluating whether they are worth ongoing investment, defining efficient acquisition/filtering methods, recording rejection decisions, and producing high-quality source lists or notes. Use when the user mentions 信源, 信源池, 高质量信源, 信息源, 来源池, 作者池, account/blog/source curation, or wants a repeatable framework for finding and using high-quality information sources."
---

# Source Research Skill

Use this skill when the task is about:
- discovering or recording new source pools;
- deciding whether a pool is worth continued investment;
- defining how to acquire information from a pool efficiently;
- filtering pools into high-quality sources;
- standardizing how source-research artifacts are stored;
- leaving reusable artifacts so future agents do not repeat the same analysis.

## Core model

Treat source research as:
1. **Three result layers**: source pools / acquisition methods / filtered high-quality sources.
2. **Four execution stages**: record pool / research methods / produce source results / automate monitoring.

Important: the four stages are **not a strict sequence**. A pool may stay manual, may have results before methods are documented, or may be recorded now and researched later.

## Default operating rules

1. If you discover a new pool while doing another task, **record it immediately**.
2. If a pool was already evaluated and rejected, **preserve the rejection conclusion** so future agents do not waste time re-evaluating it.
3. If a pool is useful but not automated yet, **manual collection is allowed**; do not block on automation.
4. If a pool repeatedly proves valuable, **raise priority** for methodology, engineering, and automation.
5. Always try to leave at least one reusable artifact: pool update, method doc, result list, rejection note, or engineering design.

## Read these references

Read these files before doing non-trivial source-research work:
- `references/framework.md`
- `references/artifacts.md`
- `references/storage.md`
- `references/organization.md`

## Storage contract

This skill is not only about how to use the framework. It also standardizes how these things should be stored:
- source pool information;
- acquisition rules or programs;
- filtering rules or programs;
- high-quality source lists;
- high-quality information captured from those sources;
- rejection conclusions;
- information results and automation assets.

Follow the established pattern used by strong skills: keep the **methodology in the skill**, and keep the **workspace data in a dedicated directory**.

The canonical dedicated workspace directory for this skill is:
- `.source-research/`

If it does not exist yet, initialize it with:
- `python <skill-dir>/scripts/init_source_research.py [workspace-root]`

Canonical categories inside `.source-research/`:
- `source-pools/`
- `acquisition/`
- `filtering/`
- `high-quality-sources/`
- `high-quality-information/`
- `rejections/`
- `programs/`

Do **not** treat generic docs as the primary storage for these results. Generic docs may hold framework notes, but canonical source-research data should live in `.source-research/`.

## Minimal workflow

### A. New pool discovered
- Add or update a pool file under `.source-research/source-pools/`.
- Mark a status such as: observed / worth deeper research / has high-quality results / suitable for engineering / not worth investment.

### B. Existing pool revisited
- Check existing pool notes and rejection conclusions first.
- If it was previously rejected, only reopen when there is genuinely new evidence.

### C. Information needed now
- Manual collection is acceptable.
- If repeated manual work appears, record that this pool should move toward reusable acquisition/filtering methods.
- Store useful captured information under `.source-research/high-quality-information/` when it is worth preserving.

### D. Valuable pool confirmed
- Add or update:
  - acquisition method or program under `.source-research/acquisition/` or `.source-research/programs/`;
  - filtering method or program under `.source-research/filtering/` or `.source-research/programs/`;
  - high-quality source results under `.source-research/high-quality-sources/`;
  - engineering/automation design when justified.

## Storage standard

When using this skill, do not leave the outcome only in chat. Normalize storage according to artifact type:
- pool metadata and status -> `.source-research/source-pools/`;
- acquisition methods/programs -> `.source-research/acquisition/` or `.source-research/programs/`;
- filtering methods/programs -> `.source-research/filtering/` or `.source-research/programs/`;
- filtered high-quality source results -> `.source-research/high-quality-sources/`;
- high-quality information from those sources -> `.source-research/high-quality-information/`;
- rejection decisions -> `.source-research/rejections/`;
- engineering/automation work -> `.source-research/programs/`.

## Output standard

Do not end with only vague suggestions. Leave concrete artifacts in the workspace so another agent can continue from files rather than chat memory.
