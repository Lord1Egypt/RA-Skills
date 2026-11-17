## Description:

Tracks user-provided receipt details, purchase prices, and warranty dates, and reports when coverage is nearing its end.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to maintain a local purchase ledger, check warranty status, and identify coverage dates that need attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt text, item names, prices, and warranty dates are stored in a local JSON ledger.

Mitigation: Avoid entering secrets or full payment details, and use a private state directory rather than a shared or synced folder unless intended.

Risk: Coverage reminders require running the reminder command; they are not automatically delivered.

Mitigation: Run the reminder command regularly and confirm warranty dates against the original receipt or warranty terms.

## Reference(s):

- [Receipt & Warranty Tracker on ClawHub](https://clawhub.ai/paradoxfuzzle/skills/receipt-warranty-tracker)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or structured JSON from the local command-line tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores receipt entries locally; warranty reminders are reported when the reminder command is run.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
