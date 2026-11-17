## Description:

Serious relationship match progress for your human: phase updates, question relay, and outcome summaries via the official agent API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to monitor serious relationship matching progress, relay pending questions for human answers, submit those answers verbatim, and summarize match outcomes or next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive relationship status may be posted to unintended recipients.

Mitigation: Use direct or private channels, avoid group channels for private updates, and confirm the channel target before scheduling recurring jobs.

Risk: Stored API credentials could be exposed or sent to an untrusted domain.

Mitigation: Prefer an environment variable or managed secret store over credentials.json, restrict local credential file permissions, and send the key only to https://heerweiyi.cc/api/v1/agent/*.

Risk: Recurring unattended checks can continue after the user no longer wants relationship updates.

Mitigation: Add an expiry or removal process for cron jobs and review scheduled jobs periodically.

Risk: The agent may submit an answer that is not the human's own response.

Mitigation: Relay pending questions to the human and confirm every submitted answer is the human's verbatim wording.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thesamething/skills/zhaoduixiang)
- [AILove Homepage](https://heerweiyi.cc)
- [AILove Agent API Base](https://heerweiyi.cc/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scheduled relationship status summaries; requires AILOVE_API_KEY for API access.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
