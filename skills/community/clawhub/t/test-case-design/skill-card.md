## Description:

Chinese-language skill for generating standardized software test case tables for functional, API, AI agent, UI, routing, linkage, and platform-specific testing scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassianran](https://clawhub.ai/user/cassianran)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, product teams, and developers use this skill to turn software features, APIs, agent behaviors, and platform requirements into executable Markdown test case tables. It focuses on test case design and excludes test plans, test strategy, penetration testing execution, vulnerability scanning, load testing, and automation scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cases may include illustrative credentials, token-like values, payments, permissions, file operations, or agent tool actions.

Mitigation: Use fake secrets, test accounts, non-production payment paths, and controlled environments when adapting generated cases.

Risk: The Agent trigger is broad and may produce agent-oriented cases when a request only loosely mentions agents.

Mitigation: Review generated cases for scope fit before using them in a test suite, especially for credential, file, permission, or tool-use scenarios.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cassianran/skills/test-case-design)
- [Skill Definition](SKILL.md)
- [Common Test Case Rules](references/templates/common-rules.md)
- [Output Format Specification](references/examples/format-spec.md)
- [Functional Testing Capability](references/core-capabilities/functional-testing.md)
- [API Testing Capability](references/core-capabilities/api-testing.md)
- [AI Agent Testing Capability](references/core-capabilities/agent-testing.md)
- [PC Web Platform Testing](references/platform/pc-web.md)
- [Mobile App Platform Testing](references/platform/mobile-app.md)
- [Mini Program Platform Testing](references/platform/mini-program.md)
- [Mobile Web Platform Testing](references/platform/mobile-web.md)
- [Desktop Platform Testing](references/platform/desktop.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs standardized test case fields including ID, title, type, module, priority, preconditions, steps, expected results, actual result, and status.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
