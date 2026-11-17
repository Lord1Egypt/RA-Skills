## Description:

This skill generates standardized Markdown-table test cases for functional, API, UI, compatibility, platform-specific, and AI Agent testing while excluding test plans, test strategies, automation scripts, vulnerability scanning, and performance or load testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassianran](https://clawhub.ai/user/cassianran)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use this skill to turn feature, API, platform, or AI Agent requirements into executable test cases with concrete inputs, expected results, priorities, and checklist-based coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated test cases could contain incorrect assumptions or unsafe execution steps if used without review.

Mitigation: Review each generated case against the target requirement, environment, and authorization boundary before execution.

Risk: Example credentials, bearer tokens, payment actions, or production data could be copied into generated test cases.

Mitigation: Use test-only placeholders, sandbox payment rails, and non-production data when adapting generated cases.

Risk: The broad Agent trigger may produce overly broad AI Agent test coverage when the user's request is ambiguous.

Mitigation: Narrow prompts by naming the agent workflow, tool boundary, data sensitivity, and platform under test.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cassianran/skills/software-test-case-design)
- [General test case rules](references/templates/common-rules.md)
- [Functional testing capability](references/core-capabilities/functional-testing.md)
- [API testing capability](references/core-capabilities/api-testing.md)
- [AI Agent testing capability](references/core-capabilities/agent-testing.md)
- [Test case output format](references/examples/format-spec.md)
- [Common checklist](references/checklists/common-checklist.md)
- [API checklist](references/checklists/api-checklist.md)
- [Agent checklist](references/checklists/agent-checklist.md)
- [Mobile app platform guidance](references/platform/mobile-app.md)
- [Mobile web platform guidance](references/platform/mobile-web.md)
- [Mini-program platform guidance](references/platform/mini-program.md)
- [Desktop platform guidance](references/platform/desktop.md)
- [PC web platform guidance](references/platform/pc-web.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Test cases include concrete steps and expected results; generated cases require review before execution.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
