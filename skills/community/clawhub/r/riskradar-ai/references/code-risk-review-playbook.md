# Code Risk Review Playbook

## Risk Categories

- Functional correctness
- Runtime exceptions and boundary handling
- Dependency and API contract impact
- Security and privacy exposure
- Performance and scalability risk
- Configuration and feature-flag risk
- AI workflow risk: LLM, Agent, RAG, model routing, prompt, tool calling, fallback
- Regression and release-readiness risk

## Evidence Requirements

Each finding should include:

- exact file and code location;
- trigger condition;
- user, system, or business impact;
- confidence level;
- verification path;
- suggested fix or test.

## Report Table

```markdown
| Priority | Risk | Evidence | Impact | Verification | Recommendation |
| --- | --- | --- | --- | --- | --- |
```
