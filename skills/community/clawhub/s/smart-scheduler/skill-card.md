## Description:

Coordinate meeting requests, proposed time slots, confirmations, and ICS exports from a local scheduling ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehulupase01](https://clawhub.ai/user/mehulupase01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to coordinate scheduling requests, record candidate meeting times, confirm agreed slots, and export calendar files from a local ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar export can write to arbitrary local paths and overwrite writable files.

Mitigation: Keep exports under the skill's .runtime directory and review output paths before running export commands.

Risk: Scheduling text can contain ambiguous or untrusted meeting details.

Mitigation: Confirm participant acceptance explicitly, preserve provided time zones, and present unresolved options instead of inventing agreement.

## Reference(s):

- [Message Templates](references/message-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/mehulupase01/skills/smart-scheduler)
- [Project Homepage](https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/smart-scheduler)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with shell commands; helper commands emit JSON and can write ICS calendar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite ledger under .runtime by default; ICS export paths should be reviewed before writing.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
