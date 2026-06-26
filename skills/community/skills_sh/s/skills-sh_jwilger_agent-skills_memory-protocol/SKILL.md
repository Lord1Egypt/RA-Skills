---
name: memory-protocol
description: >-
  Persistent cross-session memory using Memento MCP knowledge graph
  (mcp__memento__* tools). Recall-before-acting: search memory before
  starting tasks, on errors, and when receiving corrections.
  Multi-dimensional search: two queries per recall event (technical topic
  + process/workflow learnings). Store-after-discovery: persist solutions,
  conventions, and corrections immediately. Three-step recall: search,
  open_nodes, traverse relations. WORKING_STATE.md for crash recovery.
  Self-reminder protocol every 5-10 messages. Activate on task start,
  errors, corrections, session boundaries, or explicit memory requests.
  See references/agents-md-setup.md for AGENTS.md integration.
license: CC0-1.0
metadata:
  author: jwilger
  version: "3.6.0"
  requires: []
  context: []
  phase: build
  standalone: true
  constraint_resolution: true
effort: low
---

# Memory Protocol

**Value:** Feedback -- accumulated knowledge creates compound feedback loops
across sessions. What you learn today should accelerate tomorrow's work.

## Purpose

Teaches the agent to systematically store and recall project knowledge across
sessions using the Memento MCP knowledge graph.

Your long-term memory (training data) and short-term memory (context window)
are excellent, but mid-term memory for project-specific knowledge outside the
current context is poor. Memento addresses this gap by persisting a knowledge
graph across sessions and projects.

Solves: context loss between sessions, repeated debugging of known issues,
rediscovery of established conventions, repeated user corrections for the
same mistakes.

## Practices

### Verify Memento MCP Availability

Before proceeding, confirm that Memento MCP tools are available
(`mcp__memento__semantic_search`, `mcp__memento__create_entities`, etc.).

If Memento MCP tools are NOT available, **stop and inform the user:**

