## Description: <br>
Huawei Cloud UCS cluster onboarding, lifecycle, access, quota, and fleet-group management guidance using the hcloud CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to register Huawei Cloud CCE or self-managed Kubernetes clusters with UCS, manage cluster lifecycle actions, organize fleet groups, retrieve kubeconfigs, and check UCS quotas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Huawei Cloud AK/SK values and Kubernetes kubeconfig credentials. <br>
Mitigation: Use a least-privilege IAM user, keep credentials out of chat and shell history, store kubeconfigs only in protected files, and restrict file permissions such as chmod 600. <br>
Risk: Cluster deregistration, fleet-group deletion, and related lifecycle commands can remove UCS management capabilities or alter production resources. <br>
Mitigation: Manually confirm cluster and fleet-group identifiers before running destructive commands, check dependent policy governance first, and verify the post-change state with list or show commands. <br>
Risk: The documented full management policy grants broad UCS permissions over Resource *. <br>
Mitigation: Prefer the read-only policy when possible and grant full management permissions only for deliberate onboarding or maintenance tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/ucs-cluster-onboarding-manager) <br>
- [IAM permission policies](artifact/references/iam-policies.md) <br>
- [UCS cluster onboarding API guide](artifact/references/ucs-cluster-onboarding-api-guide.md) <br>
- [Cluster registration workflow](artifact/references/task-cluster-registration.md) <br>
- [Fleet management workflow](artifact/references/task-fleet-management.md) <br>
- [Access management workflow](artifact/references/task-access-management.md) <br>
- [Verification method](artifact/references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with hcloud and kubectl command blocks plus JSON/YAML output examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create, update, or delete cloud resources and may return kubeconfig content; users should review targets and protect credentials before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
