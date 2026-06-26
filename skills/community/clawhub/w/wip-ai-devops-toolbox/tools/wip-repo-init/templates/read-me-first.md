# ai/ ... Read Me First

This is the working folder for the team. Plans, notes, ideas, dev updates, todos. Everything that isn't code lives here.

This folder only exists in `-private` repos. It never ships to public.

## Structure

```
ai/
  read-me-first.md                          <- you're here
  _sort/                                    <- stuff that hasn't been filed yet
  _trash/                                   <- stuff that's done or replaced (never delete, move here)
  dev-updates/                              <- one file per significant change, auto-detected by wip-release
    _trash/
  product/
    readme-first-product.md                 <- the product bible (read this before anything else)
    _trash/
    notes/                                  <- freeform notes, research, observations
      _trash/
    plans-prds/                             <- plans and PRDs with lifecycle stages
      roadmap.md                            <- prioritized roadmap (Upcoming / Done / Deprecated)
      _sort/                                <- plans that haven't been categorized yet
      _trash/
      upcoming/                             <- planned work (next up after current)
      current/                              <- active plans being implemented right now
      archive-complete/                     <- finished plans (moved here when done)
      todos/                                <- per-agent todo files
    product-ideas/                          <- ideas that aren't plans yet
      _trash/
```

## What's In Each Section

| Location | What It Is | Read More |
|----------|-----------|-----------|
| [_sort/](_sort/README.md) | Holding pen. Files that need to be looked at and filed somewhere. iCloud duplicates, randomly placed files, things you're not sure about. | [_sort/README.md](_sort/README.md) |
| [_trash/](_trash/README.md) | The archive. Files that are done, replaced, or consumed. Never delete anything, move it here. | [_trash/README.md](_trash/README.md) |
| [dev-updates/](dev-updates/README.md) | Engineering changelog. One file per significant change. Auto-detected by `wip-release` for release notes. | [dev-updates/README.md](dev-updates/README.md) |
| [product/readme-first-product.md](product/readme-first-product.md) | The product bible. What this product is, how it works, what's built, what's missing. Read before any plan, build, or PR. | [product/readme-first-product.md](product/readme-first-product.md) |
| [product/notes/](product/notes/README.md) | Freeform notes, research, observations. Anything useful that isn't a plan or idea. | [product/notes/README.md](product/notes/README.md) |
| [product/plans-prds/roadmap.md](product/plans-prds/roadmap.md) | Prioritized roadmap. Upcoming (ordered by priority), Done (with dates), Deprecated (with reasons). | [product/plans-prds/roadmap.md](product/plans-prds/roadmap.md) |
| [product/plans-prds/todos/](product/plans-prds/todos/README.md) | Per-agent todo files. One file per person/agent. Three sections: To Do, Done, Deprecated. | [product/plans-prds/todos/README.md](product/plans-prds/todos/README.md) |
| [product/product-ideas/](product/product-ideas/README.md) | Ideas that aren't plans yet. The incubator. Move to `plans-prds/upcoming/` when ready to commit. | [product/product-ideas/README.md](product/product-ideas/README.md) |

## Rules

**Never delete anything.** Move to `_trash/` in the nearest parent folder. Files in `_trash/` stay in git history and can always be recovered.

**`_sort/` is the holding pen.** When something doesn't have an obvious home yet, or iCloud duplicated something, put it in `_sort/`. File it properly when you know where it goes.

**`_trash/` is not garbage.** It's the archive. Completed plans go to `archive-complete/`. But notes, drafts, and superseded files go to `_trash/`. The difference: `archive-complete/` is work that shipped. `_trash/` is work that was replaced, abandoned, or consumed.

## How to Use This

**Starting a new feature?**
1. Write a plan in [product/plans-prds/current/](product/plans-prds/current/)
2. Write dev updates as you work in [dev-updates/](dev-updates/)
3. When the plan ships, move it to [archive-complete/](product/plans-prds/archive-complete/)

**Got an idea but not ready to plan?**
Put it in [product/product-ideas/](product/product-ideas/)

**Found something interesting but don't know where it goes?**
Put it in [_sort/](_sort/) or [product/notes/](product/notes/)

**Tracking work across agents?**
Use [product/plans-prds/todos/](product/plans-prds/todos/) (one file per person/agent) or GitHub Issues

## Dev Updates

Dev updates go in [dev-updates/](dev-updates/) with the naming convention:

```
YYYY-MM-DD--HH-MM--agent--description.md
```

Example: `2026-03-11--09-30--cc-mini--fix-hook-duplicates.md`

`wip-release` auto-detects today's dev updates and uses them as release notes. Write them as you work. They're the changelog that writes itself.
