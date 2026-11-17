## Description:

Guides developers in declaring, running, and automating Rez 3.4.0 package tests in CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CI engineers use this skill to define Rez package tests, troubleshoot test selection, and run named tests in pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running package tests can execute commands declared by the package being tested.

Mitigation: Review package-defined tests and CI commands, including install paths, before execution.

Risk: A bare rez-test run skips tests not tagged default, leaving CI coverage incomplete.

Mitigation: List available tests and explicitly run the required named tests in CI.

## Reference(s):

- [rez-test-ci on ClawHub](https://clawhub.ai/loonghao/skills/rez-test-ci)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python, shell, and CI YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance targets Rez 3.4.0.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
