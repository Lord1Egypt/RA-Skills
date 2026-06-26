---
name: delegation
version: 1.0.0
description: Opus-level strategic decomposition for any opportunity, project, or task. Breaks work into atomic pieces with evals, assigns each to the cheapest capable model, and wires them into an executable pipeline. Use when starting anything new (opportunity, feature, project), when a task is too big to hand directly to a sub-agent, or when the user says "break this down", "figure out what to build", "analyze this opportunity". The THINK layer — Opus thinks, everything else works.
---

# Delegation — Think Once, Execute Cheap

> Opus is the brain. Everything else is hands.
> This skill is the translation layer between insight and execution.

## Core Principle

**Never use a $0.10/task model for $0.002/task work.**
**Never use a $0.002/task model for $0.10/task thinking.**

```
OPPORTUNITY ──► OPUS THINKS ──► ATOMIC TASK QUEUE ──► CHEAP MODELS EXECUTE ──► EVALS VERIFY ──► SHIP
                 (once)           (written artifact)     (sonnet/flash/gptoss)   (automated)
```

## Phase 0: VENTURE EVAL (new ideas only — skip for defined tasks)

When Ryan has a raw idea, before any decomposition, run the Venture Eval Protocol. This replaces VC due diligence with builder-optimized evaluation. **3 rounds max, then decide.**

### Round 1: Irrational Optimism (Flash — cheap, fast)

Prompt a cheap model to go MAXIMUM bullish. No skepticism allowed.

```
You are an irrationally optimistic founder evaluating this idea: {IDEA}

Assume everything goes right. Answer:
1. WHAT: one sentence
2. WHO PAYS: specific buyer (not "businesses" — name the persona)
3. WHY NOW: what changed in the world that makes this possible today
4. TAM: bottoms-up, not "1% of $X billion" — how many buyers × price
5. UNFAIR EDGE: what do we already have (infra, data, distribution, skills)
6. FIRST $1K: exact steps to the first thousand dollars in revenue
7. 10X SCENARIO: what does this look like if everything works for 2 years
8. EXISTING ASSETS: which of our products/pipelines/skills does this plug into
```

### Round 2: Brutal Fix (Sonnet — stronger reasoning)

Take Round 1's output and try to KILL it:

```
You are a ruthless VC partner reviewing this pitch: {ROUND_1_OUTPUT}

For each of the 8 points, either:
- CONFIRM: evidence supports it, cite why
- FIX: the claim is wrong but fixable — here's how
- KILL: this is fundamentally broken and unfixable — here's why

Then answer:
- BIGGEST RISK: the one thing that kills this
- CAN WE TEST IT FOR <$100?: yes/no + how
- COMPARABLE EXITS: 3 companies in adjacent space that sold/IPO'd
- VERDICT: BUILD / PARK / KILL (with one-sentence reason)
```

### Round 3: Questionnaire (only if Round 2 says BUILD)

If the idea survives, generate 5 questions that MUST be answered before committing resources:

```
Based on this evaluated idea: {ROUND_2_OUTPUT}

Generate exactly 5 questions where:
- Each question can be answered with data (not opinion)
- Each answer changes the build plan materially
- Each can be researched in <30 minutes
- Format: QUESTION | HOW TO ANSWER | WHAT CHANGES IF YES vs NO
```

Ryan answers the 5 questions → answers feed into Phase 1 decomposition.

### Token Budget for Venture Eval

| Round | Model | Est. Tokens | Cost |
|-------|-------|-------------|------|
| R1: Optimism | flash | ~1500 | $0.003 |
| R2: Fix | sonnet | ~2000 | $0.06 |
| R3: Questions | flash | ~800 | $0.002 |
| **Total** | | **~4300** | **$0.065** |

**If we can't resolve it in $0.07 of reasoning, the idea isn't clear enough.** Park it and revisit when more signal arrives.

### When NOT to Venture Eval

