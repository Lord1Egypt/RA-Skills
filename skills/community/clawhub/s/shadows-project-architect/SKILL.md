---
name: project-architect
description: "Structured project planning — requirements analysis, architecture design, task breakdown, dependency mapping, milestone definition. Use when starting a new project or major feature."
metadata: { "openclaw": { "emoji": "🏗️", "homepage": "https://clawhub.ai/NakedoShadow", "os": ["darwin", "linux", "win32"] } }
---

# Project Architect — Structured Planning Protocol

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Starting a new project from scratch
- Planning a major feature or module
- User says "plan this", "architect", "design the system"
- Refactoring a large codebase
- Breaking a monolith into services

## WHEN NOT TO TRIGGER

- Small bug fixes or single-file changes
- User already has a detailed plan
- Quick prototyping / experimentation

## PREREQUISITES

No binaries required. This is a pure planning and reasoning skill. It produces structured text output (project plans, architecture documents, task breakdowns) without executing any commands or requiring any external tools.

---

## PROTOCOL — 5 PHASES

### Phase 1 — REQUIREMENTS CAPTURE

Ask the user (max 5 questions):
1. **What** — What does this system/feature do? (core functionality)
2. **Who** — Who uses it? (user personas)
3. **Scale** — Expected load/data volume? (performance requirements)
4. **Constraints** — Tech stack preferences, budget, timeline?
5. **Integration** — What existing systems does it connect to?

### Phase 2 — ARCHITECTURE DESIGN

Based on requirements, define:

**System Components**:
```
[Component A] --> [Component B] --> [Component C]
       |                                  |
       v                                  v
  [Database]                        [External API]
```

For each component:
- Responsibility (single purpose)
- Interface (inputs/outputs)
- Technology choice (with rationale)
- Data model (key entities)

**Architecture Decisions Record (ADR)**:
```markdown
### ADR-001: [Decision Title]
- **Status**: Accepted
- **Context**: [Why this decision was needed]
- **Decision**: [What was decided]
- **Consequences**: [Trade-offs accepted]
```

### Phase 3 — TASK BREAKDOWN

Break the project into implementable tasks:

```markdown
## Epic 1: [Name]
- [ ] Task 1.1: [Description] (~Xh)
- [ ] Task 1.2: [Description] (~Xh)
  - Depends on: Task 1.1
- [ ] Task 1.3: [Description] (~Xh)

## Epic 2: [Name]
- [ ] Task 2.1: [Description] (~Xh)
  - Depends on: Task 1.2
```

Rules:
- Each task must be completable in 1-4 hours
- Dependencies explicitly stated
- Effort estimate for each task
- Tasks ordered by dependency chain

### Phase 4 — DEPENDENCY MAPPING

Identify critical path:
1. Map task dependencies as a directed graph
2. Identify the longest path (critical path)
3. Identify parallelizable work streams
4. Flag external dependencies (APIs, approvals, data)

### Phase 5 — MILESTONE DEFINITION

Define 3-5 milestones:
```markdown
### Milestone 1: Foundation (Week 1)
- [x] Project setup, CI/CD pipeline
- [x] Core data models
- [x] Basic API skeleton
**Demo**: API responds to health check

### Milestone 2: Core Features (Week 2-3)
- [ ] Feature A implementation
- [ ] Feature B implementation
**Demo**: User can perform primary workflow

### Milestone 3: Polish & Deploy (Week 4)
- [ ] Error handling, edge cases
- [ ] Documentation
- [ ] Production deployment
**Demo**: Live system accessible to users
```

---

## SECURITY CONSIDERATIONS

This skill is purely advisory — it generates project plans, architecture documents, and task breakdowns as text output. It does not execute commands, read sensitive files, make network calls, or modify any configuration. Zero risk profile.

---

## OUTPUT FORMAT

```markdown
# Project Plan: [Name]
**Date**: [YYYY-MM-DD]

## 1. Requirements Summary
[Concise requirements from Phase 1]

## 2. Architecture
[Diagram + component descriptions + ADRs]

## 3. Task Breakdown
[Epics with tasks, estimates, dependencies]

## 4. Critical Path
[Dependency chain visualization]

## 5. Milestones
[3-5 milestones with demo criteria]

## 6. Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| ...  | ...        | ...    | ...        |

## 7. Next Steps
[First 3 tasks to start immediately]
```

---

## RULES

1. **Ask before assuming** — never design without understanding requirements
2. **Simple first** — start with the simplest architecture that could work
3. **No over-engineering** — design for current needs, not hypothetical futures
4. **Explicit dependencies** — every task must state what it depends on
5. **Demo-driven milestones** — each milestone must have a demonstrable outcome

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
