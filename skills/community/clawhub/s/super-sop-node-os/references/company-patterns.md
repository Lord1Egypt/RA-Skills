# Company Pattern Radar

Latest full radar: `docs/REFERENCE_RADAR_2026-06-12.md` in the source repository.

Use these patterns when applying Super SOP Node OS:

| Pattern | Learned From | Node Mapping |
|---|---|---|
| Project loader files and skills are durable context | OpenAI Codex, Codex Skills, OpenClaw Skills | Context, Sediment |
| Workflows should route, branch, parallelize, and evaluate | Anthropic Building Effective Agents | Planning, Routing, Score, Check |
| Context must be engineered through sessions, memory, artifacts, and token control | Google ADK, LangGraph | Context, Data Modeling |
| Agent handoff needs task state and artifacts | Google A2A, Microsoft Agent Framework | Handoff, Data Modeling |
| Long-running work needs persistence and interrupts | LangGraph | Action, Check, Sediment |
| Enterprise agents need state, telemetry, middleware, and governance | Microsoft Agent Framework, Feishu | Data Modeling, Check |
| Visual workflow nodes require explicit input/output contracts | Coze Studio | Planning, Action, Check |
| Evaluation and trace loops are core AgentOps | Coze Loop, Anthropic evals, OpenAI tracing, AgentScope | Test, Score, Check |
| Learning should be interactive, not only explanatory | OpenMAIC | Learning, Test, Score |
| Experience should become reusable skills/rules | Hermes, OpenClaw, Codex Skills | Sediment |
| Long-horizon agents need sandbox, memory, filesystem, and subagents | DeerFlow, AgentScope | Routing, Action, Check |

Rule:

```text
When a framework offers a useful concept, map it into node purpose, input, output, check, and sediment format before adopting it.
```
