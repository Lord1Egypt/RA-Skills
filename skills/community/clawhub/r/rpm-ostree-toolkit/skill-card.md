## Description:

Immutable OS management for Fedora Atomic / Bazzite — rpm-ostree layering, rollbacks, rebasing, and system upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silverod](https://clawhub.ai/user/silverod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and Linux power users use this skill to manage Fedora Atomic, Bazzite, Silverblue, and related rpm-ostree systems with package layering, upgrades, rollbacks, rebasing, cleanup, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact rpm-ostree commands can change deployments, kernel arguments, cleanup state, or trigger reboots.

Mitigation: Review each proposed command before execution and run only commands that match the user's update, recovery, or configuration goal.

Risk: Installing RPMs from URLs or rebasing to another image can introduce untrusted or incompatible system content.

Mitigation: Verify package and image sources, confirm branch and hardware compatibility, and keep a known-good deployment pinned when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silverod/skills/rpm-ostree-toolkit)
- [Publisher profile](https://clawhub.ai/user/silverod)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command guidance is intended for Linux systems with rpm-ostree and root or wheel privileges.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
