## Description: <br>
Manage Zilliz Cloud vector databases through zilliz-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanshuyou](https://clawhub.ai/user/zhanshuyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer Zilliz Cloud vector databases, including setup, cluster and collection management, vector operations, RBAC, backups, imports, monitoring, and billing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose powerful Zilliz Cloud administration commands, including delete, drop, restore, RBAC, billing, and vector deletion operations. <br>
Mitigation: Review commands before approval, require confirmation for destructive actions, and verify the active cluster, database, collection, and role targets before execution. <br>
Risk: Authentication credentials, passwords, and payment card details may be needed for some workflows. <br>
Mitigation: Keep secrets and card details in the user's own terminal, use interactive Zilliz login or configuration flows, and avoid sharing credentials in chat or command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhanshuyou/zilliz-skill) <br>
- [Zilliz](https://zilliz.com/) <br>
- [Zilliz Cloud](https://cloud.zilliz.com/) <br>
- [README](README.md) <br>
- [Setup and authentication reference](references/setup.md) <br>
- [Cluster reference](references/cluster.md) <br>
- [Collection reference](references/collection.md) <br>
- [Vector operations reference](references/vector.md) <br>
- [Backup reference](references/backup.md) <br>
- [Monitoring reference](references/monitoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with zilliz-cli shell commands and command-output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request user confirmation before destructive operations and directs sensitive authentication or billing inputs to the user's own terminal.] <br>

## Skill Version(s): <br>
0.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
