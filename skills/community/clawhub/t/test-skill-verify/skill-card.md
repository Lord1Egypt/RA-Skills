## Description:

Queries Huawei Cloud CCE cluster lists and returns key cluster fields such as name, status, version, and node count in tabular form.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Huawei Cloud CCE clusters for routine checks, resource management, and troubleshooting. It helps list cluster status, Kubernetes version, and node counts for a selected Huawei Cloud region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Huawei Cloud credentials are required to query CCE clusters.

Mitigation: Use environment variables for AK/SK values, avoid logging credentials, and provide only least-privilege credentials with cce:cluster:list permission.

Risk: The referenced execution script is not included in the artifact evidence.

Mitigation: Inspect any separately supplied script before running it and prefer pinned, reviewed SDK dependencies in a virtual environment.

## Reference(s):

- [Huawei Cloud SDK Center - CCE](https://console.huaweicloud.com/apiexplorer/#/ssdkcenter)
- [Huawei Cloud CCE API Reference](https://support.huaweicloud.com/aipcecce/index.html)
- [Huawei Cloud CCE ListClusters API](https://apiexplorer.developer.huaweicloud.com/apiexplorer/doc?product=CCE&api=ListClusters)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and tabular text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Huawei Cloud credentials from environment variables and least-privilege cce:cluster:list access.]

## Skill Version(s):

0.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
