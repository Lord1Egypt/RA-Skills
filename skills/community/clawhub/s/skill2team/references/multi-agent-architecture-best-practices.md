# Multi-Agent Architecture Best Practices

Skill2Team designs a conceptual agent architecture relationship graph, not a framework-specific runtime graph.

## Framework-neutral representation

Use a relationship graph that can later be mapped to an explicitly selected multi-agent runner:

- agent nodes represent stable roles, responsibilities, capabilities, tool/resource access, and output contracts;
- typed edges represent routing, delegation, handoff, review, guardrail, state/artifact transfer, fan-out/fan-in, human wait, checkpoint, and terminal boundaries;
- workflow nodes remain separate from agent nodes unless they create a durable accountability boundary;
- runtime-specific names such as framework nodes, tasks, teams, crews, or handoffs are adapters, not the default architecture language.

## Current best-practice rules

1. Keep role boundaries narrow enough that each agent has a clear mission and a clear non-responsibility list.
2. Model handoffs explicitly: trigger, input artifact, expected output, owner, reviewer/gate, and failure behavior.
3. Separate producer, reviewer, and guardrail responsibilities when output quality or safety matters.
4. Preserve human intervention points instead of silently automating approvals, selections, and no-auto-continue boundaries.
5. Track state and artifacts by owner; rerun downstream work only when consumed upstream artifacts become stale.
6. Keep package metadata runtime-neutral, then provide a Codex adapter only when `Delivery: package` targets Codex.
7. Design continuation may mention framework adapters; package-end guidance must focus on using the converted target team in Codex.

## Package implication

For `Delivery: package`, the generated target-team package must contain:

- Codex custom-agent files and manifests;
- the full design result in `design-output.zip`;
- framework-neutral architecture and workflow maps;
- conformance/audit contracts;
- package-end prompts only for Codex registration, smoke tests, registered entry-agent use, and current-session Codex fan-out when same-thread hot-load fails.
