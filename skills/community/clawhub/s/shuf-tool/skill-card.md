## Description:

Randomly shuffles lines of text input for random sampling, data randomization, and selection tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ClawHub users use this skill to have an agent shuffle line-oriented text, select random samples, or work with randomized ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Piped standard input may be handled as a pathname, which could print a file's contents instead of shuffling piped lines.

Mitigation: Avoid piping untrusted text into the helper until stdin handling is fixed; use explicit, reviewed files or controlled input.

Risk: The included helper is minimal and may not fully implement the options documented by the skill.

Mitigation: Test required command options in a controlled environment before relying on the shuffled output.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces shuffled line-oriented output; documented options should be tested before relying on them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
