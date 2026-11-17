## Description:

Write and run tests across languages and frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexwoo-awso](https://clawhub.ai/user/alexwoo-awso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to choose, write, and run unit, integration, and end-to-end tests while respecting the project's existing language, package manager, and test framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package-install and Playwright browser-install commands can change project dependencies or toolchain state.

Mitigation: Prefer existing lockfiles, package scripts, and locally installed test tools; require approval before adding dependencies or browser packages, and pin or review versions for sensitive projects.

Risk: Applying generic testing guidance mechanically could introduce a new framework where the project already has a working test stack.

Mitigation: Start by detecting the language, package manager, and existing framework, then prefer the current stack before adding a new one.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/alexwoo-awso/skills/test-runner-codex)
- [Original ClawHub skill](https://clawhub.ai/cmanfre7/test-runner)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
