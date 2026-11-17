## Description:

SSH Deploy Skill helps agents manage Linux servers over SSH with inventory management, batch command execution, file transfers, and templated software installation scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awamwang](https://clawhub.ai/user/awamwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to configure SSH server inventories, execute commands across one or more Linux servers, transfer files, and apply reusable installation templates for common infrastructure software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run commands, upload files, and change repositories or services on remote servers with high privileges.

Mitigation: Review generated commands and templates before execution, test on a single non-production host first, and use least-privilege deploy users instead of root where possible.

Risk: Default SSH behavior can expose sessions when host keys are accepted automatically.

Mitigation: Use --strict for host-key verification and maintain known_hosts entries for managed servers.

Risk: Inventory files or environment setup may expose credentials if passwords are stored directly.

Mitigation: Use SSH keys, avoid password entries in inventory.json, and pass secrets through environment variables or a dedicated secret manager.

Risk: Installer templates may rely on mutable network sources or unpinned package installs.

Mitigation: Pin dependency versions and replace curl-to-bash or remote installer steps with verified, trusted package sources for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awamwang/skills/ssh-deploy-skill)
- [README](artifact/README.md)
- [Best Practices](artifact/references/best-practices.md)
- [Mirror Configuration](artifact/references/mirrors.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated configuration or script snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, ssh, scp, and the paramiko Python package; outputs may target inventory.json entries or hosts from ~/.ssh/config.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
