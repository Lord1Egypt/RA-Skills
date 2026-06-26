---
name: tech-stack-evaluation
description: "Evaluate whether a project's current tech stack is appropriate for its goals, and recommend alternatives when maintainability, performance, or feature expansion is blocked. Trigger on 'is there a better tech stack', 'what stack should I use', 'should we rewrite this', or maintainability concerns. Produces evidence-based recommendations with effort-vs-payoff analysis."
version: 1.0.0
author: Alejandro Del Villar
license: MIT
metadata:
  hermes:
    tags: [architecture, tech-stack, maintainability, modernization, refactoring]
    related_skills: [refactor-safely, codebase-survey, spike]
---

# Tech Stack Evaluation

Evaluate whether a project's current tech stack is appropriate for its goals, and recommend alternatives when maintainability, performance, or feature expansion is blocked.

## When to Use

- User asks: "is there a better tech stack for this?", "what stack should I use?", "should we rewrite this?"
- User expresses maintainability pain: "hard to extend", "unwieldy", "everything is coupled"
- Pre-planning a new feature that the current stack can't support
- Considering a migration from prototype to production-grade

## When NOT to Use

- The user has a specific bug to fix — use `debug-issue` instead
- The user wants a new feature built on the current stack — use `draft-feature-plan`
- The project is trivial (< 20 files) — just read the files and suggest directly

## Workflow

### 1. Diagnose the real problem

Before recommending a stack change, understand what the user is actually solving for. Ask (or infer from context):

| Concern | Signal | Typical Fix |
|---------|--------|-------------|
| **Performance** | "slow on large datasets", "takes forever to load" | Optimize data layer (Polars, DuckDB, caching), not necessarily frontend framework |
| **Maintainability** | "hard to extend", "everything is coupled", "adding a feature touches 4 files" | Structural refactor (split monoliths, consolidate APIs, add type safety) |
| **Feature expansion** | "need real-time updates", "need multi-user", "need mobile app" | Add capabilities (WebSocket, DB persistence, React Native) |
| **Team growth** | "onboarding new developers", "need documentation" | Add types, tests, component library, not necessarily new framework |
| **Deployment/hosting** | "Railway is expensive", "need to scale" | Evaluate hosting alternatives, containerization, serverless |
| **Modernization** | "this feels old", "want to use current best practices" | Incremental upgrades (TypeScript, testing, CI) rather than rewrite |

**Critical insight:** Most "tech stack" questions are actually **maintainability** or **structural** questions. A React rewrite won't fix a 1,400-line monolithic processor. A type system won't help if the API has 51 endpoints where 15 would suffice.

### 2. Run a maintainability assessment

Use the `codebase-survey` skill's maintainability audit to produce evidence:

```bash
# File size audit
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.tsx" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/venv/*" | xargs wc -l | sort -rn | head -20

# Method/function count audit
grep -c "def " app/core/allocation.py          # Python methods
grep -c "@router." app/api/routes.py            # FastAPI endpoints
grep -c "function " app/static/js/charts.js     # JS functions
```

Produce a **maintainability grade** (A-F) with specific targets.

### 3. Map the current stack

| Layer | Current | What it does well | What it blocks |
|-------|---------|-------------------|----------------|
| Backend framework | | | |
| Data processing | | | |
| Frontend | | | |
| State management | | | |
| Styling | | | |
| Charts/visualization | | | |
| Hosting | | | |
| Persistence | | | |

### 4. Recommend options, not a single answer

Present 2-3 options ordered by effort vs. payoff:

| Option | Effort | Payoff | When to choose |
|--------|--------|--------|----------------|
| **Minimal** (structural refactor) | Low | Medium | Maintainability is the only concern, stack is otherwise fine |
| **Incremental** (modernize frontend) | Medium | High | Frontend is the pain point, backend is solid |
| **Full** (new stack) | High | Maximum | Multiple blockers, team growth, or multi-platform needs |

For each option, specify:
- What changes
- What stays the same
- Migration path (can it be done incrementally?)
- Risk (data loss, downtime, learning curve)

### 5. Tie recommendations to the assessment

Every recommendation must reference the evidence:
- "Split `AllocationProcessor` (1,402 lines, 36 methods) into 5 focused processors" — not "use a better framework"
- "Consolidate 51 API endpoints into ~15 with a chart registry" — not "add GraphQL"
- "Migrate frontend to React + TypeScript for component isolation and type safety" — not "React is better"

## Common Stack-Specific Patterns

### Python FastAPI + Pandas + Vanilla JS Dashboards

This is a common pattern for data-heavy internal tools. The typical evolution:

| Stage | Stack | Pain Point | Next Step |
|-------|-------|------------|-----------|
| 1 | FastAPI + Pandas + Vanilla JS | Works for 1-2 users, 5-10 charts | None needed |
| 2 | Same stack, files grow | Adding charts requires 4-file changes | Split processors, consolidate API |
| 3 | Same stack, 30+ charts, multi-user | No persistence, no sharing, frontend is spaghetti | Add React + TypeScript, consider DB |
| 4 | Growth continues | Performance issues with large datasets | Polars/DuckDB, caching, materialized views |

### When to keep FastAPI

Keep FastAPI when:
- Data processing is the core value (Pandas/Polars/NumPy workflows)
- The team knows Python well
- The app is internal/BI, not customer-facing
- Deployment is simple (Railway, Heroku)

### When to add React

Add React when:
- The dashboard has 10+ interactive views
- Multiple developers work on different tabs
- You need reusable components (filters, tables, export buttons)
- Type safety across the API boundary matters

### When to add a database

Add persistence when:
- Multi-user collaboration is needed
- Historical data/query snapshots matter
- Session loss on restart is unacceptable
- You need user accounts, permissions, or audit logs

## Anti-patterns to Avoid

1. **Recommending a rewrite when a refactor suffices.** If the backend logic is solid but the frontend is messy, don't suggest rewriting the whole stack. Isolate the problem.
2. **Recommending new tech without evidence.** "Use Next.js" is not a recommendation. "Migrate to Next.js because the current vanilla JS has 45 nearly-identical API loader functions that a React + TanStack Query stack would collapse to 5" is.
3. **Ignoring the user's domain expertise.** If the user built a complex system in 10 weeks, their velocity is not standard. Recommendations should match their throughput model, not a typical team's.
4. **Forgetting deployment constraints.** A recommendation that requires Kubernetes when the user uses Railway is not actionable.
5. **Not considering the data model.** Stateless file-upload apps have different needs than multi-tenant SaaS. Don't suggest Postgres for a project that genuinely doesn't need persistence.

## Verification Checklist

- [ ] Real problem diagnosed (performance vs. maintainability vs. features vs. team)
- [ ] Maintainability assessment completed with file size/method counts
- [ ] Current stack mapped with pros/cons per layer
- [ ] 2-3 options presented with effort/payoff/risk
- [ ] Every recommendation tied to specific evidence from the assessment
- [ ] Migration path is incremental (not all-or-nothing)
- [ ] Deployment constraints considered
- [ ] User's velocity and expertise factored in
