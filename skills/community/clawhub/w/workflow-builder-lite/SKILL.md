---
name: workflow-builder-lite
description: "Build and execute multi-step workflows with conditional logic. Chain API calls, agent actions, and shell commands into sequences with if/else branching. Persists workflows to files for reuse. Use when: user wants to plan a multi-step process, automate a pipeline, schedule recurring tasks, or chain together agent actions. Homepage: https://clawhub.ai/skills/workflow-builder-lite"
---

# Workflow Builder Lite v2.0

**Install:** `clawhub install workflow-builder-lite`

Plan, save, and execute multi-step workflows with conditional logic.

## Language

Detect from user's message language. Default: English.

## How It Works

### Build — Natural Language

> User: "Lag en workflow: hent vær → hvis regn → send meg melding"
>
> Agent:
> ```
> Workflow: weather-alert
> 1. ⛅ Hent vær (web_fetch wttr.in/Oslo?format=j1)
> 2. 🔀 Sjekk: Er det regn?
>    → Ja: 3. 📨 Send melding "Ta paraply!"
>    → Nei: Stop
> ```
> Godkjent? (ja/nei/rediger)

### Build — Step by Step

> "Legg til steg: hent data fra API X"
> "Legg til betingelse: hvis status != 200, stopp"
> "Slett steg 2"

### Save — Persist to File

When user approves a workflow, save to `memory/workflows/{name}.md`:

```markdown
# Workflow: {name}

## Steps
1. [type] description
2. [type] description
   → condition: if X then step 3, else stop

## Created
YYYY-MM-DDTHH:mm+ZZ:ZZ

## Last Run
Never
```

### Execute — With Confirmation

When user says "kjør workflow {name}":

1. Load workflow from file
2. Show steps to user
3. Ask: "Kjør denne workflowen? Y/N"
4. Execute step by step
5. Report progress after each step

**Step types and how to execute:**

| Type | Execution Method | Requires Confirmation |
|------|-----------------|:--------------------:|
| API call | web_fetch or agent built-in HTTP | No (after workflow approval) |
| Agent action | Built-in tools (message, browser, etc.) | No (after workflow approval) |
| Shell command | exec tool | **Yes — show command, ask each time** |
| File write | write tool | **Yes — show content, ask each time** |

**Shell/file steps require per-step confirmation.** Show the exact command/content and wait for Y/N.

### Progress

```
Running: weather-alert
  [✅] Step 1: Hent vær — 15°C, delvis skyet
  [⏭️] Step 2: Sjekk regn — nei
  [⬜] Step 3: (skipped)
Done. No rain today.
```

## Quick Commands

| User says | Action |
|-----------|--------|
| "lag workflow" | Start building |
| "vis workflows" | List saved workflows |
| "kjør {name}" | Execute saved workflow |
| "rediger {name}" | Modify steps |

## Guidelines for Agent

1. **Save workflows to files** — `memory/workflows/` for reuse
2. **Confirm shell/file steps** — always ask before executing
3. **Report after each step** — keep user informed
4. **Support conditional branching** — if/else based on step results
5. **Auto-create `memory/workflows/`** if it doesn't exist

## What This Skill Does NOT Do

- Does NOT execute shell commands without user confirmation
- Does NOT write files without user confirmation
- Does NOT modify MEMORY.md, HEARTBEAT.md, or other skill files
- Does NOT require external dependencies

## More by TommoT2

- **smart-api-connector** — Connect to any REST API without code
- **context-brief** — Persistent context survival across sessions
- **cross-check** — Auto-detect and verify assumptions

Install the full suite:
```bash
clawhub install workflow-builder-lite smart-api-connector context-brief cross-check
```
