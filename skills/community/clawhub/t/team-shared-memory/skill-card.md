## Description:

Team Shared Memory synchronizes shared memory across multiple agent workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amd5](https://clawhub.ai/user/amd5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw agents use this skill to synchronize shared project and reference memory between local workspaces while keeping user and feedback memory private.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent team memory may be writable by other users, workspaces, or agents, and sync operations move files without strong approval boundaries.

Mitigation: Use only trusted local memory directories with restrictive filesystem permissions, run under an unprivileged account, and manually review shared Markdown before relying on it.

Risk: The advertised secret scan should not be relied on to protect synchronization operations.

Mitigation: Review memory content before sharing and treat secret scanning as advisory until enforced scanning and approval or quarantine controls are available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amd5/skills/team-shared-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance for local memory synchronization workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=18.0.0 and local access to OpenClaw memory directories.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
