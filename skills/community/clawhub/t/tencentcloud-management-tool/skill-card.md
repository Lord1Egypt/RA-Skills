## Description: <br>
Guides agents in managing Tencent Cloud resources with tccli, including CVM, Lighthouse, CBS, VPC, DNSPod, SSL, CAM, Monitor, TAT, and domain workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cocofhu](https://clawhub.ai/user/cocofhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and cloud administrators use this skill to query, configure, inspect, and deploy Tencent Cloud resources through tccli-assisted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to pass Tencent Cloud login token material through the agent and stores tccli credentials under the user's home directory. <br>
Mitigation: Treat OAuth codes and tccli credential files as secrets, prefer least-privilege temporary credentials, and avoid sending login codes through chat when another secure path is available. <br>
Risk: The skill covers high-impact cloud workflows such as paid resource creation, DNS changes, disk operations, and remote root commands. <br>
Mitigation: Confirm every paid, destructive, DNS, disk-formatting, or root remote command before execution, and prefer read-only Describe or help commands before changing resources. <br>
Risk: The authoritative security review describes the release as purpose-aligned but under-scoped for several high-impact cloud and credential-handling workflows. <br>
Mitigation: Install only when the agent is intended to manage Tencent Cloud resources, review helper scripts before use, and constrain credentials to the minimum permissions needed for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cocofhu/tencentcloud-management-tool) <br>
- [Tencent Cloud API Documentation](https://cloud.tencent.com/document/api) <br>
- [TCCLI Official Documentation](https://cloud.tencent.com/document/product/440) <br>
- [Tencent Cloud CAM Documentation](https://cloud.tencent.com/document/product/598) <br>
- [Tencent Cloud Audit Documentation](https://cloud.tencent.com/document/product/629) <br>
- [CVM Security Check](references/cvm-security-check.md) <br>
- [Automated Resource Check](references/auto-check-resource.md) <br>
- [Cloud Service Health Check](references/cloud-service-healthcheck.md) <br>
- [Lighthouse Website Setup](references/lighthouse-website-setup.md) <br>
- [CBS Bind to CVM](references/cbs-bindto-cvm.md) <br>
- [Lighthouse OpenClaw Setup](references/lighthouse-openclaw-setup.md) <br>
- [Lighthouse App Deploy](references/lighthouse-app-deploy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud API command suggestions that require user-provided credentials, regions, resource identifiers, and explicit confirmation for paid or destructive operations.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
