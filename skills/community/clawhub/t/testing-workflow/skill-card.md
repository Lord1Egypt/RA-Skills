## Description:

Testing Workflow orchestrates project testing by routing agents through discovery, strategy, implementation, validation, and maintenance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to set up, improve, validate, and maintain testing workflows across unit, integration, and end-to-end coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended installer executes unpinned remote tooling from a mutable branch.

Mitigation: Install from a pinned, reviewed commit or use the manual copy path after inspecting the files, and do not run the installer with elevated privileges.

Risk: Invoking the skill can lead an agent to inspect a project and propose or make test, documentation, and CI-related changes.

Mitigation: Review proposed changes before applying them, run the relevant test suite, and separately trust any related skills the workflow routes to.

## Reference(s):

- [Testing Workflow ClawHub Page](https://clawhub.ai/wpank/skills/testing-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code blocks, shell commands, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route the agent to related testing, code review, quality gate, and debugging skills when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
