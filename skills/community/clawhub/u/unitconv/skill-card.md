## Description:

Convert units for length, weight, temperature, data, and speed. Use when switching measurement systems, sizing storage, or adjusting recipe quantities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other users use Unitconv to convert common measurement units from the command line for sizing, recipes, storage, speed, temperature, and time calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted conversion values may run local shell commands through AWK when inputs come from untrusted users or automated workflows.

Mitigation: Do not install this version in untrusted-input workflows; validate numeric values and pass data to AWK with -v or fixed calculation functions before routine use.

## Reference(s):

- [Unitconv ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/unitconv)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Numeric conversion results with unit labels.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
