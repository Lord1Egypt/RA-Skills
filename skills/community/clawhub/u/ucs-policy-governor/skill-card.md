## Description:

Huawei Cloud UCS (Universal Cloud Service) policy governance and compliance management skill using hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and cloud administrators use this skill to manage Huawei Cloud UCS policy instances, policy definitions, policy enforcement, and compliance audits across clusters and fleet groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, delete, enable, and disable Huawei Cloud UCS policy governance settings.

Mitigation: Prefer read-only IAM permissions for audits and require explicit approval after confirming account, region, cluster, fleet group, and policy instance before any mutating command.

Risk: Functional verification and remediation flows can affect production clusters or fleet groups.

Mitigation: Run verification and remediation against non-production targets by default, use gradual rollout with warn mode where appropriate, and require approval before deny-mode enforcement or deletion.

Risk: Cloud credentials and generated kubeconfig files can expose access to managed clusters.

Mitigation: Never print AK/SK values, use masked credential checks, write kubeconfig only to a private temporary file with restrictive permissions, and remove it immediately after use.

## Reference(s):

- [UCS Policy API Reference Guide](references/ucs-policy-api-guide.md)
- [IAM Permission Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Common Pitfalls and Solutions](references/common-pitfalls.md)
- [Task: Policy Management](references/task-policy-management.md)
- [Task: Compliance Audit](references/task-compliance-audit.md)
- [Huawei Cloud UCS Documentation](https://support.huaweicloud.com/ucs/index.html)
- [hcloud CLI Documentation](https://support.huaweicloud.com/cli/index.html)
- [Huawei Cloud API Explorer](https://apiexplorer.developer.huaweicloud.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hcloud CLI commands, IAM policy snippets, compliance checklists, and remediation steps.]

## Skill Version(s):

0.1.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
