## Description:

Monitors OpenClaw API usage on Windows by reading local usage logs, estimating calls, tokens, and cost, and generating usage reports and quota alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guowaa223](https://clawhub.ai/user/guowaa223)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using OpenClaw on Windows use this skill to monitor local API consumption, check whether daily or weekly quotas are sufficient, and produce text or JSON reports for usage review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw logs and can write local reports or state files that may expose usage, model, session, or cost information.

Mitigation: Run it only in a trusted local workspace, restrict permissions on logs and generated reports, and review data-handling expectations before sharing outputs.

Risk: The documentation includes a Windows scheduled-task example for persistent recurring execution.

Mitigation: Create scheduled tasks only after review, using least privilege, absolute executable and script paths, controlled script permissions, and a documented removal command.

Risk: Quota and cost outputs are estimates derived from local logs and configured model rates.

Mitigation: Use the reports for operational guidance and verify important billing or quota decisions against official provider records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guowaa223/skills/windows-api-monitor)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style guidance with inline shell commands; scripts emit text or JSON usage reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows and OpenClaw log locations, quota settings, and alert thresholds shape the reported results; cost estimates should be checked against official billing.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
