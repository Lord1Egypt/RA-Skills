---
name: riskradar-ai
description: AI Code Review and Code Risk Review quality gate for Git Diff, release readiness, regression testing, security testing, dependency impact, runtime risk, LLM testing, Agentic AI risk, and RAG security.
triggers:
  - code-risk-review
  - ai-code-review
  - git-diff-review
  - quality-gate
  - regression-testing
  - test-strategy
  - runtime-risk
  - dependency-impact
  - security-testing
  - performance-risk
  - agentic-ai-risk
  - rag-security
  - llm-testing
  - qa-automation
  - release-readiness
role: specialist
scope: testing
output-format: report
---

# RiskRadar AI

RiskRadar AI is a general-purpose code risk review and release-quality gate skill for software teams. It turns code changes into actionable engineering and QA evidence: exact code locations, impact, severity, confidence, test strategy, and release recommendation.

It works for backend, frontend, mobile, platform, data, AI, LLM, Agent, RAG, API, infrastructure, and integration-heavy systems.

## When To Use

Use this skill when you need to:

- Review a pull request or Git Diff before release.
- Find functional, runtime, dependency, security, performance, compatibility, and regression risks.
- Review AI-enabled workflows such as LLM calls, agents, RAG retrieval, prompt templates, tool calling, and model fallback logic.
- Build a release quality gate with concrete verification steps.
- Generate unit, integration, E2E, adversarial, resilience, and monitoring test recommendations.

## Core Workflow

1. **Scope the change**: identify repositories, files, Git Diff, affected modules, user flows, APIs, data flows, and runtime boundaries.
2. **Map critical paths**: trace state transitions, external dependencies, persistence, network calls, async jobs, permissions, and user-visible impact.
3. **Identify AI dependencies**: detect LLM calls, agents, RAG, prompt templates, model routing, tool calls, feature flags, and fallback behavior when applicable.
4. **Analyze risks**: classify functional, runtime, dependency, security, performance, AI, privacy, resilience, and regression risks.
5. **Validate evidence**: link every finding to code, configuration, data flow, logs, tests, or product behavior.
6. **Design tests**: produce targeted unit, integration, E2E, adversarial, resilience, and monitoring tests.
7. **Write the report**: include severity, confidence, exact location, impact, verification steps, and release recommendation.

## Reference Guides

| Topic | Reference | Load When |
| --- | --- | --- |
| Code risk review | `references/code-risk-review-playbook.md` | Always use for risk classification, evidence requirements, and report table |

## Required Output

Produce a Markdown report with:

- Executive summary and release recommendation.
- Risk table with severity, confidence, exact code location, impact, and fix/test recommendation.
- AI workflow risk section when LLM, Agent, RAG, model, or tool-calling logic is involved.
- Test strategy by layer: unit, integration, E2E, adversarial, resilience, monitoring.
- Evidence checklist and open questions.

## AI Workflow Risk Section

```markdown
## AI Workflow Risk Review

| Risk | Code Location | User/System Impact | AI/Model/Agent Link | Evidence Needed | Verification | Priority |
| --- | --- | --- | --- | --- | --- | --- |
```

## Quality Bar

- Do not invent risks without code or configuration evidence.
- Every high-severity risk must include a concrete reproduction or verification path.
- Separate facts, assumptions, and inferred risks.
- Prefer actionable, release-blocking findings over generic advice.
- If evidence is insufficient, state exactly what is missing.
