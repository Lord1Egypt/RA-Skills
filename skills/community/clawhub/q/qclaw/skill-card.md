## Description:

Summarize noisy WeChat group chats into decisions, action items, mentions, risks, and tracked keywords for OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use QClaw to turn busy WeChat group transcripts into concise summaries, confirmed decisions, action items, keyword hits, mentions, and risk signals for OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided chat logs may contain private business or personal information.

Mitigation: Redact sensitive names, credentials, financial details, and confidential client content before using the skill when possible.

Risk: Summaries may omit nuance or mark uncertain facts incorrectly when the transcript lacks context.

Mitigation: Review decisions, action items, mentions, and risk labels against the source chat before acting on them.

## Reference(s):

- [QClaw on ClawHub](https://clawhub.ai/projectsnowwork/skills/qclaw)
- [README](artifact/README.md)
- [Examples](artifact/examples.md)
- [System Prompt Template](artifact/prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown sections with concise bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include uncertainty markers, action-item checkboxes, urgency labels, and risk status labels.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
