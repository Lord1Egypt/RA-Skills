## Description:

Manage registration records and attendee data for sign-ups, capacity checks, export conversion, and confirmation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this local terminal skill to record registration-related entries, inspect recent activity and simple statistics, and export stored records to JSON, CSV, or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist sensitive attendee inputs in local logs.

Mitigation: Avoid entering names, contact details, or other attendee information unless local retention is acceptable and the stored files are secured or deleted when no longer needed.

Risk: The security summary says the implementation does not match a complete registration-management purpose.

Mitigation: Review behavior before operational use and treat the artifact as a local activity logger with export utilities rather than a full registration manager.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/registration)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Terminal text with optional JSON, CSV, or plain-text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local activity records under ~/.local/share/registration.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
