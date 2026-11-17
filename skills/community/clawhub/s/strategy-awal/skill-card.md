## Description:

OpenClaw MVP v8.1 for email classification and Google Workspace execution for Awalcom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strategy-awal](https://clawhub.ai/user/strategy-awal)

### License/Terms of Use:

MIT-0

## Use Case:

Awalcom strategy teams and their OpenClaw operator use this skill to check a strategy inbox, classify emails by Oman, Qatar, or MENA context, and prepare approved Google Workspace drafts, slides, or sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google OAuth setup may include unrelated Calendar and Contacts access.

Mitigation: Use the narrowest OAuth scopes needed for Gmail, Drive, Docs, Sheets, and Slides, and remove Calendar and Contacts from the reauthorization command unless separately justified.

Risk: Sensitive strategy emails may be copied into Telegram summaries or shared Google Workspace assets.

Mitigation: Keep Telegram channels private and require explicit confirmation before copying email content into any shared document, sheet, or slide deck.

Risk: Keyword-based regional classification can be ambiguous or incorrect.

Mitigation: Ask for clarification on ambiguous emails and review generated Workspace assets before sharing, finalizing, or using them for external communication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/strategy-awal/skills/strategy-awal)
- [Publisher Profile](https://clawhub.ai/user/strategy-awal)
- [README](artifact/README.md)
- [Approval Workflow](artifact/docs/approval-workflow.md)
- [Telegram Commands](artifact/docs/telegram-commands.md)
- [Troubleshooting](artifact/docs/troubleshooting.md)
- [Email Classification Keywords](artifact/context/email-classification-keywords.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown, text summaries, command-oriented guidance, and links to generated Google Workspace assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured gog and gh command-line tools, Google Workspace OAuth, and Telegram approval before external actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
