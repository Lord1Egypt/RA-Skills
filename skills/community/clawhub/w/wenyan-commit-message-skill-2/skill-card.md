## Description:

Writes git commit messages in Classical Chinese when the user explicitly requests a wenyan, classical Chinese, ancient Chinese, or ornate commit-message style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xing-lin](https://clawhub.ai/user/xing-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn staged or unstaged git diffs into concise Classical Chinese commit messages, including an optional body when the change is complex.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads staged or unstaged git diffs, which may include sensitive material.

Mitigation: Avoid invoking it on changes containing secrets or other content you do not want included in agent context.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text commit message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subject line with optional body; intended for direct use as commit-message text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
