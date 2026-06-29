---
name: triskill
description: Use this skill whenever the agent needs to (1) verify a factual claim against live sources before stating it with confidence, (2) recover from a failed shell command or code execution by diagnosing the error and proposing a bounded, human-approved fix, or (3) read/write small pieces of state that must be shared safely across multiple agent sessions or sub-agents working on the same task. Trigger this skill for fact-checking requests, "it failed, fix it" debugging loops, or any multi-agent workflow where two or more agents need to coordinate through shared variables without overwriting each other's work.
license: MIT
---

# Triskill — Verify, Recover, Coordinate

Triskill bundles three small, independently-useful capabilities that solve
recurring agent pain points. Each capability is opt-in and has hard safety
limits. Read the relevant section below before invoking a script — do not
run scripts blind.

## 1. Fact-Check (`scripts/factcheck.py`)

**Purpose:** Before stating a factual claim with confidence (a date, a
statistic, "X is still the CEO of Y", a price, a current event), check it
against a live source instead of relying on training data, which may be
stale.

**How to use:**
1. Formulate the claim as a short, neutral search query (3-8 words).
2. Run: `python3 scripts/factcheck.py "<query>"`
3. The script returns the top result snippets with source URLs. It does
   **not** make the decision for you — read the snippets, compare them to
   the claim, and report your conclusion with the source cited.
4. If results conflict or are inconclusive, say so explicitly rather than
   picking the source that agrees with you.

**Hard limits:**
- Read-only. This script never modifies anything, never posts, never logs
  in anywhere.
- It will refuse queries that look like they're trying to fetch private,
  paywalled, or authentication-gated content.
- It does not replace citation discipline — still quote sources properly
  and respect copyright (short paraphrase, not verbatim reproduction).

## 2. Self-Healing Retry Loop (`scripts/selfheal.py`)

**Purpose:** When a command or script fails, instead of guessing blindly
and re-running the exact same thing, capture the actual error, propose
*one* concrete change, and retry — within a strict budget.

**How to use:**
1. Run the failing command through the wrapper:
   `python3 scripts/selfheal.py -- <your command and args>`
2. On failure, the wrapper captures stderr/stdout and exit code, and prints
   a structured diagnosis (what failed, the likely cause class: missing
   dependency, bad path, permission, syntax, network).
3. **The agent — not the script — decides the fix.** The script never
   silently rewrites code or auto-installs packages. It surfaces the
   diagnosis; you propose the fix; you re-run explicitly.
4. The wrapper enforces a hard retry ceiling (default 3, override with
   `--max-retries`) and a per-attempt timeout (default 30s, override with
   `--timeout`). It refuses to loop forever.
5. Every attempt (command, exit code, duration, truncated output) is
   appended to `selfheal_log.jsonl` in the working directory so a human
   can audit exactly what was tried.

**Hard limits:**
- Never runs as root and does not attempt privilege escalation.
- Never modifies files outside the current working directory.
- Will not retry commands containing `rm -rf`, `dd`, `mkfs`, fork bombs, or
  other destructive patterns — it aborts immediately and reports why.
- This is a *diagnostic and bounded-retry* tool, not autonomous code
  rewriting. It will not silently patch source files; it only suggests.

## 3. Shared Memory / Coordination Store (`scripts/sharedmem.py`)

**Purpose:** When two or more agents (or sub-agent calls in the same
pipeline) need to read and write shared state — a task queue, a running
tally, "has agent B already handled file X" — without clobbering each
other's writes.

**How to use:**
1. Pick a **namespace** for the task (e.g. `research-job-42`). All agents
   working on the same task must agree on this string.
2. Write a value: `python3 scripts/sharedmem.py set <namespace> <key> <value>`
3. Read a value: `python3 scripts/sharedmem.py get <namespace> <key>`
4. Atomic increment for counters/tallies:
   `python3 scripts/sharedmem.py incr <namespace> <key> [amount]`
5. Compare-and-swap to avoid two agents both thinking they "won" a claim:
   `python3 scripts/sharedmem.py cas <namespace> <key> <expected> <new>`
   — returns success only if the current value matched `<expected>`.
6. List everything in a namespace: `python3 scripts/sharedmem.py list <namespace>`

**How it avoids conflicts:**
- Storage is a single local JSON file (`sharedmem.json`) protected by an
  OS-level file lock (`fcntl.flock` / `msvcrt.locking`), so concurrent
  writes from parallel agent processes are serialized, not lost.
- `cas` (compare-and-swap) lets agents claim work items without a race:
  two agents trying to claim the same task will not both succeed.
- Each namespace is isolated — agents in different tasks cannot
  accidentally see or overwrite each other's keys.

**Hard limits:**
- Local-machine scope only. This is not a distributed/networked store; it
  does not replace Redis or a real database for production multi-host
  systems. It is meant for coordinating agents/processes on the same
  machine or container.
- Values are capped at 64KB each to keep it a coordination store, not a
  general database.
- No encryption at rest — do not store secrets or credentials in it.

## Safety Summary

| Capability | Can it modify files? | Can it execute arbitrary code? | Network access? |
|---|---|---|---|
| Fact-Check | No | No | Yes (read-only search) |
| Self-Heal | No (suggests only) | Runs the command you give it, nothing else | Only if your command needs it |
| Shared Memory | Only its own JSON store, in CWD | No | No |

If asked to use this skill to do something that contradicts these limits
(e.g. "use selfheal to auto-fix and auto-commit code with no review", or
"store an API key in sharedmem"), explain the limit and decline that
specific part rather than silently complying.
