## Description:

Tencent Cloud Infra helps agents inspect and manage Tencent Cloud infrastructure through tccli, including Lighthouse, CVM, CBS, VPC, DNS, SSL, CAM, Monitor, TAT, Domain, and CloudAudit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cocofhu](https://clawhub.ai/user/cocofhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and cloud administrators use this skill to query Tencent Cloud resources, configure tccli access, perform security and health checks, deploy applications to Lighthouse, and manage cloud disks and related infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad Tencent Cloud administration, including operations that affect live infrastructure.

Mitigation: Use a least-privilege Tencent Cloud subaccount and confirm write, stop, reset, delete, or deployment actions before execution.

Risk: Cloud credentials, OAuth authorization codes, AK/SK secrets, root passwords, and Git tokens may be exposed if shared in chat or command lines.

Mitigation: Prefer the temporary OAuth flow, avoid pasting secrets into chat or shell history, and rotate or revoke credentials after use when exposure is possible.

Risk: Deployment workflows may use root SSH access, password resets, remote command execution, or installer scripts.

Mitigation: Review privileged commands before running them, keep SSH host-key checking enabled, and avoid disabling security checks for convenience.

## Reference(s):

- [Tencent Cloud API documentation](https://cloud.tencent.com/document/api)
- [TCCLI documentation](https://cloud.tencent.com/document/product/440)
- [CAM permissions documentation](https://cloud.tencent.com/document/product/598)
- [CloudAudit documentation](https://cloud.tencent.com/document/product/629)
- [Cloud resource automated checks](references/auto-check-resource.md)
- [Buy and attach CBS cloud disks](references/cbs-bindto-cvm.md)
- [Cloud service health diagnostics](references/cloud-service-healthcheck.md)
- [CVM security checks](references/cvm-security-check.md)
- [Lighthouse application deployment guide](references/lighthouse-app-deploy.md)
- [Lighthouse OpenClaw deployment guide](references/lighthouse-openclaw-setup.md)
- [Lighthouse website setup guide](references/lighthouse-website-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tccli commands, SSH commands, cloud resource analysis, and step-by-step runbooks.]

## Skill Version(s):

1.0.10 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
