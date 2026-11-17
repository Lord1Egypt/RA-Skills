## Description:

Writes Classical Chinese (文言文) git commit messages from the current git diff when the user explicitly requests that style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xing-lin](https://clawhub.ai/user/xing-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn staged or unstaged git diffs into a succinct Classical Chinese commit subject and optional body when they explicitly request that style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads staged or unstaged git diffs, which may contain secrets or sensitive code.

Mitigation: Review or redact sensitive diff content before invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xing-lin/skills/wenyan-commit-message-skill)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text commit message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subject line is capped at 50 Chinese characters; optional body lines are capped at 72 characters.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
