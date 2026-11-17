## Description:

查询华为云CCE（云容器引擎）集群列表，支持表格化输出集群名称、状态、版本、节点数等关键字段

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to list Huawei Cloud CCE clusters in a selected region and review cluster name, status, version, and node-count information in a table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Huawei Cloud AK/SK credentials are exposed to the SDK runtime when the skill is used.

Mitigation: Run the skill only in trusted environments, provide credentials through environment variables, and avoid logging or storing credential values.

Risk: The skill requires cloud permissions to list CCE clusters.

Mitigation: Grant only the documented cce:cluster:list permission and avoid broader IAM permissions.

Risk: Dependency installation examples do not pin Huawei Cloud SDK versions.

Mitigation: Pin dependency versions during deployment and review upgrades before use.

Risk: The release artifact references scripts and local reference files that are not included in the artifact evidence.

Mitigation: Confirm the package contains the required executable script and supporting references before relying on the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/test-skill-verify-02)
- [Huawei Cloud SDK Center - CCE](https://console.huaweicloud.com/apiexplorer/#/ssdkcenter)
- [Huawei Cloud CCE API Reference](https://support.huaweicloud.com/aipcecce/index.html)
- [Huawei Cloud CCE ListClusters](https://apiexplorer.developer.huaweicloud.com/apiexplorer/doc?product=CCE&api=ListClusters)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and tabular text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Huawei Cloud AK/SK credentials from environment variables and requires cce:cluster:list permission.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
