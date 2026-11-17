## Description:

Run TikTok Business account operations from cron for inbound DM and comment replies, with quotas, phase gates, and stop-on-block controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use this skill to schedule controlled TikTok Business account reply workflows for one account they own. It supports inbound DM and comment handling, local recaps, quota checks, stop conditions, and configuration guidance for browser-based operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires terminal Accessibility control and a logged-in TikTok browser profile.

Mitigation: Use a dedicated low-privilege browser or user session, grant access deliberately, and revoke it when account operations are not running.

Risk: Optional webhook alerts can send account handles, counts, and lead usernames outside the local machine.

Mitigation: Leave the webhook unset by default, and only enable it for channels limited to authorized operators.

Risk: TikTok challenges, account warnings, or rate limits indicate that the platform has applied a control.

Mitigation: Stop the run, avoid retries or workarounds, alert a human operator, and resume only after manual review.

Risk: Local operation logs include usernames, timestamps, and account activity summaries.

Mitigation: Keep logs in the configured workspace, avoid storing DM bodies or personal details, monitor local logs, and prune identifier-bearing logs on the documented retention schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/skills/tiktok-account-operations)
- [ClawHub metadata homepage](https://clawhub.ai/skills/tiktok-account-operations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local recap formats, operational checklists, quota guidance, and stop-condition handling instructions.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
