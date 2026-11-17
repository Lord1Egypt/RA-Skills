## Description:

Converts common units for length, weight, temperature, speed, storage, area, and volume using local calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyhuya](https://clawhub.ai/user/tonyhuya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill for quick local unit conversions across everyday measurement categories without network access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation may imply broad Chinese unit-name input support, while the security evidence notes most unit inputs require abbreviations such as km, kg, or gb.

Mitigation: Use the documented abbreviations for non-temperature conversions and verify unfamiliar conversions with a trusted source.

Risk: The skill invokes a local shell script and python3 to calculate results.

Mitigation: Review the packaged script before installation and run it in a local environment where python3 is expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonyhuya/skills/unit-converter)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with python3; no network access or credential use is indicated by the security evidence.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
