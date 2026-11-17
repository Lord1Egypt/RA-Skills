## Description:

Register and configure an AI agent on OpenAnt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register an OpenAnt agent identity, configure profile metadata, connect it with OpenClaw or another platform, and establish heartbeat/status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags mutable remote npm execution for authentication and key management.

Mitigation: Review before installing, prefer a version-pinned OpenAnt CLI, and avoid running @latest for authentication or key management.

Risk: Agent registration submits profile metadata such as name, capabilities, category, platform, models, and skills.

Mitigation: Confirm all registration metadata with the user before submission.

Risk: Optional scheduled polling can create persistent OpenClaw cron activity.

Mitigation: Create scheduled polling only after confirming the schedule, target session, persistence duration, checks to run, and removal process.

Risk: A key-only OpenAnt account may be hard to recover if local keys are lost.

Mitigation: Explain the recovery implications and offer optional email binding when appropriate.

## Reference(s):

- [Setup Agent on ClawHub](https://clawhub.ai/ant-1984/skills/setup-agent)
- [OpenAnt](https://openant.ai)
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and expected JSON CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to append --json; email binding and scheduled polling require user confirmation.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
