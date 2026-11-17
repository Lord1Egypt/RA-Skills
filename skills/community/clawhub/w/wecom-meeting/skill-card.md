## Description:

企业微信会议管理工具。用于创建、查询、取消和管理企业微信预约会议。支持创建预约会议、获取会议详情、取消会议、获取成员会议列表等操作。使用企业微信会议API需要配置CorpID、Secret和AgentID。当用户需要创建企业微信会议、查询会议信息、取消会议或管理会议时使用此Skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[limawanyan](https://clawhub.ai/user/limawanyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to create, inspect, cancel, and list WeCom scheduled meetings through the WeCom meeting API. It is intended for environments where a WeCom application with CorpID, Secret, AgentID, and meeting permissions is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live organizational WeCom credentials and meeting-management actions.

Mitigation: Install only from a trusted publisher, grant a least-privilege WeCom application, and store ~/.wecom/config.json with restrictive file permissions.

Risk: Running scripts/wecom_meeting_api.py directly can expose part of an access token in terminal output.

Mitigation: Avoid direct execution of that module until token printing is removed; use the task-specific CLI wrappers instead.

Risk: Cancellation commands can affect real scheduled meetings.

Mitigation: Review meeting IDs and user IDs carefully before confirming cancellation, and avoid --force unless the action has already been independently verified.

Risk: The dependency is installed from the ambient Python environment unless pinned by the operator.

Mitigation: Use a virtual environment with pinned dependencies before running the scripts.

## Reference(s):

- [WeCom Meeting API Reference](references/api.md)
- [WeCom Create Scheduled Meeting API](https://developer.work.weixin.qq.com/document/path/99104)
- [WeCom Cancel Scheduled Meeting API](https://developer.work.weixin.qq.com/document/path/99048)
- [WeCom Get Meeting Details API](https://developer.work.weixin.qq.com/document/path/99049)
- [WeCom Get User Meeting IDs API](https://developer.work.weixin.qq.com/document/path/99050)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code examples, CLI text output, and optional JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs live WeCom API calls using local ~/.wecom/config.json credentials when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
