## Description:

Helps agents manage Tencent Cloud resources through tccli, including CVM, Lighthouse, CBS, VPC, DNSPod, SSL, CAM, Monitor, TAT, and Domain workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cocofhu](https://clawhub.ai/user/cocofhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect and manage Tencent Cloud resources, deploy Lighthouse applications, mount cloud disks, run security and health checks, and configure DNS, SSL, CAM, and monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage live Tencent Cloud resources and therefore may affect production infrastructure or billing.

Mitigation: Install only when Tencent Cloud management is expected, use a least-privilege cloud account, and require explicit confirmation for purchases, DNS changes, disk formatting, remote commands, and deletes.

Risk: Credential material such as OAuth codes, SecretKeys, personal access tokens, passwords, or tccli credential files could be exposed during setup or operation.

Mitigation: Avoid sending secrets through chat, prefer temporary OAuth credentials, restrict permissions on ~/.tccli credential files, and rotate credentials used with insecure flows.

Risk: Deployment flows may involve installers, images, SSH access, and host configuration steps that need operator review.

Mitigation: Prefer pinned installers and images, use SSH keys with host-key verification, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cocofhu/skills/tencentcloud-management-tool)
- [Tencent Cloud API documentation](https://cloud.tencent.com/document/api)
- [TCCLI documentation](https://cloud.tencent.com/document/product/440)
- [CAM permission documentation](https://cloud.tencent.com/document/product/598)
- [CloudAudit documentation](https://cloud.tencent.com/document/product/629)
- [auto-check-resource.md](references/auto-check-resource.md)
- [cbs-bindto-cvm.md](references/cbs-bindto-cvm.md)
- [cloud-service-healthcheck.md](references/cloud-service-healthcheck.md)
- [cvm-security-check.md](references/cvm-security-check.md)
- [lighthouse-app-deploy.md](references/lighthouse-app-deploy.md)
- [lighthouse-openclaw-setup.md](references/lighthouse-openclaw-setup.md)
- [lighthouse-website-setup.md](references/lighthouse-website-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute tccli workflows that affect live Tencent Cloud resources; purchases, DNS changes, disk formatting, remote commands, and deletes require explicit user confirmation.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
