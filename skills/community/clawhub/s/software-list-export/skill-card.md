## Description:

Export installed software to CSV with versions and likely download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auto-dog](https://clawhub.ai/user/auto-dog)

### License/Terms of Use:

MIT-0

## Use Case:

Users preparing to migrate, reinstall, or audit a computer use this skill to create a reviewable inventory of installed applications, versions, likely reinstall locations, and uncertainty notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated software inventory can reveal workplace tools, security products, and personal usage patterns.

Mitigation: Review the CSV before sharing it and remove sensitive entries that are not needed for migration or reinstall planning.

Risk: Likely download URLs may be vendor or product pages rather than confirmed installer links.

Mitigation: Treat unconfirmed URLs as starting points and verify download sources before reinstalling software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/auto-dog/skills/software-list-export)

## Skill Output:

**Output Type(s):** [text, shell commands, CSV, guidance]

**Output Format:** [CSV file with a brief text status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV columns: name, version, download_url, comments.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
