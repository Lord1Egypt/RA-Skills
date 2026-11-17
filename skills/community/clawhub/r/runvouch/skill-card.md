## Description:

RunVouch monitors OpenClaw agent runs by reporting run start and end events, tool use, costs, and evidence so missed runs, loops, and runaway spend can trigger alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runvouch](https://clawhub.ai/user/runvouch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect unattended OpenClaw agents to RunVouch monitoring for run check-ins, cost caps, loop detection, heartbeats, and outcome evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exact tool inputs and detailed operational telemetry may expose secrets, private prompts, customer data, or proprietary code to the configured external endpoint.

Mitigation: Enable the skill only in approved workspaces, require redaction or minimization of sensitive tool inputs, and get administrator approval before production use.

Risk: Remote RunVouch status can influence whether an agent trusts another agent's output.

Mitigation: Treat RunVouch status as one operational signal and require human review before blocking or relying on critical downstream work.

## Reference(s):

- [RunVouch website](https://runvouch.com)
- [RunVouch ClawHub skill page](https://clawhub.ai/runvouch/skills/runvouch)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint paths, environment variables, heartbeat cadence, and outcome evidence expectations.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
