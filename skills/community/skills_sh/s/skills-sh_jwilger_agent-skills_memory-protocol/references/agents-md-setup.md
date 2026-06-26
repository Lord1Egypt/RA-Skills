# Memory Protocol — AGENTS.md Setup

This file tells the `bootstrap` skill what to add to AGENTS.md when the
`memory-protocol` skill is installed. Bootstrap wraps this content in
`<!-- BEGIN MANAGED: memory-protocol -->` / `<!-- END MANAGED: memory-protocol -->`
markers.

## Section: Conventions (append)

Add these items to the existing Conventions bullet list:

- Search project memory (Memento MCP) before starting any non-trivial task, when encountering errors or unexpected behavior, and when receiving corrections — before attempting fixes or implementations
- After resolving a non-obvious problem, receiving a user correction, or establishing a new convention, store the discovery in project memory immediately

## Section: Memory-Aware Workflow (new section, after Conventions)

Add this as a new top-level section in AGENTS.md:

```markdown
## Memory-Aware Workflow

This project uses persistent cross-session memory via the `memory-protocol` skill
and Memento MCP. The following situations require memory interaction:

**Search memory BEFORE acting when:**
- Starting any new task or feature (check for relevant past learnings)
- Encountering an error, test failure, or unexpected behavior (it may have been solved before)
- Receiving a correction from the user (check if this correction was already stored — if so, you failed to recall)
- Debugging an intermittent or recurring issue
- About to make a process decision (ADR, commit, PR, deployment)
- Spawning subagents (check for coordination learnings)
- Resuming work in a new session

**Every search requires two queries** (multi-dimensional search):
1. The specific technical topic (error message, feature name, library)
2. Process/workflow learnings about this *type of work* (e.g., "TDD mistakes", "deployment conventions", "API endpoint patterns")

**Store to memory AFTER discovery when:**
- You solved a non-obvious problem (especially one that required debugging)
- The user corrected your approach or output
- A new convention or architectural decision was established
- You learned something that would help in a future session

See the `memory-protocol` skill for the full protocol including graph traversal and storage format.
```
