# Claude Code Quick Reference Card

## Start a New Project

```
I want to start a new project: [description]
Please follow the vibe-coding-blueprint methodology:
1. First design the system architecture, output to docs/ARCHITECTURE.md
2. Establish the fractal documentation structure
3. Then start writing code
```

## Add a New Feature

```
I want to add [feature] to [module].
Before writing code, please generate the technical plan (data model + interfaces + dependencies).
I will confirm before you implement.
```

## Debugging (Human in Command)

```
I'm encountering a problem: [describe symptom]
Expected vs actual: [comparison]
I've tried: [approaches already attempted]

Please analyze possible causes first. I'll tell you the root cause, then we'll fix it.
```

## Sync Docs After Update

```
Verification passed. Please sync:
1. Header comments in [filename] (if interfaces changed)
2. docs/[folder]/FOLDER.md
3. docs/ARCHITECTURE.md (if significant changes)
```

## Danger Signals — Stop and Flag

When these appear, tell Claude Code to stop and diagnose together:
- Same issue modified 3+ times without resolution
- Fixing one thing breaks another
- Code is getting messier

---

## Core Principles

1. **Plan first** → Never code before outputting the plan
2. **Small steps** → Break large modules into small verifiable tasks
3. **Documents as memory** → Sync docs immediately after each change
4. **Human in command** → Root cause stays with you; model handles execution
