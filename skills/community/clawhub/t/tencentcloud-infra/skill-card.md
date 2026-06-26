## Description: <br>
Guides agents through Tencent Cloud administration with tccli, covering resource discovery, security checks, Lighthouse and CVM operations, deployment workflows, storage, DNS, SSL, CAM, monitoring, and account login support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cocofhu](https://clawhub.ai/user/cocofhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect, configure, and administer Tencent Cloud resources through tccli with guided command selection and confirmation steps for risky actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help administer Tencent Cloud resources and may enable broad cloud-changing actions. <br>
Mitigation: Use a least-privilege subaccount and review every purchase, DNS change, firewall change, disk format, and root command before approval. <br>
Risk: The login flow may route sensitive OAuth codes or long-lived secrets through the assistant. <br>
Mitigation: Prefer temporary OAuth credentials, avoid sharing long-lived AK/SK secrets in chat, and clear or revoke ~/.tccli credentials when finished. <br>
Risk: Incorrect tccli parameters or outdated cloud-product assumptions can cause failed or unintended operations. <br>
Mitigation: Confirm current parameters with tccli --help and query resource state before executing modifying commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cocofhu/tencentcloud-infra) <br>
- [Tencent Cloud API Documentation](https://cloud.tencent.com/document/api) <br>
- [TCCLI Documentation](https://cloud.tencent.com/document/product/440) <br>
- [CAM Permissions Documentation](https://cloud.tencent.com/document/product/598) <br>
- [CloudAudit Documentation](https://cloud.tencent.com/document/product/629) <br>
- [Cloud Server Security Check](references/cvm-security-check.md) <br>
- [Automated Tencent Cloud Resource Inspection](references/auto-check-resource.md) <br>
- [Lighthouse Website Setup Guide](references/lighthouse-website-setup.md) <br>
- [Buy and Attach CBS Disk to Cloud Server](references/cbs-bindto-cvm.md) <br>
- [Deploy OpenClaw on Tencent Cloud Lighthouse](references/lighthouse-openclaw-setup.md) <br>
- [Tencent Cloud Lighthouse Application Deployment Guide](references/lighthouse-app-deploy.md) <br>
- [Cloud Service Health Diagnosis](references/cloud-service-healthcheck.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, checklists, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tccli commands, confirmation prompts, security findings, deployment steps, and credential-handling guidance.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
