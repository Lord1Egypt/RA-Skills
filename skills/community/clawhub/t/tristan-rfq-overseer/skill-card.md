## Description:

Use this skill to run an end-to-end RFQ (Request for Quotation) pipeline for a procurement/sourcing operation: intake from email or Telegram, Obsidian-vault storage, pricing calculation, supplier quote comparison, and confirmed-send drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yrc96](https://clawhub.ai/user/yrc96)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and sourcing operators use this skill to capture RFQs, store their status in an Obsidian vault, calculate pricing, compare supplier quotes, and draft client quotations that require explicit confirmation before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram commands can expose or change sensitive procurement records without documented sender controls.

Mitigation: Use only with a private Telegram bot or chat and enforce sender and chat allowlists outside the skill.

Risk: The skill can read or update procurement records in an Obsidian vault.

Mitigation: Constrain Obsidian access to the intended RFQ, Certs, and Quotes folders and dry-run pricing or quote changes before enabling write-back.

Risk: Incorrect or unreviewed quote details could be sent to a client.

Mitigation: Keep outbound quotation emails staged until the account owner gives explicit confirmation in the live sending channel.

## Reference(s):

- [Vault Schema](references/vault-schema.md)
- [Telegram Conventions](references/telegram-conventions.md)
- [Email Conventions](references/email-conventions.md)
- [ClawHub Skill Page](https://clawhub.ai/yrc96/skills/tristan-rfq-overseer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, JSON script output, and markdown tables or draft quotation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update Obsidian RFQ notes when write flags are used; email delivery is intended only after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
