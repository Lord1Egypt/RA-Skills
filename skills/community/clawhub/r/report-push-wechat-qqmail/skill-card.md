## Description:

Pushes an agent-generated report summary to WeChat-style notifications and the full report text to QQ Mail when the user explicitly requests report delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu99012101-bot](https://clawhub.ai/user/liu99012101-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to distribute completed analysis reports through two channels: a concise WeChat-style task summary and a full QQ Mail message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends report summaries to PushPlus and full report text through QQ Mail.

Mitigation: Use it only for reports that are appropriate for those third-party channels, and verify the recipient address before sending.

Risk: The security evidence states that the PushPlus token and report summaries are handled over plaintext HTTP.

Mitigation: Change the PushPlus endpoint to HTTPS and rotate any PushPlus token previously used with this version before deployment.

Risk: The security evidence identifies overly broad invocation wording.

Mitigation: Require explicit user confirmation before sending reports, especially when report contents are sensitive or externally sourced.

Risk: The security guidance calls out a script filename mismatch and dependency installation pinning issue.

Mitigation: Fix the script path referenced by the skill and pin dependency installation consistently before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liu99012101-bot/skills/report-push-wechat-qqmail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with a shell command invocation and JSON status interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The WeChat-style summary is constrained to 100 characters or fewer, while QQ Mail receives the full report text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
