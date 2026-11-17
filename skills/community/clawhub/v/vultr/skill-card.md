## Description:

Vultr helps an agent manage Vultr cloud infrastructure including instances, bare metal, Kubernetes clusters, databases, DNS, firewalls, VPCs, storage, reserved IPs, billing, tickets, users, and startup scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happytreees](https://clawhub.ai/user/happytreees)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to list, deploy, and modify Vultr cloud resources through the Vultr API v2 using a local API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad account-changing actions in a Vultr account.

Mitigation: Use a least-privilege Vultr API key and review create, update, delete, reinstall, close, attach, detach, and key-regeneration commands before execution.

Risk: The skill can retrieve or handle sensitive material such as kubeconfig files, regenerated object-storage keys, account API keys, and user passwords.

Mitigation: Avoid saving sensitive outputs in shared workspaces, restrict file permissions, and treat command arguments and JSON responses as secrets when they contain credentials.

Risk: The security evidence reports no built-in confirmations or tight scoping.

Mitigation: Run commands only from clear, explicit prompts and avoid destructive operations from ambiguous requests.

## Reference(s):

- [Vultr API Reference](references/api-reference.md)
- [Vultr API v2 endpoint](https://api.vultr.com/v2)
- [Vultr API key settings](https://my.vultr.com/settings/#settingsapi)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a Vultr API key stored at ~/.config/vultr/api_key.]

## Skill Version(s):

1.3.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
