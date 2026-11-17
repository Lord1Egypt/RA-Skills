## Description:

Professional software-testing skill for AI coding agents. Use this skill when a user needs to write, run, design, or strategize tests: unit tests (Python pytest or JS Jest/Vitest), end-to-end tests (Playwright), API tests (REST/GraphQL), performance or load tests (k6/Locust), security tests (OWASP API Top 10), visual regression, contract testing, or to design a test strategy, coverage gates, or a TDD workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT

## Use Case:

Developers and software engineers use this skill to plan, write, and review tests across unit, API, browser, performance, security, and contract testing. It also helps create test plans, coverage gates, test scaffolds, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags cleanup guidance that works around host safety protections, which could enable unsafe unattended actions.

Mitigation: Honor safety denials, revise cleanup guidance before unattended use, and require approval for cleanup actions.

Risk: Active, performance, or security tests can affect services or data when run against shared or production systems.

Mitigation: Use disposable environments and agreed test limits; run only against authorized targets.

Risk: Browser captures may contain sensitive information, and cloud snapshot processing can expose data.

Mitigation: Protect browser captures and obtain approval before processing cloud snapshots.

Risk: Downloaded dependencies, generated assertions, and coverage gates can introduce unreviewed behavior or misleading results.

Mitigation: Review and pin installation sources, then validate generated assertions and coverage gates.

## Reference(s):

- [Unit testing playbook](references/unit-testing.md)
- [End-to-end testing playbook](references/e2e-testing.md)
- [API testing playbook](references/api-testing.md)
- [Test strategy playbook](references/test-strategy.md)
- [Security testing playbook](references/security-testing.md)
- [Performance testing playbook](references/performance-testing.md)
- [Contract testing playbook](references/contract-testing.md)
- [Reporting playbook](references/reporting.md)
- [Visual regression playbook](references/visual-regression.md)
- [Code review playbook](references/code-review-playbook.md)
- [ClawHub skill page](https://clawhub.ai/skills-repo/skills/software-tester)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown plans and reports, runnable test code, shell commands, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-specific; depends on the codebase, test framework, and user-provided scope.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
