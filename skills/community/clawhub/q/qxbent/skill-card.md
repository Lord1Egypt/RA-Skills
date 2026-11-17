## Description:

启信宝企业信息查询工具，提供企业工商信息、股东信息、主要人员、变更记录等查询功能。支持通过企业名称查询，返回标准化的企业数据。

This skill is for research and development only.

## Publisher:

[llx-26](https://clawhub.ai/user/llx-26)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to query QiXinBao enterprise records by company name and return standardized business registration, shareholder, key personnel, and change-record information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The exported client can send the QiXinBao API token to a caller-chosen URL.

Mitigation: Use createClient() with the documented QiXinBao endpoint, avoid passing a custom baseURL, and review any direct QxbEntClient construction before use.

Risk: The skill requires a sensitive QXBENT_API_TOKEN credential.

Mitigation: Configure the token only through the environment variable, use a limited-scope token where available, and monitor or rotate it regularly.

Risk: The skill installs Node.js dependencies before use.

Mitigation: Install dependencies from a reviewed lockfile or restricted environment and review dependency updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llx-26/skills/qxbent)
- [QiXinBao enterprise API endpoint](https://external-api.qixin.com/skill/ent/public)
- [Enterprise information API](references/getEnterpriseInformation.md)
- [Shareholder list API](references/getPartnerListV3.md)
- [Key personnel API](references/getEmployeesListV4.md)
- [Change records API](references/getPagingEntBasicInfo.md)
- [User guide](USER_GUIDE.md)
- [Testing guide](TESTING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with optional TypeScript examples, shell commands, and structured enterprise fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, axios, and a QXBENT_API_TOKEN environment variable; query results depend on the QiXinBao API and token permissions.]

## Skill Version(s):

1.0.2 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
