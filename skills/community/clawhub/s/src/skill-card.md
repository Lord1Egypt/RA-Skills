## Description:

Bridge macOS-only tools into a Linux OpenClaw gateway via SSH wrappers and connected Mac nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when a Linux OpenClaw gateway needs a repeatable SSH-wrapper path to tools that must run on connected Mac nodes, such as imsg, remindctl, memo, things, peekaboo, brew-backed CLIs, or other macOS-local binaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer inputs or target Mac details could cause unsafe wrapper generation or command execution if they are malicious or insufficiently trusted.

Mitigation: Install only when the target Mac and installer inputs are trusted, inspect generated wrappers before use, and keep wrappers narrow to a single intended tool.

Risk: Broad SSH access can expand the blast radius of a compromised gateway or Mac node.

Mitigation: Use dedicated non-root SSH accounts, scoped SSH keys, known-hosts pinning where feasible, and one wrapper per tool rather than a general shell bridge.

Risk: Generated wrappers can persist after the original need has passed.

Mitigation: Track who installed or rotated wrappers, document the owning node and rollback command, and remove wrappers or revoke keys that are no longer needed.

## Reference(s):

- [Security Model](artifact/references/security-model.md)
- [Publish Pattern](artifact/references/publish-pattern.md)
- [ClawHub Skill Page](https://clawhub.ai/matthewxmurphy/skills/src)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash command examples, wrapper script paths, and configuration conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installer scripts can create executable SSH wrapper files on the Linux gateway when run by the user.]

## Skill Version(s):

0.6.1 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
