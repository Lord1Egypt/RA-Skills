## Description:

Detect and preserve human code edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill during repository edits to detect tracked or ignored human changes, load relevant changes into context, and preserve them before editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to commit after each series of edits, which may create commits before the user has reviewed them in sensitive or shared repositories.

Mitigation: Tell the agent whether commits require confirmation and ask it to show the diff and proposed commit message before committing.

Risk: The skill can cause ignored files to be loaded into agent context before editing, which may expose local or sensitive file contents if used broadly.

Mitigation: Use the skill only for repositories and files where the agent is allowed to inspect ignored content, and avoid applying it to secrets or private local configuration.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides workflow guidance for checking gitignored files, inspecting diffs, preserving human edits, and committing completed edit series.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
