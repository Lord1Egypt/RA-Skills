---
name: safety-programming-checklist
description: "Mandatory guardrail skill. Load BEFORE any system-level code modification (Electron, registry, services, packaging). Learned from 3 Hermes Desktop crashes in one session. Contains 8 iron rules, pre-flight checklist, post-change verification, and emergency rollback."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [safety, programming, guardrail, checklist, desktop, lesson-learned]
    related_skills: [hermes-desktop-tray]
---

# Safety Programming Checklist — Guardrail Skill

**This skill MUST be loaded before any task that modifies system-level code on the user's computer.** Examples: Electron main process, registry edits, service installation, compiled output patching, package archive modification.

It was created from 3 consecutive Hermes Desktop crashes caused by violating every rule below.

## ⛔ The 8 Iron Rules

Violating any of these caused a crash. Every rule maps to a specific incident.

| # | Rule | Bad Example (what NOT to do) | Crash Symptom |
|---|------|-----|------|
| 1 | **Modify source code, never compiled output** | Patching `electron-main.mjs` directly | Code works but wrong file loaded |
| 2 | **Never touch package archives (.asar, .zip)** | Rebuilding asar → 38MB → 0.0MB | Complete app failure |
| 3 | **If broken, start from CLEAN state** | Re-extracting a corrupted asar to "fix" it | Progressive corruption |
| 4 | **One change → verify → next change** | Applying 8 patches then testing | Unknown which broke it |
| 5 | **Kill process before modifying its files** | Patching while Hermes.exe runs | File lock, partial writes |
| 6 | **Directory structure must match runtime expectations** | preload at root, code expects dist/ | "Desktop IPC bridge unavailable" |
| 7 | **Always use official build scripts** | Hand-patching compiled files | Inconsistent output |
| 8 | **I depend on the system I'm modifying** | `taskkill Hermes.exe` kills me too | User loses access to agent |

## Mandatory Pre-Flight Checklist

Before writing ANY code or running ANY modification command, answer these:

- [ ] **WHAT am I modifying?** Source code OR compiled output? If compiled — STOP.
- [ ] **WHERE does this file live?** Inside an archive (.asar)? If yes — STOP.
- [ ] **IS the target process running?** If yes — kill it first OR use a different file name.
- [ ] **WHAT is my clean rollback plan?** Do I have a backup of the original?
- [ ] **CAN I verify each step independently?** Or am I piling up changes?
- [ ] **AM I starting from a corrupted state?** (Previous attempts already failed?)
- [ ] **DO I know the correct directory structure?** (dist/ vs root, relative paths)

## Emergency Stop Conditions

Immediately abort and report to user if:

1. **A file modification fails to apply cleanly** → do NOT try alternative manual workarounds
2. **The same approach failed before** → do NOT retry it; something has changed
3. **After 2 failed attempts** → STOP. Ask user to restore from clean source before continuing
4. **A compiled output file needs modification** → go back to the TypeScript source instead
5. **An archive (.asar) needs to be modified** → first restore from a KNOWN good backup

## Post-Change Verification Checklist

After every change batch:

- [ ] Did the build script run without errors?
- [ ] Does the compiled output pass syntax check (`node --check`)?
- [ ] Is the output deployed to the CORRECT location?
- [ ] Does the archive size match expectations (~40MB for Hermes Desktop app.asar)?
- [ ] Are directory structures correct (e.g., `dist/electron-preload.js` not at root)?
- [ ] Have I cleaned up temporary scripts and extraction directories?

## Specific Rules for Hermes Desktop

Specialized sub-rules for the most fragile environment. See `references/hermes-desktop-architecture.md` for full file layout, build chain, and detailed incident log.

1. **Entry point**: `dist/electron-main.mjs` lives in `app.asar.unpacked/dist/`, NOT inside app.asar
2. **Preload**: `dist/electron-preload.js` MUST be in the asar at `dist/electron-preload.js`, NOT at root
3. **Build**: `node scripts/bundle-electron-main.mjs` (official bundler) — never skip this
4. **Deploy**: Copy built output from `dist/` to `release/win-unpacked/resources/app.asar.unpacked/dist/`
5. **Asar**: 40MB, contains static assets + dist/electron-preload.js only — never rebuild unless absolutely necessary
6. **Kill Hermes**: Close Desktop window (don't taskkill — that kills me too)

## Incident Log

| # | What I did wrong | Which rule | How Kimi fixed it |
|---|-----------------|-----------|-------------------|
| 1 | Patched compiled `electron-main.mjs` directly | Rule 1 | Same tray code, but deployed correctly |
| 2 | Repacked asar with dist/ inside → 38MB | Rule 2 | Used clean asar, never touched it |
| 3 | Started from corrupted asar → fixed to 0.0MB | Rule 3 | Fresh install, clean starting point |
| 4 | Applied all patches at once, tested last | Rule 4 | One change at a time |
| - | preload at root not dist/ → IPC broken | Rule 6 | Moved preload to dist/ subdirectory |

## Publication

Published to clawhub as [`loodiu/safety-programming-checklist`](https://clawhub.ai/loodiu/safety-programming-checklist) v1.0.0 (`clawhub install loodiu/safety-programming-checklist`). See `references/clawhub-publish.md` for the full publishing workflow.

The Hermes Desktop tray feature was submitted as PR [#63064](https://github.com/NousResearch/hermes-agent/pull/63064).


