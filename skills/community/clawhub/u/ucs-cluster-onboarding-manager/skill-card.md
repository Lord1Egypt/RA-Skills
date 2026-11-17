## Description:

Huawei Cloud UCS cluster onboarding, lifecycle, access, quota, and fleet grouping management skill using the hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud platform operators use this skill to manage Huawei Cloud UCS cluster registration, deregistration, lifecycle queries and updates, fleet grouping, kubeconfig access, federation kubeconfig downloads, and quota checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive kubeconfig credentials can be exposed when pasted into command-line arguments, chat, tickets, shell history, or CI logs.

Mitigation: Use a secure file, stdin, or secret-store workflow if supported by hcloud; avoid pasting real kubeconfig YAML into shared systems or logged commands.

Risk: The skill supports privileged Huawei Cloud UCS administration actions, including cluster registration, deregistration, fleet changes, kubeconfig generation, and quota inspection.

Mitigation: Grant only the minimum UCS IAM permissions needed, prefer IAM users over root credentials, enable MFA for sensitive operations, and confirm destructive actions before execution.

Risk: Downloaded kubeconfig and federation credentials can grant cluster access beyond the immediate task.

Mitigation: Use restrictive file permissions before writing kubeconfig files, keep federation token duration short, and rotate or regenerate credentials when access is no longer needed.

## Reference(s):

- [IAM Permission Policies](references/iam-policies.md)
- [Task: Cluster Registration](references/taREDACTED-SECRET.md)
- [Task: Access Management](references/task-access-management.md)
- [Task: Fleet Management](references/task-fleet-management.md)
- [UCS Cluster Onboarding API Reference Guide](references/ucs-cluster-onboarding-api-guide.md)
- [Verification Method](references/verification-method.md)
- [Common Pitfalls and Solutions](references/common-pitfalls.md)
- [Output Format](references/output-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline hcloud CLI commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational checklists, IAM policy guidance, verification steps, and warnings for credential-sensitive workflows.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
