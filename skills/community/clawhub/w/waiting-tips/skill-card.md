## Description:

Shows bilingual learning tips while OpenClaw is thinking, with 75 tips covering AI interaction, prompt engineering, productivity, and wisdom across Telegram, Feishu, WhatsApp, and other platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to show short bilingual learning tips during AI response wait time or when a user asks for tips. It supports chat experiences across Telegram, Feishu/Lark, WhatsApp, Discord, Slack, and other OpenClaw-supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Telegram, Feishu, and WhatsApp bot examples use messaging credentials and local WhatsApp authentication state.

Mitigation: Treat bot tokens, app secrets, and local auth state as sensitive; keep them out of source control and pin dependencies when adapting examples.

Risk: Waiting tips are short educational prompts and may not match every organization's communication or AI-use policy.

Mitigation: Review and customize the text files in artifact/tips before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongsheng123132/skills/waiting-tips)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown-formatted bilingual tip messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional style and count parameters select emoji, card, Chinese-only, English-only, and one-to-five-tip outputs.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
