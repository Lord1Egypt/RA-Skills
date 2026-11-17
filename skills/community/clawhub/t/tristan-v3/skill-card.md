## Description:

Runs an end-to-end RFQ pipeline for procurement and sourcing operations, covering intake from email or Telegram, Obsidian vault storage, pricing calculation, supplier quote comparison, and confirmed-send drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yrc96](https://clawhub.ai/user/yrc96)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and sourcing operators use this skill to manage RFQ intake, note creation, pricing, supplier comparison, and draft quotation preparation across email, Telegram, and an Obsidian vault. It is intended for workflows where a human reviews pricing and supplier outputs before any external quotation is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pricing, supplier rankings, or RFQ drafts could affect business decisions if accepted without review.

Mitigation: Manually review generated prices, supplier rankings, and draft emails before relying on them operationally or sharing them externally.

Risk: Connecting the wrong vault, email account, or Telegram channel could expose or modify unintended business data.

Mitigation: Install only after configuring the intended Obsidian vault, Telegram channel, and email account, and keep channel access limited to the RFQ workflow.

Risk: An outbound quotation could be sent before the user has approved the final draft.

Mitigation: Keep explicit send confirmation enabled and require a fresh confirmation when a draft changes after review.

Risk: Publishing or validation behavior may vary if dependency versions drift.

Mitigation: Use pinned dependencies or an isolated environment for publishing and validation tools.

## Reference(s):

- [Vault Schema](artifact/references/vault-schema.md)
- [Telegram Conventions](artifact/references/telegram-conventions.md)
- [Email Conventions](artifact/references/email-conventions.md)
- [ClawHub Release Page](https://clawhub.ai/yrc96/skills/tristan-v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write pricing and quote-comparison results into Obsidian markdown notes when the bundled scripts are run with write options.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
