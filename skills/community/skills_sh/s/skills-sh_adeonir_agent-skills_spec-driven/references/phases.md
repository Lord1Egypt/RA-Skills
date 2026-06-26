# Subagent Dispatch

Protocol for dispatching subagents during phase execution.

## When to Use

Referenced from each phase ref (design, tasks, implement, audit)
when deciding how to dispatch subagents for context isolation.

## Workflow

Dispatch fires for every phase that runs above Small -- auto-sizing decides the
*depth* of the dispatched work, not whether to dispatch. Disk artifacts are the
handoff for discovery and execution subagents -- they don't return findings
through the context. Plan and audit subagents are read-only by harness contract:
they return structured slot fillers (tables, lists, rows) that the main agent
composes into the artifact via the canonical template.

At **Medium**, design, tasks, and audit dispatch their subagents at light depth
-- the same isolation as Large/Complex, with a reduced slot set. The implement
subagent dispatches per invocation at every scope. Only quick mode (Small) runs
entirely without dispatch.

## Dispatch Map

Full dispatch instructions live in each reference that uses them:

| Subagent | Defined in |
|-----------|-----------|
| Research subagents (one per unknown topic) | [design.md](design.md) Step 5 |
| Codebase exploration subagent | [design.md](design.md) Step 6 |
| Design Plan subagent | [design.md](design.md) Step 10 |
| Tasks Plan subagent | [tasks.md](tasks.md) Step 4 |
| Implement subagent | [implement.md](implement.md) Step 4 |
| Audit subagent (read-only evidence + verdict) | [audit.md](audit.md) Step 2a |

Research and exploration subagents in design.md run in the same
dispatch turn (independent). The Design Plan subagent runs after
exploration artifacts exist. The Tasks Plan subagent runs after
design.md exists. The implement subagent runs after design/tasks
artifacts exist. The audit subagent runs after implement sets
`to-review`.