- Task is already defined (bug fix, feature request, maintenance)
- Ryan explicitly says what to build
- It's a client project with specs
- It's infrastructure/tooling work

## Phase 1: THINK (Opus only — ~500-2000 tokens output)

This is the ONLY phase that uses Opus. Everything after is delegated.

### 1a. Opportunity Frame (if Venture Eval was skipped)

Answer in ≤150 words:

```
WHAT: [one sentence — what is this]
WHO: [target customer — be specific, not "SMBs"]
WHY NOW: [timing signal — regulation, tech shift, market gap]
TAM: [total addressable market — even rough napkin math]
COMPETITORS: [top 3, their weakness]
OUR EDGE: [what we have that they don't — existing infra, distribution, data]
SLICE: [the specific wedge we'd enter with — not the whole market]
```

### 1b. Decompose into Atoms

Break the work into the **smallest independently testable units**.

Rules:
- Each atom has ONE clear output (a file, a URL, a data point, a yes/no answer)
- Each atom can be verified by a machine (not "looks good" — a command that returns pass/fail)
- Each atom takes <15 min for a sub-agent
- If an atom takes >15 min, it's not atomic — split again
- Dependencies are explicit (atom B needs atom A's output file)

Output format:

```markdown
| # | Atom | Output | Eval | Model | Depends | Est. |
|---|------|--------|------|-------|---------|------|
| 1 | Research competitor pricing | `research/pricing.md` | ≥3 competitors listed | flash | — | 3m |
| 2 | Scaffold Next.js app | `src/app/page.tsx` | `npm run build` exits 0 | sonnet | — | 5m |
```

### 1c. Model Assignment

```
Is it code generation?          → sonnet
Is it bulk/template/classify?   → flash
Is it batch of 20+?            → gptoss
Does it need >100K context?    → gemini-pro
Is it client-facing copy?      → opus (exception)
Is it a yes/no check?          → flash
```

**Default: flash.** Only upgrade when there's a reason.

### 1d. Eval Specification

Every atom gets a machine-verifiable eval:

| Eval Type | Example | Check |
|-----------|---------|-------|
| **File exists** | `research/pricing.md` | `test -f research/pricing.md` |
| **Build passes** | Next.js builds | `npm run build; echo $?` → 0 |
| **HTTP 200** | Site is live | `curl -so /dev/null -w "%{http_code}" [url]` → 200 |
| **Content check** | ≥3 competitors | `grep -c "^##" research/pricing.md` ≥ 3 |
| **Screenshot** | UI renders correctly | Browser screenshot + image model eval |

## Phase 2: PLAN (still Opus, just ordering — fast)

1. Topological sort by dependencies
2. Group into waves (parallel atoms)
3. Estimate total time = longest path through dependency graph
4. Estimate total cost = sum of (model cost × est. time)

Write full plan to `workspace/DELEGATION_PLAN.md`.

## Phase 3: EXECUTE (Opus hands off — never touches work again)

Hand `DELEGATION_PLAN.md` to orchestrator → spawner pipeline.

Opus's ONLY role during execution: monitor completion events, re-route on failure.

**Opus does NOT:** write code, generate content, run builds, do research queries.

## Phase 4: EVAL (automated)

After each atom: run eval command → pass/fail → retry with model escalation if needed.

```
fail → retry same model → upgrade model (flash→sonnet→opus) → mark failed
```

## Phase 5: LEARN (feeds auto-improve)

Append timing + pass/fail per atom to `.learnings/LEARNINGS.md`.

## Anti-patterns

- ❌ Opus writing code
- ❌ Subjective evals ("looks nice")
- ❌ Atoms bigger than 15 min
- ❌ Skipping the frame for new opportunities
- ❌ Re-thinking during execution (plan is locked after Phase 2)
- ❌ Spending >$0.07 reasoning about an unvalidated idea
- ❌ Using gptoss for <20 items
