## Description:

Provides OpenClaw cost-reference guidance, budget-alert suggestions, and model-spending optimization tips for token usage reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redwoo](https://clawhub.ai/user/redwoo)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to review token-cost patterns, set budget guidance, and identify model-routing or context-management changes that may reduce API spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate active monitoring, alerting, and budget-control capabilities.

Mitigation: Treat outputs as guidance and verify actual usage, alerting, and enforcement through OpenClaw session data or separate budget controls.

Risk: Optional Slack and email alert examples could disclose cost data if run with real endpoints or unsanitized values.

Mitigation: Run external alert examples only with explicit user intent, approved destinations, and sanitized cost summaries.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [Token Cost Monitor on ClawHub](https://clawhub.ai/redwoo/skills/token-cost-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local cost-reference output from a shell script; does not provide live enforcement of budget limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
