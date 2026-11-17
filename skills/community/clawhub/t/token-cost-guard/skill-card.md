## Description:

Token Cost Guard monitors OpenClaw or Hermes agent token usage and cost records, compares spending against prior snapshots or time windows, and generates or sends threshold alert reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor token spend across local OpenClaw or Hermes runtimes, detect spending spikes, and prepare threshold-based alert reports. It is suited for operational cost awareness where local runtime usage records are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect broad local OpenClaw or Hermes usage logs and runtime databases.

Mitigation: Enable it only in trusted workspaces, prefer explicit invocation, and restrict use to specific agents or runtime paths when possible.

Risk: Implicit invocation may run cost checks without a direct user command.

Mitigation: Disable or limit implicit invocation in environments where local usage records should only be read after explicit approval.

Risk: Alert delivery can expose cost and model usage details to external channels or unintended recipients.

Mitigation: Use --send-openclaw only with trusted channels and targets, and test delivery with dry-run or controlled recipients before scheduled use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/token-cost-guard)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional JSON summaries and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local state snapshots and report files under the selected runtime when invoked.]

## Skill Version(s):

0.2.4 (source: evidence.json release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
