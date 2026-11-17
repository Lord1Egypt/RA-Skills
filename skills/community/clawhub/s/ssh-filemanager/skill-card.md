## Description:

Manage files on remote OpenClaw nodes over Tailscale SSH, including listing, reading, writing, deleting, moving, copying, searching, chmod, and file transfer operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xeon0v0](https://clawhub.ai/user/xeon0v0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage files on remote OpenClaw nodes reachable through Tailscale SSH, including inspecting metadata, transferring files, and applying file changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad remote file changes over SSH, including overwrites, chmod, moves, copies, and recursive deletes.

Mitigation: Use it only in trusted Tailnet environments, require explicit confirmation for destructive operations, and apply least-privilege SSH and ACL access.

Risk: Weak host, path, and mode safeguards can make untrusted hostnames, paths, modes, or prompts unsafe.

Mitigation: Validate the target host, absolute paths, chmod modes, and requested operation before execution; avoid untrusted prompts until stronger validation is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xeon0v0/skills/ssh-filemanager)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use existing SSH access to read, overwrite, chmod, copy, move, and recursively delete remote files; destructive actions require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
