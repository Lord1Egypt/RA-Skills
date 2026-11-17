## Description:

Reply on Telegram with an HTML widget card (price, poll, checklist, chart, countdown) when an answer is better seen than read; checks it, then sends or updates it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happysean2845](https://clawhub.ai/user/happysean2845)

### License/Terms of Use:

MIT

## Use Case:

Agents communicating with a user in a private Telegram chat use the skill to present prices, poll results, checklists, charts, or countdowns as compact widget cards and update their displayed state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign scan verdict has medium confidence and is partial because one reference was unresolved.

Mitigation: Review the unresolved reference before relying on the scan result.

Risk: The scan reports network, file-write, environment-access, subprocess, and allowlist findings that it judged expected for this skill.

Mitigation: Review these behaviors before installation and keep bot credentials and link allowlist settings limited to intended use.

## Reference(s):

- [Telegram Widgets guide](https://core.telegram.org/bots/widgets.md)
- [Telegram widget rules (included)](artifact/references/widget-rules.md)
- [ClawHub release page](https://clawhub.ai/happysean2845/skills/telegram-widget-skill)

## Skill Output:

**Output Type(s):** [Code, JSON, Shell commands, API calls]

**Output Format:** [Telegram HTML widget documents with JSON state, plus CLI commands for validation, sending, and updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Widgets are for private Telegram chats. After sending, the HTML stays fixed while chat data and captions can be updated.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
