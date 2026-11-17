## Description:

Convert Unix timestamps to dates and back for epoch parsing, time difference calculations, log debugging, and relative date generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Unixtime to inspect the current epoch time, convert between Unix timestamps and readable dates, calculate countdowns, and analyze durations between timestamps while debugging logs or planning time-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local shell script for timestamp conversion.

Mitigation: Review the script before installation and execute it only in an environment where local command execution is acceptable.

Risk: Date parsing and displayed local times can vary by operating system date utility, locale, and timezone.

Mitigation: Confirm important conversions against the intended host environment and prefer explicit UTC inputs for shared operational use.

## Reference(s):

- [Unixtime on ClawHub](https://clawhub.ai/bytesagain3/skills/unixtime)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text output and Markdown usage guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local command output depends on the host operating system date utility and timezone settings.]

## Skill Version(s):

3.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
