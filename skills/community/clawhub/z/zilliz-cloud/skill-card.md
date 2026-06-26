## Description: <br>
Manage Zilliz Cloud clusters and Milvus vector databases: cluster operations, collections, vector search, RBAC, backups, imports, and more via zilliz-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lumina2025](https://clawhub.ai/user/Lumina2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Zilliz Cloud and Milvus vector database resources from an agent-assisted terminal workflow, including cluster lifecycle, collection management, vector operations, RBAC, backups, imports, monitoring, and billing checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help operate real Zilliz Cloud database resources when credentials are configured. <br>
Mitigation: Use least-privileged Zilliz credentials and review exact commands before cluster modification, delete, drop, restore, RBAC, billing, or other high-impact actions. <br>
Risk: API keys or other credentials could be exposed if pasted into chat. <br>
Mitigation: Configure credentials in the user's terminal or environment and avoid sharing secrets in conversation. <br>
Risk: Interactive authentication commands cannot be run reliably inside an AI agent session. <br>
Mitigation: Run zilliz login, zilliz configure, and organization switching commands directly in the user's terminal. <br>


## Reference(s): <br>
- [Zilliz CLI plugin homepage](https://github.com/zilliztech/zilliz-plugin) <br>
- [Zilliz Cloud](https://cloud.zilliz.com/) <br>
- [Zilliz](https://zilliz.com/) <br>
- [ClawHub skill page](https://clawhub.ai/Lumina2025/zilliz-cloud) <br>
- [Publisher profile](https://clawhub.ai/user/Lumina2025) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request JSON output from zilliz-cli for structured parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter: 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
