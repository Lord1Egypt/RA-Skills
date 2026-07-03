## Description: <br>
Huawei Cloud UCS Policy Governor helps agents manage UCS policy instances, policy definitions, enforcement jobs, and compliance audits through hcloud CLI guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud platform engineers, and compliance operators use this skill to manage Huawei Cloud UCS policy instances, enable or disable policy enforcement on clusters or fleet groups, and audit fleet compliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers broad Huawei Cloud UCS operations that can create, update, disable, or delete policy enforcement on clusters and fleet groups. <br>
Mitigation: Use a dedicated least-privilege IAM user, prefer read-only permissions for audit tasks, avoid production targets for verification examples, and confirm cluster, fleet, policy, and job IDs before write operations. <br>
Risk: Huawei Cloud credentials and generated kubeconfig files can grant sensitive cloud or cluster access if exposed. <br>
Mitigation: Keep AK/SK values out of code, chat, shell history, and logs; use environment variables or masked CLI configuration; rotate credentials regularly; and clean up generated kubeconfig files. <br>


## Reference(s): <br>
- [UCS Policy API Reference Guide](references/ucs-policy-api-guide.md) <br>
- [IAM Permission Policies](references/iam-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Task: Policy Management](references/task-policy-management.md) <br>
- [Task: Compliance Audit](references/task-compliance-audit.md) <br>
- [Common Pitfalls & Solutions](references/common-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline hcloud CLI commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include policy-management guidance, IAM permission JSON, and verification steps; users should review target IDs before changing cloud resources.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
