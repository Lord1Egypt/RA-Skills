## Description:

Track subscriptions, alert before renewals, identify forgotten services, and calculate total spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kilusha](https://clawhub.ai/user/kilusha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-finance agents use this skill to record recurring subscriptions, review upcoming renewals, summarize spend by category, and manage local status changes such as paused or cancelled records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's cancel/remove wording can be mistaken for cancelling a real paid subscription with the provider.

Mitigation: Treat cancel/remove as a local record update only, and separately confirm cancellation with the subscription provider.

Risk: CSV exports may be opened in spreadsheet software with subscription names, notes, or URLs from untrusted text.

Mitigation: Review exported fields before opening CSV files in spreadsheets, especially if records include untrusted formulas or links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kilusha/skills/subscription-manager-pro)
- [Skill homepage](https://github.com/openclaw/skills/tree/main/skills/subscription-manager-pro)
- [Repository metadata](https://github.com/openclaw/skills.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown responses with CLI command examples and local JSON or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores subscription records locally under ~/.openclaw/workspace/subscription-manager-pro/data and can export records as CSV or JSON.]

## Skill Version(s):

1.0.0 (source: evidence release and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
