## Description:

Use the robotx CLI to deploy, manage versions, and check status for RobotX applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haibingtown](https://clawhub.ai/user/haibingtown)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment agents use this skill to install or invoke the RobotX CLI, authenticate to a RobotX server, deploy applications, inspect projects and versions, stream logs, and publish builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow can execute unverified remote shell scripts from a mutable GitHub branch.

Mitigation: Review installer source before use and prefer a pinned release or verified checksum/signature instead of curl-to-bash.

Risk: RobotX credentials may be exposed through environment variables or ~/.robotx.yaml.

Mitigation: Scope and rotate the RobotX API key, avoid installing in environments with unrelated sensitive credentials, and protect ~/.robotx.yaml with restrictive permissions.

## Reference(s):

- [RobotX hosted login](https://robotx.xin)
- [RobotX ClawHub skill page](https://clawhub.ai/haibingtown/skills/robotx)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For automated workflows, the skill recommends RobotX CLI commands with JSON output written to stdout and progress logs written to stderr.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
