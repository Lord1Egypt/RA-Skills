## Description:

Handles messages in a Discord sleep-tracking channel by using the tracker and source Discord metadata to add, correct, delete, and render sleep log entries without invented timestamps or entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdmichaelb](https://clawhub.ai/user/cdmichaelb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents operating a dedicated Discord sleep channel use this skill to log sleep events, correct or delete the latest entry, and render a file-grounded sleep summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sleep logs may contain personal sleep history and Discord metadata.

Mitigation: Install only in a dedicated sleep-tracking channel, set WORKSPACE to a directory intended for this data, and treat generated files as sensitive.

Risk: Deleted entries may remain in the CSV with a deleted status.

Mitigation: Account for this retention behavior when handling access, export, or deletion expectations.

Risk: CSV values from untrusted channel messages may be unsafe to open directly in formula-capable spreadsheets.

Mitigation: Sanitize cells or disable formulas before opening exported CSV data in spreadsheet software.

## Reference(s):

- [Sleep Channel Rules](references/CHANNEL_RULES.md)
- [Sleep Tracking System](references/README.md)
- [ClawHub Skill Page](https://clawhub.ai/cdmichaelb/skills/sleep-channel)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON confirmations and Markdown sleep-log summaries with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses source Discord metadata and the configured local timezone for logged entries.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
