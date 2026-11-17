## Description:

Proxmox VE VM builder with cloud-init automation, config-driven hardware defaults, validation, and static IP support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbojer](https://clawhub.ai/user/mbojer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to assemble Proxmox VE VM creation commands, cloud-init user-data, SSH key setup, network settings, and optional data disk configuration for manual review and execution on a Proxmox node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shell commands could be incorrect or unsafe if user-provided VM names, paths, disk names, package names, URLs, or other inputs are not reviewed before execution.

Mitigation: Inspect every generated command before running it on a Proxmox host, and prefer a revised version that validates inputs and shell-quotes generated commands.

Risk: The skill handles and displays VM passwords, which can expose credentials or encourage password-based SSH access.

Mitigation: Do not reuse passwords with this skill, avoid password SSH where possible, and rotate or disable generated passwords after initial access.

Risk: Local configuration files, SSH key paths, and generated files may contain sensitive infrastructure details.

Mitigation: Keep pve-env.md and private keys permission-restricted, do not commit them, and verify generated file paths before saving or running commands.

## Reference(s):

- [Proxmox QM Command Reference](artifact/qm-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/mbojer/skills/pve-builder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style prompts and bash command blocks for manual execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally save generated commands to a user-selected file; outputs should be reviewed before execution.]

## Skill Version(s):

1.0.11 (source: server release metadata; artifact frontmatter lists 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
