# Skill Intake Protocol

Use this when a new skill is installed, discovered, updated, or manually added to a workspace that already uses Shared Memory OS.

## Goal
Decide whether the incoming skill:
- is irrelevant to memory governance
- can safely coexist
- needs a shared-memory note
- conflicts with the workspace memory model

## Intake flow

### 1. Read the candidate skill header
Check:
- `name`
- `description`
- whether it mentions memory, notes, learning, reflection, heartbeat, habits, project tracking, workflow steering, or long-term storage

### 2. Classify

#### Class A — unrelated
Examples:
- React
- GitHub CLI helpers
- browser automation
- web search

Action:
- no shared-memory changes required

#### Class B — adjacent but compatible
Examples:
- summarize
- skill discovery
- workflow helpers
- self-improvement helpers that do not insist on isolated storage

Action:
- add or maintain a short note that the skill should respect the workspace shared-memory model

#### Class C — conflicting or likely to fragment memory
Signals:
- defines its own long-term memory hierarchy
- insists on writing outside workspace memory without override behavior
- defines competing heartbeat or maintenance rules
- encourages always-on logging without routing discipline
- would create duplicate project or preference stores

Action:
- do not blindly merge
- log the conflict candidate
- adapt only after explicit review

### 3. Record the outcome
Use the smallest useful place:
- stable rule → shared-memory skill references or workspace docs
- one-time review note → `memory/corrections.md` or daily
- active unresolved conflict → project file or intake backlog

### 4. Only then integrate
If compatible, add the minimal rule needed.
Do not over-edit unrelated skills.

## Fast heuristics

A new skill probably needs Shared Memory alignment if it mentions:
- memory
- remember
- learning
- reflection
- heartbeat
- archive
- project patterns
- habits
- preferences

A new skill probably does NOT need alignment if it is purely about:
- coding framework usage
- browser clicking
- API lookup
- search
- one-shot transformation

## Principle
Install broadly. Integrate selectively.
