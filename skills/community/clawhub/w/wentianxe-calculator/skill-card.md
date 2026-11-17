## Description:

Perform mathematical calculations and unit conversions. Use when the user needs to calculate expressions, convert units (length, mass, temperature, volume, area, time), or solve math problems. Supports basic arithmetic (+, -, *, /, %, ^), scientific functions (sin, cos, tan, log, sqrt, etc.), and common unit conversions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wushengbing](https://clawhub.ai/user/wushengbing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to calculate arithmetic or scientific expressions and convert common units for length, mass, volume, area, time, and temperature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Very large expressions could consume local CPU or memory.

Mitigation: Use expression length, complexity, numeric magnitude, timeout, and memory limits before exposing the skill to untrusted users or public automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wushengbing/skills/wentianxe-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; calculator script commands output JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calculator responses include result, category, or error fields when using the bundled command-line script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
