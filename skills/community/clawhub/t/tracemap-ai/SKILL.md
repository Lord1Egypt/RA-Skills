---
name: tracemap-ai
description: Requirements Traceability and Test Case Validation skill for PRD analysis, requirement coverage, coverage gap detection, multi-repo testing, acceptance testing, traceability matrix, LLM testing, Agentic AI, and RAG testing.
triggers:
  - requirements-traceability
  - test-case-validation
  - requirement-coverage
  - coverage-gap
  - acceptance-testing
  - multi-repo-testing
  - qa-report
  - traceability-matrix
  - defect-analysis
  - prd-analysis
  - spec-validation
  - agentic-ai
  - rag-testing
  - llm-testing
role: specialist
scope: testing
output-format: report
---

# TraceMap AI

TraceMap AI verifies whether requirements, test cases, and code changes truly line up. It converts PRDs, specs, acceptance criteria, test cases, and multi-repo code changes into a requirement-test-code traceability matrix.

It works for product features, backend services, frontend flows, mobile apps, APIs, data pipelines, AI workflows, LLM integrations, agents, RAG systems, and cross-repository releases.

## When To Use

Use this skill when you need to:

- Validate whether a PRD or spec is fully covered by test cases and code changes.
- Review test cases before development, test execution, or release acceptance.
- Analyze multi-repo changes across frontend, backend, services, configuration, prompts, data pipelines, and integrations.
- Build traceability evidence for QA sign-off, release governance, or product acceptance.
- Identify uncovered requirements, weak acceptance criteria, missing evidence, and high-impact defects.

## Core Workflow

1. **Collect inputs**: PRD, spec, acceptance criteria, test cases, repositories, Git Diff, configuration, prompt/model changes, and release scope.
2. **Extract requirements**: split product and technical requirements into atomic, testable acceptance points.
3. **Map implementation**: connect each requirement to code files, services, APIs, configs, prompts, models, and data flows.
4. **Map tests**: connect each requirement to test cases, fixtures, expected evidence, and execution results.
5. **Analyze coverage**: classify covered, partially covered, uncovered, redundant, blocked, and untestable requirements.
6. **Analyze defects**: identify severity, priority, reproduction steps, business impact, and owner suggestions.
7. **Generate report**: produce a traceability matrix, gap summary, defect list, and release acceptance recommendation.

## Reference Guides

| Topic | Reference | Load When |
| --- | --- | --- |
| Traceability validation | `references/traceability-validation-playbook.md` | Always use for coverage categories, mapping dimensions, and matrix template |

## Required Output

Produce a Markdown report with:

- Executive summary and release acceptance recommendation.
- Requirement-test-code traceability matrix.
- Coverage summary: covered, partial, uncovered, redundant, blocked.
- Defect list with severity, priority, reproduction steps, owner, and fix recommendation.
- AI workflow validation matrix when applicable.
- Evidence checklist and open questions.

## AI Workflow Validation Matrix

```markdown
## AI Workflow Validation Matrix

| Requirement ID | Scenario | AI/Model/Agent Link | Test Case | Code Location | Evidence | Coverage Result | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

## Quality Bar

- Do not mark a requirement as covered unless there is clear test and code evidence.
- Distinguish missing implementation from missing tests.
- Every defect must include impact and reproduction path.
- Every AI workflow must include fallback, observability, and safety checks.
- If evidence is incomplete, state what needs to be provided.
