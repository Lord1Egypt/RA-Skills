## Description:

Manage and track persistent project tasks with priorities, completion status, filtering, and markdown export across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johstracke](https://clawhub.ai/user/johstracke)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to maintain persistent task lists for multi-session projects, sprint planning, and progress reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown export may overwrite files in broad home-directory locations when an agent follows unsafe or untrusted instructions.

Mitigation: Review export paths before execution; prefer a dedicated exports directory and avoid overwriting existing files by default.

## Reference(s):

- [Task Runner ClawHub listing](https://clawhub.ai/johstracke/skills/task-runner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists task data in a JSON database under the user's OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
