## Description:

Provides monthly, zone-specific planting schedules, plant details, and custom entries to help gardeners plan seasonal crops year-round.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johstracke](https://clawhub.ai/user/johstracke)

### License/Terms of Use:


## Use Case:

External gardeners, small farmers, and garden planners use this skill to get USDA zone-specific monthly planting calendars, look up plant details, search crops, add custom entries, and export markdown schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar export can overwrite broad home or temporary-directory paths despite stronger safety claims.

Mitigation: Use --export only with a dedicated new file under ~/.openclaw/workspace/ and avoid important existing files, dotfiles, or broad home-directory paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Command-line text output and optional Markdown export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local planting database for custom entries and can export planting calendars as Markdown.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
