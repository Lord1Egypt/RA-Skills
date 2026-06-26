# [Product Name] ... Read Me First

**Last updated:** YYYY-MM-DD
**Status:** Living document. Read this before any plan, build, or PR.

---

## What This File Is

This is the product bible for this repo. It answers: what is this thing, why does it exist, how does it work, and what's the current state. Every person and agent working on this repo reads this first.

**Keep it current.** Update it when the architecture changes, when major features ship, when the mental model shifts. If this file is stale, the team is working from bad context.

**Keep it honest.** Don't describe the aspirational version. Describe what's built and what's missing. Plans go in `plans-prds/`. This file is ground truth.

---

## This Folder

```
product/
  readme-first-product.md   <- you're here (the product bible)
  _trash/
  notes/                    <- freeform notes, research, observations
  plans-prds/               <- plans with lifecycle stages
    roadmap.md              <- the prioritized roadmap
    current/                <- plans being built right now
    upcoming/               <- plans that are next
    archive-complete/       <- plans that shipped
    todos/                  <- per-agent task lists
    _sort/                  <- plans that need categorizing
    _trash/
  product-ideas/            <- ideas that aren't plans yet
```

**Navigate:**
- **Want to know what's planned?** Read `plans-prds/roadmap.md`.
- **Want to know what's being built right now?** Look in `plans-prds/current/`.
- **Have an idea?** Write it up in `product-ideas/`.
- **Ready to turn an idea into a plan?** Move it from `product-ideas/` to `plans-prds/upcoming/` (or `current/` if starting now).

**Plan lifecycle:**
```
product-ideas/  ->  upcoming/  ->  current/  ->  archive-complete/
   (idea)          (planned)     (building)       (shipped)
```

---

## What [Product Name] Is

_One paragraph. What it does in human words. Not what it is technically. What problem it solves and for whom._

---

## Core Concepts

_The 3-5 mental models someone needs to understand this product. Not implementation details. The "aha" moments that make everything else make sense._

_Example: "Raw files are ground truth. Databases are indexes. If anything breaks, rebuild from raw files."_

_Example: "One agent per harness per machine. That's the identity unit."_

---

## How It Works

_The architecture at a level a new contributor can follow. Diagrams are fine. ASCII art is fine. The goal is: someone reads this section and can navigate the codebase without asking questions._

_Include:_
- _High-level data flow_
- _Key components and what they do_
- _Where state lives (databases, config files, etc.)_
- _What talks to what_

---

## Key Source Files

_Table of the important files and what they do. Not every file. The ones a new contributor needs to find their way._

| File | What It Does |
|------|-------------|
| `src/core.ts` | _description_ |
| `src/cli.ts` | _description_ |

---

## What's Built (as of vX.Y.Z)

_Bullet list of what actually works right now. Update the version and date when this section changes._

---

## What's Missing

_Bullet list of known gaps, limitations, and unfinished work. This is not the roadmap (that's in `plans-prds/roadmap.md`). This is the honest answer to "what doesn't work yet?"_

---

## Key Documents

_Links to the important plans, PRDs, and references. Relative paths within `ai/product/`._

| Document | Location |
|----------|----------|
| **This file** | `readme-first-product.md` |
| **Roadmap** | `plans-prds/roadmap.md` |

---

## Principles

_The non-negotiable rules for this product. The things that override convenience. 5-10 max._

1. _Principle one._
2. _Principle two._

---

## How to Update This File

- **New major feature shipped?** Update "What's Built" and "What's Missing."
- **Architecture changed?** Update "How It Works" and "Key Source Files."
- **New mental model?** Update "Core Concepts."
- **New principle?** Add to "Principles."
- **Always update** the "Last updated" date at the top.
- **Never delete sections.** If a section is empty, leave the heading. It reminds the team to fill it in.
