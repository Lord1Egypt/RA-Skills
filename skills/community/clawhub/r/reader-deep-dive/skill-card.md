## Description:

Daily briefing that connects your recent reading to your long-term archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sameerbajaj](https://clawhub.ai/user/sameerbajaj)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate a daily or on-demand briefing that connects recent Readwise Reader saves with related items from their long-term archive and delivers the result through WhatsApp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readwise reading metadata and generated summaries are shared with Gemini and delivered through WhatsApp.

Mitigation: Use the skill only when that data sharing is acceptable for the account and reading content involved.

Risk: A misconfigured TARGET_NUMBER could send the briefing to an unintended recipient.

Mitigation: Set TARGET_NUMBER deliberately and run a manual test before enabling the scheduled cron job.

Risk: Malicious or misleading article metadata could influence the generated briefing.

Mitigation: Review briefings before relying on their conclusions, especially when recent saves or archive items come from untrusted sources.

## Reference(s):

- [Reader Deep Dive on ClawHub](https://clawhub.ai/sameerbajaj/skills/reader-deep-dive)
- [sameerbajaj ClawHub profile](https://clawhub.ai/user/sameerbajaj)
- [Readwise access token](https://readwise.io/access_token)
- [Readwise Reader API list endpoint](https://readwise.io/api/v3/list/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [WhatsApp-friendly Markdown-style text with setup and scheduling shell commands in the documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires READWISE_TOKEN and TARGET_NUMBER at runtime; generated briefings may include Readwise item URLs and are delivered through WhatsApp.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
