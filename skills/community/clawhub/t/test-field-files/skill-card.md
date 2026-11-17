## Description:

查询华为云CDM（Cloud Data Migration）资源详情，包括集群列表、集群详情、任务列表和任务执行历史

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Huawei Cloud CDM clusters, jobs, and job execution history during routine checks or troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud resource metadata queries depend on Huawei Cloud AK/SK credentials, so overly broad credentials could expose more account information than intended.

Mitigation: Use least-privilege read-only IAM credentials and inject credentials through environment variables.

Risk: The release references a query script and reference docs that are not included in the provided artifact.

Mitigation: Confirm the required script and reference documents are present in the deployment environment before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/test-field-files)
- [Huawei Cloud CDM API reference](https://support.huaweicloud.com/api-cdm/index.html)
- [Huawei Cloud KooCLI guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Huawei Cloud CDM query workflow; credentials are expected through environment variables.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
