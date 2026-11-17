## Description:

Timezone Toolkit converts times between timezones, shows world clocks, finds meeting overlap across zones, and looks up UTC offsets and DST status using Python's built-in zoneinfo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run local timezone conversions, compare world clocks, plan meetings across zones, and inspect UTC offsets or DST status without external dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timezone abbreviations such as EST or PST are mapped to regional IANA zones, so date-specific daylight saving behavior can affect conversion results.

Mitigation: Use full IANA timezone names and include explicit dates for time-sensitive conversions.

## Reference(s):

- [Timezone Toolkit on ClawHub](https://clawhub.ai/johnnywang2001/skills/timezone-toolkit)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local CLI output only; no network, credential, persistence, or destructive behavior identified in server security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
