## Description:

Provides a Tencent Cloud CLI reference for installing, configuring, and using TCCLI to manage Tencent Cloud services from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxhoio](https://clawhub.ai/user/sxhoio)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to install and configure TCCLI, look up common Tencent Cloud commands, and manage resources such as compute instances, networking, DNS, SSL certificates, monitoring, and databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud CLI commands can change or disrupt Tencent Cloud resources when run with privileged credentials.

Mitigation: Use least-privileged Tencent Cloud credentials and review resource IDs, regions, domains, firewall rules, and certificate targets before executing state-changing commands.

Risk: Credential setup examples involve Tencent Cloud secret IDs and keys that could be exposed on shared machines.

Mitigation: Configure credentials only in trusted environments and avoid entering or storing secrets on shared systems.

## Reference(s):

- [TCCLI Official Documentation](https://cloud.tencent.com/document/product/440/34011)
- [TencentCloud/tencentcloud-cli GitHub Repository](https://github.com/TencentCloud/tencentcloud-cli)
- [ClawHub Skill Page](https://clawhub.ai/sxhoio/skills/tccli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and lookup tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, credential configuration, output formatting, help commands, and service-specific command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
