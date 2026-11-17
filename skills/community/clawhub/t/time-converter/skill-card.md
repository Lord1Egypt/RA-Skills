## Description:

Convert time between different timezones using IANA timezone database. Supports 12/24-hour formats, specific dates, and automatic DST handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and external users use this skill to convert times between IANA time zones for meeting planning, UTC normalization, and date-specific timezone comparisons with daylight-saving offsets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package documents a convert_time executable, but the security evidence says no bundled executable code is present.

Mitigation: Confirm the executable is supplied by the runtime environment before relying on the command examples.

Risk: Timezone planning can be wrong when daylight-saving status or date context is omitted.

Mitigation: Provide an explicit date and IANA timezone names for conversions that affect meetings or scheduling.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/time-converter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and timezone conversion text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversion results include source and target datetimes, timezone names, UTC offsets, and daylight-saving context when applicable.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
