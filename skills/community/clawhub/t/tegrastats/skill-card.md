## Description:

Monitors NVIDIA Jetson GPU status, memory usage, CPU temperature, and frequency information with the local tegrastats utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxd9199](https://clawhub.ai/user/wxd9199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Jetson device health and runtime telemetry from tegrastats during local debugging, monitoring, or performance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The monitoring command may fail or provide irrelevant output on systems where NVIDIA Jetson tegrastats is not expected to exist.

Mitigation: Install and use the skill only on Jetson environments that include the system-bundled tegrastats utility.

Risk: The artifact documentation is Chinese-only, which may reduce reviewer accessibility in some deployment environments.

Mitigation: Review or translate the documentation before deployment when language accessibility matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxd9199/skills/tegrastats)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash command examples and plain text tegrastats output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Jetson system where the bundled tegrastats command is available.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
