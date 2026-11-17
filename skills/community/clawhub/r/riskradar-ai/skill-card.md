## Description:

AI Code Review and Code Risk Review quality gate for Git Diff, release readiness, regression testing, security testing, dependency impact, runtime risk, LLM testing, Agentic AI risk, and RAG security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[start-fish](https://clawhub.ai/user/start-fish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests, Git diffs, source code, and AI-enabled workflows for release risks, security exposure, dependency impact, runtime failure paths, and regression-test gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked for broad code review, testing, security, and release-readiness prompts, which can expose proprietary code or sensitive configuration to the agent.

Mitigation: Use it only on repositories and diffs that are approved for agent inspection, and review the scope before installation or invocation.

Risk: The skill produces review guidance and release recommendations that could affect deployment decisions.

Mitigation: Require human review of findings, verification steps, and release recommendations before using them as a release gate.

## Reference(s):

- [Code Risk Review Playbook](references/code-risk-review-playbook.md)
- [ClawHub skill listing](https://clawhub.ai/start-fish/skills/riskradar-ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity, confidence, exact code location, impact, verification steps, test strategy, evidence checklist, open questions, and release recommendation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
