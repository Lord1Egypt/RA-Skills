## Description:

Convert Windows paths to WSL paths for file operations in WSL environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiqihan](https://clawhub.ai/user/weiqihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to translate user-provided Windows paths into WSL-compatible `/mnt/<drive>/...` paths for file access, project work, image handling, and other resource operations inside WSL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make it easier for an agent to operate on files under Windows-mounted drives.

Mitigation: Only provide paths for files and folders that the agent is allowed to access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weiqihan/skills/wsl-path-converter)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown or plain text path conversion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WSL path equivalents for user-provided Windows paths; no code execution is included in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
