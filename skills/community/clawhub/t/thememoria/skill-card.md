## Description:

Use Memoria as OpenClaw's durable memory slot for explicit cross-session recall, storage, correction, deletion, snapshots, rollback, branching, and merge workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[randomradio](https://clawhub.ai/user/randomradio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure OpenClaw to use Memoria as a durable external memory system for project and user context. It guides explicit memory retrieval, storage, correction, deletion, recovery, branching, and maintenance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local embedded setup documents a curl-to-bash installer, which can execute remote code without independent verification.

Mitigation: Prefer the cloud plugin install path or use a pinned, signed, and checksum-verified release before running any installer.

Risk: Plugin and source install examples are not pinned to immutable versions or commits.

Mitigation: Install a pinned package version or clone and inspect a specific trusted commit before linking the plugin.

Risk: The skill uses API and embedding keys during setup.

Mitigation: Treat Memoria API keys and embedding keys as secrets, avoid storing them in durable memory, and rotate them if exposed.

Risk: Durable memory can preserve sensitive user or project context across sessions.

Mitigation: Store only intentional durable facts, avoid secrets unless explicitly required, and use correction, deletion, snapshots, rollback, and governance tools for maintenance.

## Reference(s):

- [Memoria homepage](https://github.com/matrixorigin/Memoria)
- [OpenClaw Setup](references/setup.md)
- [Tool Surface](references/tool-surface.md)
- [Memory Slot Operations](references/operations.md)
- [Usage Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline command examples and tool-selection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for choosing and using Memoria memory tools; it may also propose OpenClaw installation and setup commands.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
