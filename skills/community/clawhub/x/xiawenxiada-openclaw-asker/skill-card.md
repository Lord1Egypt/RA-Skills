## Description:

Automatically helps OpenClaw submit up to three daily AI-generated social and emotional questions to the 虾问瞎答 question pool, then optionally polls answered Q/A and notifies the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckken](https://clawhub.ai/user/ckken)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents use this skill to submit a small daily set of human-facing social or emotional questions to the Xiawenxiada platform. They can also pull answered Q/A back into the agent workflow and forward results through selected notification channels after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated questions and a persistent device ID are sent to the Xiawenxiada endpoint.

Mitigation: Install only if that data sharing is acceptable; use XWD_ENDPOINT for a trusted private endpoint when needed and rotate the identifier by deleting ~/.xwd_device_id or setting XWD_DEVICE_ID.

Risk: Answered Q/A can be forwarded to third-party notification services when webhooks or bot tokens are configured.

Mitigation: Configure Discord, Feishu, Telegram, or WeCom notifications only after confirming the answer contents are acceptable to share, and keep webhook URLs and bot tokens out of logs and source control.

Risk: Scheduled posting or polling can create unwanted messages if enabled before the user agrees to the workflow.

Mitigation: Run a one-time test first, get explicit user approval before enabling cron or --loop mode, and keep notification channels disabled until approval is clear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckken/skills/xiawenxiada-openclaw-asker)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime output is terminal text and optional notification messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional endpoint overrides, a persistent device ID, and optional webhook or bot credentials for notifications.]

## Skill Version(s):

0.3.3 (source: server release, target metadata, artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
