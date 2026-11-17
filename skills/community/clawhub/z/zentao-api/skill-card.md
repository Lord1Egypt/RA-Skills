## Description:

调用禅道（ZenTao）RESTful API v2.0 完成用户请求，覆盖项目集、产品、项目、执行、需求（Story/Epic/Requirement）、Bug、任务、测试用例、测试单、产品计划、版本、发布、反馈、工单、应用、用户、文件等 20 个模块的增删改查及状态流转操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[catouse](https://clawhub.ai/user/catouse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to query and update ZenTao project management records through the ZenTao RESTful API v2.0. It supports common workflows such as listing projects and bugs, creating tasks or requirements, and changing issue or task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling stores ZenTao URL, token, and account data in ~/.zentao-token.json.

Mitigation: Treat the token cache as sensitive credential material and restrict access to trusted local environments.

Risk: The documented eval-based token-loading flow can execute unexpected shell output if the helper script or environment is compromised.

Mitigation: Review the helper script before use, avoid the eval flow unless it is fixed, and prefer safer environment-variable handling.

Risk: The skill can create, update, delete, and change status for live ZenTao records.

Mitigation: Confirm every write or delete operation unless the user has explicitly authorized direct mutation.

Risk: Using an untrusted or non-HTTPS ZenTao server can expose credentials and project data.

Mitigation: Use the skill only with trusted ZenTao servers and prefer HTTPS-only URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catouse/skills/zentao-api)
- [Repository metadata](https://github.com/easysoft/zentao-skills.git)
- [ZenTao API 2.0 official documentation](https://www.zentao.net/book/api/2309.html)
- [ZenTao API 1.0 documentation](https://www.zentao.net/book/api/1397.html)
- [Artifact API reference](artifact/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed ZenTao API requests and parsed response summaries; write or delete operations should be confirmed before execution.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
