## Description:

Sandboxed command runner for AI agents that validates and isolates shell actions inside a Bubblewrap user namespace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[star8592](https://clawhub.ai/user/star8592)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route shell commands through a local Bubblewrap-backed safety layer before execution. It is intended for Linux environments where command isolation and logging are useful, with the security guidance reviewed before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The safety claims are overstated and the command-execution service is under-scoped.

Mitigation: Review before installing, run only in a narrow project directory, and avoid sensitive working directories.

Risk: The current release should not be relied on for validation, confirmation, loop limiting, or strict read-only isolation.

Mitigation: Prefer a release with pinned dependencies, workspace-bound writable mounts, authentication or strict socket permissions, and execution resource limits before relying on it for higher-risk workflows.

## Reference(s):

- [Homepage](https://coinwin.info)
- [ClawHub skill page](https://clawhub.ai/star8592/skills/skillshield-openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash examples and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux, Bubblewrap, cargo, curl, and python3 at runtime.]

## Skill Version(s):

2.1.8 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
