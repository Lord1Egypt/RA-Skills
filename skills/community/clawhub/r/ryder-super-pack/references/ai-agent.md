# AI Agent Builder (OpenClaw Optimized)

This reference defines the architecture and orchestration patterns for high-performance AI agents within the OpenClaw environment.

## 1. Core Architectures

### Pattern: ReAct (Reason + Act)
*Best for: open-ended research, dynamic tool use.*
OpenClaw agents use the `thought` -> `call` -> `response` loop natively. 
- **Optimization**: Use `thought: on` in session status to monitor reasoning.
- **Tooling**: Prefer specific tools over generic `exec` when available (e.g., `web_search` for research).

### Pattern: Plan-and-Execute
*Best for: multi-step engineering, complex migrations.*
1. **Planner**: Generates a `TodoList` or `PLAN.md`.
2. **Executor**: Uses `subagents spawn` to handle atomic steps.
3. **Verification**: Each step must have a terminal `exec` or `read` check.

## 2. Subagent Coordination (The Ryder Method)

**The Ryder Rule**: Never do in one turn what can be delegated to a specialist.

### Topology: Hub-and-Spoke
- **Ryder (Orchestrator)**: Manages state, handles user comms, dispatches tasks.
- **Specialists (Subagents)**:
  - `coder`: Writes/refactors code.
  - `researcher`: Fetches docs via `web_fetch`.
  - `reviewer`: Audits against `SKILL.md` criteria.

### Workflow: Two-Stage Review
1. **Implementation**: Subagent completes task.
2. **Spec Compliance**: Different subagent verifies against requirements.
3. **Code Quality**: Final audit for style, security, and performance.

## 3. Tool-Integrated RAG

OpenClaw's memory system is your RAG.
- **Ingestion**: Use `write` to save high-value context to `memory/`.
- **Retrieval**: Use `memory_search` with specific queries before every complex decision.
- **Update**: Use `memory_get` to pull exactly what you need, avoiding context bloat.

## 4. MCP Server Development
*Phase-based approach for OpenClaw:*
1. **Research**: `web_fetch` the API docs.
2. **Scaffold**: Create the server using TypeScript template.
3. **Deploy**: Use `exec` to run and test locally via stdio.
4. **Eval**: Generate 10 complex test cases.

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*
