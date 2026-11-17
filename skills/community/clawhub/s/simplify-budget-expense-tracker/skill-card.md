## Description:

Simplify Budget Expense Tracker lets agents log, find, update, and delete expenses, income, subscriptions, and recurring items in a Simplify Budget Google Sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serdarsalim](https://clawhub.ai/user/serdarsalim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance agents use this skill to maintain a Simplify Budget Google Sheet through conversational expense, income, subscription, and recurring-payment workflows. It is intended for users who have copied the required sheet template and configured Google Sheets service-account access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill can write financial data in unsafe or under-disclosed ways.

Mitigation: Review before installing, test against a copied sheet, and require user confirmation before write operations.

Risk: The default command wrapper contains a fallback SPREADSHEET_ID, which could direct writes to an unintended sheet if not overridden.

Mitigation: Set SPREADSHEET_ID explicitly to the user's own copied Simplify Budget sheet before use.

Risk: The skill uses a Google service account with spreadsheet edit access.

Mitigation: Limit the service account to the copied budget sheet and avoid granting broader Drive or account permissions.

Risk: Untrusted transaction text may be unsafe until formula handling is fixed.

Mitigation: Avoid accepting untrusted transaction text and review logged values before deployment.

Risk: The package includes an unrelated session-pruning utility that archives OpenClaw Telegram sessions.

Mitigation: Remove or ignore the session-pruning script unless that archival behavior is intentionally needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/serdarsalim/skills/simplify-budget-expense-tracker)
- [Simplify Budget Template](https://docs.google.com/spreadsheets/d/1fA8lHlDC8bZKVHSWSGEGkXHNmVylqF0Ef2imI_2jkZ8/edit?gid=524897973#gid=524897973)
- [Simplify Budget Web UI](https://simplifybudget.com/)
- [README](artifact/README.md)
- [Setup Guide](artifact/SETUP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational text with command-backed budget results and inline shell command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Google Sheets as the source of truth and requires GOOGLE_SA_FILE, SPREADSHEET_ID, and TRACKER_CURRENCY at runtime.]

## Skill Version(s):

1.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
