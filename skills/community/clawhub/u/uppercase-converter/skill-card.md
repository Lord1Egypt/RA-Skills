## Description:

Converts English lowercase letters to uppercase using a bundled Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jennyli2022](https://clawhub.ai/user/jennyli2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and end users use this skill to convert supplied text or piped file contents to ASCII uppercase while leaving digits, punctuation, whitespace, and non-English characters unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-requested file rewrites can overwrite existing content if converted output is written back to the same path.

Mitigation: Confirm the intended file change before writing back; otherwise return stdout or write to a new file.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text result, with Markdown guidance when command usage is shown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Only ASCII a-z letters are converted; other characters pass through unchanged.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
