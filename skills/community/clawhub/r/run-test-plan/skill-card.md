## Description:

Execute YAML test plan, stop on first failure, output rich debug prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run YAML-defined test plans, prepare setup prerequisites, execute shell, curl, and browser-driven test steps, and stop at the first failure with a debug-ready report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YAML test plans can direct setup, build, service, shell, curl, and browser actions with broad command and network control.

Mitigation: Run only trusted plans from trusted repositories and review plan values before execution.

Risk: Commands may run with sensitive environment variables or broad filesystem and network access.

Mitigation: Use a constrained environment with minimal credentials and limit filesystem and network access where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/run-test-plan)
- [Publisher Profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and test result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create test evidence files such as screenshots, API responses, service logs, and failure reports under docs/testing/evidence.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
