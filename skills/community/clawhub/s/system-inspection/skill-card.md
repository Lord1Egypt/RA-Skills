## Description:

System Inspection is an OpenClaw health-check SOP for periodically inspecting gateway status, channels, cron tasks, and recent error logs, then reporting only actionable findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect an OpenClaw runtime for gateway availability, channel health, task failures, log errors, and configuration drift. It is intended to return concise conclusion, cause, and recommendation lines, or stay quiet when no actionable issue is found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic writes to private and shared memory can retain or share operational details without clear user control or retention limits.

Mitigation: Run the skill in a controlled environment and make memory writes explicit, append-only, sanitized, and approved before sharing.

Risk: Deep status and log inspection can expose sensitive operational details if the environment includes secrets or private diagnostics.

Mitigation: Restrict inspection to non-secret health baselines and review outputs before persistent storage or distribution.

## Reference(s):

- [System Inspection ClawHub release](https://clawhub.ai/1yihui/skills/system-inspection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status lines with conclusion, cause, and recommendation fields, or NO_REPLY when there is no actionable finding.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact directs the agent to write inspection summaries to private and shared memory files after each run.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
