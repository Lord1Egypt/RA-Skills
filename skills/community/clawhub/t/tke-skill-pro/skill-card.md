## Description: <br>
Tencent Cloud TKE operations skill for cluster inspection, status queries, node pool management, kubeconfig retrieval, and cluster endpoint management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangcong](https://clawhub.ai/user/tangcong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect and administer Tencent Cloud TKE clusters from an AI coding agent. It supports routine health checks, cluster and node pool queries, kubeconfig retrieval, and endpoint enablement or removal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve kubeconfig content, which may expose cluster access credentials. <br>
Mitigation: Treat kubeconfig output as a secret, avoid sharing it in chats, logs, or commits, and require explicit approval before retrieval. <br>
Risk: The skill can create or delete TKE cluster access endpoints, including external endpoints. <br>
Mitigation: Require explicit approval for create-endpoint and delete-endpoint actions, prefer private endpoints, and review external endpoint exposure before enabling it. <br>
Risk: Tencent Cloud credentials are required to run the CLI and could grant broad cloud permissions. <br>
Mitigation: Use least-privileged Tencent Cloud credentials and prefer environment variables or a secret manager over command-line secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangcong/tke-skill-pro) <br>
- [Kubernetes Specialist companion skill](https://github.com/jeffallan/claude-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tables for cluster summaries and JSON details returned from Tencent Cloud TKE APIs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
