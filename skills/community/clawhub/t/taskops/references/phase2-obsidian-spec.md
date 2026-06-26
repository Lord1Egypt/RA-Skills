# Phase 2 — Obsidian visualization and semantic testing

> Legacy phase note: this document describes the older JSON-canonical export model.
> Keep it for historical context, but do not read it as the canonical vNext contract.

## Purpose
Phase 2 turns the Phase 1 canonical graph state into a human-friendly Obsidian surface.

The goal is not to replace `graph.json`.
The goal is to project it into a note graph that is easy to inspect, click through, and pressure-test with a human in the loop.

## Validation question
Can a `graph-task` run be exported into an Obsidian-friendly markdown vault that:
- preserves Project / Step / Phase / Node relationships
- stays visually inspectable through wiki links and note boundaries
- helps a human review semantics without making Obsidian the source of truth
- remains simple enough to evolve before any round-trip editing or automation is introduced

## Canonical rule
Within this legacy phase, `graph.json` remains the canonical state.
Obsidian is a projection / inspection surface.

This is **not** the vNext default. The md-first direction in `references/md-first-vnext-spec.md` supersedes this as the main contract.

## Minimum Phase 2 deliverable
A first usable export path that writes an Obsidian-friendly vault with:
- one project note
- one step note per step
- one phase note per phase
- one node note per node
- wiki links that preserve containment and graph relationships
- enough status / result detail to support semantic inspection

## Current implementation boundary
The current Phase 2 baseline is **export only**.

Included now:
- markdown note generation
- note frontmatter for entity metadata
- wiki-link graph between Project / Step / Phase / Node notes
- result history rendered into node notes

Not included yet:
- round-trip editing from Obsidian back into `graph.json`
- semantic merge / conflict handling
- automatic closing of phases or steps
- custom Obsidian plugin behavior
- graph layout tuning or advanced visualization rules

## Why this boundary
This keeps the canonical state layer and the human inspection layer separate.
That matches the reset principles already chosen for `graph-task`.

## Likely next questions inside Phase 2
1. Is the exported note structure pleasant enough for real review?
2. Which entities need the richest note surfaces: Step, Phase, or Node?
3. Does semantic testing need writable review notes before true round-trip editing?
4. What is the smallest safe mutation loop, if any, from Obsidian back to `graph.json`?
