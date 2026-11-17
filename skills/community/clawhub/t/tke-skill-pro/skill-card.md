## Description:

Tencent Cloud TKE operations skill for cluster inspection, status queries, node pool management, endpoint management, and kubeconfig retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangcong](https://clawhub.ai/user/tangcong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to operate Tencent Cloud TKE clusters from an AI coding agent, including inventory, health checks, node pool review, endpoint management, and kubeconfig retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Tencent Cloud credentials that can authorize powerful TKE and Kubernetes operations.

Mitigation: Install only from a trusted publisher and use tightly scoped credentials through environment variables or a secret manager rather than command-line secrets.

Risk: Kubeconfig output can expose cluster access if printed into chat, logs, or shared files.

Mitigation: Avoid asking the agent to print kubeconfig into chat or logs, and store kubeconfig only in protected files.

Risk: Endpoint creation and deletion commands can change cluster access paths, including external access.

Mitigation: Review every create-endpoint or delete-endpoint action and its target cluster, subnet, security group, and extranet setting before execution.

Risk: The skill recommends installing a separate third-party Kubernetes skill for in-cluster operations.

Mitigation: Independently audit the recommended Kubernetes skill before installing or using it with cluster credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangcong/skills/tke-skill-pro)
- [Kubernetes Specialist companion skill](https://github.com/jeffallan/claude-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, inline shell commands, and supplemental JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Cloud TKE command output, kubeconfig material, and operational status summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
