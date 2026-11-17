## Description:

Convert times across world timezones and compare availability. Use when converting meetings, checking offsets, comparing zones, generating tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can ask an agent for timezone-related command-line actions such as conversions, comparisons, exports, and local status checks. Security evidence notes that the executable mainly logs arbitrary user input locally rather than performing full timezone conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as a timezone converter, but its executable behavior is mainly a local logger for arbitrary user input.

Mitigation: Review generated commands before installing or running the skill, and verify timezone outputs independently when accuracy matters.

Risk: Meeting details, names, locations, or business context entered into the tool may be saved under ~/.local/share/timezone and later searched or exported.

Mitigation: Avoid entering confidential information unless local history storage is acceptable, and clear the local data directory when retained history is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/timezone)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local CLI actions that write history files under ~/.local/share/timezone.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