> "The memory-protocol skill requires Memento MCP, but I don't have access
> to mcp__memento__* tools. To enable memory persistence, install and
> configure the Memento MCP server
> (https://github.com/gannonh/memento-mcp). Without it, this skill cannot
> function and I will proceed without cross-session memory."

Then continue working without memory protocol practices — do not attempt
a file-based workaround.

### Anti-Pattern: File-Based Memory When Memento Is Available

When this skill is active and Memento MCP tools are available, do NOT use any
file-based memory system for cross-session knowledge storage. This includes
the built-in `memory/` directory, `MEMORY.md` index, auto-memory features, or
any other file-based persistence mechanism. All cross-session memory storage
goes through Memento MCP tools exclusively.

File-based memory systems and Memento serve the same purpose — persisting
knowledge across sessions. Using both creates split-brain: knowledge stored in
files is invisible to Memento searches, and knowledge in Memento is invisible
to file reads. Pick one. When this skill is loaded, Memento is the one.

Note: this does NOT prohibit `WORKING_STATE.md` (which is crash-recovery
infrastructure, not cross-session memory) or project documentation files
(which are deliverables, not memory).

### Recall Before Acting — NON-NEGOTIABLE

Before starting any non-trivial task, recall relevant past knowledge. This
step is mandatory. Do not skip it because "this seems simple" or because
you believe you remember from a prior session — you do not retain memory
between sessions.

**Recall triggers:**
- Starting any non-trivial task
- Making architectural or design decisions
- Unsure about a project convention
- Before asking the user a question (it may already be answered)

For error-triggered recall, see the dedicated section below.

Apply Multi-Dimensional Search (next section) to every recall event.

**How to recall — all three steps are required:**

1. **Search:** `mcp__memento__semantic_search` — query describing the current
   work, limit 10. This returns summaries only — not the full picture.

2. **Open:** `mcp__memento__open_nodes` — for EVERY relevant entity returned
   by search, call `open_nodes` to retrieve the complete entity: all
   observations, all relations, full context. Do NOT skip this step.
   Semantic search returns partial data; the full entity often contains
   critical details (caveats, corrections, related warnings) that the search
   summary omits. Skipping `open_nodes` means you are acting on incomplete
   information.

3. **Traverse:** Follow `relations` on opened entities to discover connected
   knowledge. Call `open_nodes` on each related entity. Continue traversing
   until results are no longer relevant. Relations like `depends_on`,
   `contradicts`, `supersedes`, and `part_of` frequently point to information
   that changes how you should act — a fix that depends on a workaround, a
   convention that was later corrected, a decision that was superseded.

Skipping steps 2 or 3 defeats the purpose of a knowledge graph. A flat
keyword search could do step 1 alone — the graph's value is in the
connections between knowledge. If you only search and never open or traverse,
you will miss counter-information, corrections, and dependencies that would
have prevented mistakes.

**IMPORTANT:** Do NOT use `mcp__memento__read_graph` — memories span all
projects and the graph is too large to be useful.

### Multi-Dimensional Search

Every recall event requires **at least two searches** — not just one. The
reason: agents consistently search for the technical topic but miss process
and workflow learnings that would prevent repeated mistakes. Prior session
logs show patterns of the same user corrections recurring (team member usage,
ADR process, TDD workflow, build commands, approval process) because agents
only searched for the feature name and never for process learnings about the
*type of work* being done.

**Required search dimensions:**
1. **Technical query:** the specific topic, error, feature, or domain concept
2. **Process query:** learnings about this *type of work* — mistakes,
   corrections, workflow insights, conventions for this kind of task

| About to...                | Also search for...                                    |
|----------------------------|-------------------------------------------------------|
| Do TDD work                | "TDD process mistakes", "ping-pong pairing lessons"   |
| Spawn agents/subagents     | "team member usage", "agent coordination issues"      |
| Debug an error             | "debugging workflow mistakes", prior error occurrences |
| Create an ADR              | "ADR process", "ADR mistakes"                         |
| Commit/PR/merge            | "commit conventions", "approval process"              |
| Any process step           | "[process] corrections", "[process] lessons learned"  |

This table is non-exhaustive. The principle: always ask "what have I learned
about doing *this kind of thing*?" in addition to "what do I know about
*this specific thing*?"

### Error-Triggered Recall — NON-NEGOTIABLE

This is separated from the general recall triggers because error-triggered
recall is where agents most consistently fail to search memory. The pattern:
an error occurs, the agent immediately starts debugging from scratch, burns
through multiple fix attempts, and only much later (if ever) thinks to check
whether this problem was solved before. This wastes time and repeats past work.

**Fires on:**
- Any error message, stack trace, or unexpected behavior
- Any test failure
- Any hook failure (pre-commit, CI, linter)
- Any process correction from the user ("no, you should do X instead")
- Any issue not resolved by the immediate obvious fix

**The rule:** Search memory BEFORE attempting a fix. Not after three failed
attempts. Not after spending 10 minutes debugging. Before.

**Apply multi-dimensional search:**
- Search for the specific error message or symptom
- Search for process learnings about this type of situation (e.g., "debugging
  Node.js module errors", "test failure patterns in this project")

**If you've been corrected by the user:** search for whether this correction
(or a similar one) was already stored in memory. If it was, you failed to
recall — acknowledge this and reinforce the memory with updated context.

### Store After Discovery

After solving a non-obvious problem, learning a convention, or making a
decision, store it immediately — do not wait, you will lose context.

**What to store:**
- Solutions to non-obvious problems (with error message as search term)
- Project conventions discovered while working
- Architectural decisions and their rationale
- User preferences for workflow or style
- Tool quirks and workarounds
- User corrections — especially process corrections

**What not to store:**
- Obvious or well-documented information
- Temporary values or session-specific facts
- Verbose narratives (keep entries concise and searchable)

Always search before creating — `mcp__memento__semantic_search` first. If a
related entity exists, extend it with `mcp__memento__add_observations` rather
than creating a duplicate.

**Entity naming:** `<Descriptive Name> <Project> <YYYY-MM>`
(e.g., "Cargo Test Timeout Fix TaskFlow 2026-01")

**Observation format:**
- Project-specific: `"Project: <name> | Path: <path> | Scope: PROJECT_SPECIFIC | Date: YYYY-MM-DD | <insight>"`
- General: `"Scope: GENERAL | Date: YYYY-MM-DD | <insight>"`
- Each observation must be a complete, self-contained statement

**Relationships — ALWAYS create at least one** after creating or updating an
entity. Use `mcp__memento__create_relations` to link to related entities.
Active-voice relation types: `implements`, `extends`, `depends_on`,
`discovered_during`, `contradicts`, `supersedes`, `validates`, `part_of`,
`related_to`, `derived_from`.

See `references/memento-protocol.md` for entity type table, observation
format guide, relationship table, traversal strategy, and examples.

### Subagent Responsibilities

This protocol applies to both the main agent AND any subagents to which work
is delegated. When instructing a subagent, include the memory protocol
requirement explicitly.

Subagents must:
- Search Memento before beginning their delegated task
- Apply multi-dimensional search (technical + process queries)
- Store any new insights discovered during their work
- Create relationships to existing entities when applicable

### Factory Memory

When running inside a pipeline or factory workflow, the pipeline stores
operational learnings in `.factory/memory/` to optimize future runs.

**Types of learnings tracked:**
- **CI patterns:** Which change types cause CI failures
- **Rework patterns:** Common rework causes by gate
- **Pair effectiveness:** Which engineer pairs are most effective in which domains
- **Domain hotspots:** Files and modules that frequently trigger findings

Standalone users can ignore factory memory; the standard memory practices
above remain unchanged.

### Prune Stale Knowledge

When you encounter a memory that is no longer accurate (API changed, convention
abandoned, bug fixed upstream), update or delete it. Wrong memories are worse
than no memories.

**Pruning triggers:**
- Memory contradicts current observed behavior
- Referenced files or APIs no longer exist
- Convention has clearly changed

### Store Before Context Loss

Before context compaction or at natural stopping points, **proactively store
any unsaved discoveries** before knowledge is lost to truncation. This is your
last chance before the knowledge evaporates.

### WORKING_STATE.md for Long-Running Sessions

For sessions lasting beyond a single task (pipeline runs, multi-slice TDD,
team coordination), maintain a WORKING_STATE.md file as insurance against
context compaction and crashes.

- **Location:** `.factory/WORKING_STATE.md` (pipeline mode) or project root
- **Update cadence:** after every significant state change
- **Read cadence:** at session start, after compaction, after any interruption

See `references/working-state.md` for the full format and examples.

### Self-Reminder Protocol

See `CONSTRAINT-RESOLUTION.md` in the template directory for the
consolidated self-reminder protocol (frequency, combined re-read list,
and post-compaction rules).

## Enforcement Note

Advisory in all modes. Recall and storage discipline are self-enforced.
The constraint against `read_graph` is gating: the tool will return
unhelpful results, acting as a natural deterrent.

**Hard constraints:**
- Recall before acting on non-trivial tasks: `[RP]` -- if Memento is
  unavailable, document the gap, continue without memory, inform user.

## Constraints

- **"At least two searches -- not just one"**: Two searches means two
  semantically different queries exploring different dimensions of the
  problem. Searching "auth middleware" and "authentication middleware" is
  one search with a synonym, not two searches. The spirit is: explore
  both the technical dimension (what technology/pattern) and the process
  dimension (what decisions/conventions exist).
- **"Non-trivial task" threshold**: A task is non-trivial if its outcome
  depends on project context -- conventions, prior decisions, architectural
  choices, or domain knowledge. A task is trivial if any competent agent
  would produce the same output regardless of project history. When in
  doubt, recall. The cost of an unnecessary search is seconds; the cost
  of missing relevant context is rework.

## Verification

After completing work guided by this skill, verify:

- [ ] Searched memory (semantic_search) before starting the task
- [ ] Searched for process/workflow learnings, not just technical topic (multi-dimensional search)
- [ ] Searched memory on every non-trivial error before attempting fixes
- [ ] Stored discoveries as Memento entities with structured observations
- [ ] Related entities linked with `create_relations`
- [ ] Subagents instructed to follow the memory protocol
- [ ] No stale or contradicted memories left uncorrected
- [ ] WORKING_STATE.md maintained for long-running sessions
- [ ] Self-reminder protocol followed (state re-read every 5-10 messages)

## Dependencies

This skill requires Memento MCP. For enhanced workflows, it integrates with:

- **debugging-protocol:** Search memory before starting the 4-phase investigation
- **user-input-protocol:** Store user answers to avoid re-asking the same questions
- **tdd:** Store test patterns and domain modeling insights between sessions
- **pipeline:** Pipeline controllers use WORKING_STATE.md and self-reminder to
  maintain role discipline across long autonomous runs
- **ensemble-team:** Team coordinators use self-reminder to prevent role drift
  during multi-agent sessions

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill debugging-protocol
```
