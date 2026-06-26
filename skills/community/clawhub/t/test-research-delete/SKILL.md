---
name: research
description: Orchestrate parallel codebase research. Spawns multiple researcher subagents to investigate different areas, then synthesizes findings into research.md.
---

# Research Orchestration

Methodology for systematic codebase research using parallel subagents.

## Purpose

This skill runs on the **main thread** and orchestrates multiple `researcher` subagents to investigate a codebase in parallel. Produces a `research.md` file for downstream planning.

**Mandate:** Document the codebase as it exists today. No improvements, no critique, no suggested changes—pure technical mapping.

## Workflow

### Step 1: Capture the Research Question

Record the exact research question from `$ARGUMENTS`.

If no arguments provided, ask the user for their research question before proceeding.

### Step 2: Read Referenced Files First

If the user mentions specific files, read them completely before spawning agents. Use Read tool without limit/offset.

### Step 3: Decompose into Investigation Areas

Break the research question into 3-5 distinct investigation areas. For each define:

- **Search targets** - patterns, keywords, file types
- **Search locations** - directories, file patterns
- **Questions to answer** - what we need to learn

### Step 4: Spawn Parallel Researcher Subagents

Use the Task tool to spawn multiple `researcher` subagents in parallel. Each investigates one area.

**Critical:** Send ALL Task tool calls in a SINGLE message to run them in parallel.

```
Task tool calls (all in one message):
- subagent_type: "researcher"
- prompt: "Investigate [area]. Search targets: [targets]. Search locations: [locations]. Questions: [questions]"
- description: "Research [area name]"
```

Example parallel spawn:
```
[Task 1] subagent_type: researcher
         prompt: "Investigate authentication middleware and guards.
                  Search targets: auth, jwt, session, middleware, guard patterns
                  Search locations: src/, lib/
                  Questions: Where is auth middleware defined? How are routes protected? What token format is used?"

[Task 2] subagent_type: researcher
         prompt: "Investigate user model and storage.
                  Search targets: User, schema, model, database, repository patterns
                  Search locations: src/, models/, db/
                  Questions: Where is the User model? What ORM/database is used? What fields exist?"

[Task 3] subagent_type: researcher
         prompt: "Investigate login/logout flows.
                  Search targets: login, logout, signin, signout, authenticate patterns
                  Search locations: src/, routes/, controllers/
                  Questions: What is the login endpoint? How are sessions created/destroyed?"
```

### Step 5: Collect Results

Wait for all researcher subagents to complete. Each returns:
- Key files with file:line references
- How the mechanism works
- Answers to the questions posed
- Notable details and gaps

### Step 6: Gather Metadata

Run git commands to collect:

```bash
git rev-parse --short HEAD    # commit hash
git branch --show-current     # branch name
git remote get-url origin     # repository URL
```

### Step 7: Synthesize and Write research.md

Combine all subagent findings into a single `research.md` file in the current working directory.

**Required format:**

```markdown
---
date: YYYY-MM-DD
commit: <short-hash>
branch: <branch-name>
repository: <repo-name>
topic: <research-topic>
status: complete
---

# Research: <Topic>

## Research Question

<Original question from user>

## Summary

<2-3 sentence executive summary of findings>

## Detailed Findings

### <Area 1>

<Synthesized findings with specific file:line references>

### <Area 2>

<Synthesized findings with specific file:line references>

...

## Code References

Key files and their purposes:

- `path/to/file.ts:123` - <description>
- `path/to/other.ts:45-67` - <description>

## Architecture Insights

<How components connect, data flow, key abstractions>

## Open Questions

- <Unresolved question 1>
- <Unresolved question 2>
```

### Step 8: Report Completion

After writing, report:

1. Location of research.md
2. Summary of key findings (2-3 sentences)
3. List of open questions

## Output Requirements

- **Always produce research.md** - even partial findings are valuable
- **Use file:line references** - enable navigation: `src/api/handler.ts:42`
- **Document what exists** - not what should exist
- **Note gaps** - unclear items go to Open Questions

## Example Decompositions

**"How does authentication work?"**

Investigation areas (spawn 5 researcher subagents):
1. Auth middleware and guards
2. Token/session management
3. User model and storage
4. Login/logout flows
5. Permission checking

**"Research the database layer"**

Investigation areas (spawn 5 researcher subagents):
1. ORM/query builder setup
2. Schema definitions
3. Migration system
4. Connection management
5. Query patterns
