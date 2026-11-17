## Description:

Generate random numbers, passwords, and strings with configurable length and character sets. Use for security tokens, testing data, and randomization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can use this skill to generate random integers, floats, strings, UUIDs, choices, shuffled text, and passwords for testing data, demos, and lightweight randomization tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that password, token, key, reset-link, or session-identifier outputs should not be treated as cryptographically secure.

Mitigation: Limit current use to testing, demos, simple random choices, and shuffling unless the implementation is changed to use a cryptographically secure source such as Python's secrets module and the documentation is corrected.

Risk: The skill advertises security-token and secure-password use while the security verdict is suspicious.

Mitigation: Review the skill before installation for any security-sensitive workflow and avoid relying on generated security credentials until the risk is remediated.

## Reference(s):

- [Random Tool ClawHub skill page](https://clawhub.ai/dinghaibin/skills/random-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text values and Markdown with inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Random values may include integers, floats, strings, UUIDs, choices, shuffled lines, or passwords depending on selected options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
