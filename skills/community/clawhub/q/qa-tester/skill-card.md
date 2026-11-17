## Description:

Strict QA and test engineering skill for fullstack repositories that guides test planning, unit/integration/E2E coverage, bug reproduction, regression validation, and release readiness with deterministic evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bayudsatriyo](https://clawhub.ai/user/bayudsatriyo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to plan and implement unit, integration, and E2E tests; reproduce bugs; validate regressions; and summarize release readiness with explicit evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to inspect repository code and create or update tests.

Mitigation: Review proposed file changes before accepting them, and keep tests outside production source folders.

Risk: Test commands can change local state or take time to run.

Mitigation: Run tests only after explicit user approval and report only observed results.

## Reference(s):

- [Testing Patterns](references/testing-patterns.md)
- [E2E Reliability](references/e2e-reliability.md)
- [Release Gate](references/release-gate.md)
- [ClawHub Skill Page](https://clawhub.ai/bayudsatriyo/skills/qa-tester)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown with structured QA recommendations, test code when requested, and shell commands to run later]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not run tests unless explicitly approved by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
