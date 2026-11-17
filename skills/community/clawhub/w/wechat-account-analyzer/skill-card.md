## Description:

公众号账号诊断工具对任意公众号账号进行四维度量化评分，按行业水平对标并输出可落地的运营优化建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as WeChat public-account owners, social media operators, MCN agencies, brands, and content creators use this skill to diagnose account health, compare peer accounts, and plan data-driven content and operations improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and may persist credentials if an agent configures the environment.

Mitigation: Set REDFOX_API_KEY only for the current process or in a dedicated secret store, and do not allow the agent to print it or append it to shell startup files.

Risk: Queried public-account names or IDs are sent to redfox.hk for analysis.

Mitigation: Use the skill only for account identifiers that are acceptable to submit to the RedFox service.

Risk: The security summary flags persistent subscription behavior and mandatory promotional output.

Mitigation: Avoid subscription or follow-up behavior unless explicitly desired, and review generated reports before sharing.

Risk: Generated HTML reports are flagged as unsafe until output escaping is fixed.

Mitigation: Treat generated HTML as untrusted and sanitize or review it before opening in sensitive contexts or distributing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/wechat-account-analyzer)
- [RedFox Hub](https://redfox.hk/?source=clawhub)
- [Core Workflow](references/core_workflow.md)
- [Workflow Guide](references/workflow_guide.md)
- [API Guide](references/api_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML]

**Output Format:** [Markdown diagnostic reports, JSON data files, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports follow a fixed five-section structure and may store raw and report data locally.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
