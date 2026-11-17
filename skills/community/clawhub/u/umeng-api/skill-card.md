## Description:

查询友盟 (UMeng) 应用统计数据分析，支持通过 APPKEY 获取应用的基础指标信息如新增用户数、活跃用户数等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query UMeng application analytics by APPKEY, including new users, active users, retention, channel metrics, and anomaly attribution report links. It helps agents prepare concise analytics reports from UMeng OpenAPI responses when valid UMeng credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: UMeng credentials used with this skill may authorize more than read-only analytics.

Mitigation: Prefer scoped or read-only UMeng credentials where available and avoid sharing credentials in prompts, logs, or committed files.

Risk: Local umeng-config.json files can expose API credentials if stored with broad permissions or committed to version control.

Mitigation: Keep umeng-config.json out of version control and restrict it to owner-only permissions.

Risk: The bundled wrappers include create and edit request classes in addition to analytics queries.

Mitigation: Review or remove account-changing request wrappers when the deployment only needs analytics reporting.

Risk: The diagnostic module can make live UMeng requests and print returned data.

Mitigation: Avoid running diagnostic entry points directly in shared environments unless credentials, APPKEYs, and outputs are approved for that environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/umeng-api)
- [ClawHub publisher profile](https://clawhub.ai/user/squall0925)
- [UMeng OpenAPI signature documentation](https://open.1688.com/api/sysSignature.htm)
- [UMeng UApp new users API](https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getNewUsers&v=1&cat=default)
- [UMeng UApp active users API](https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getActiveUsers&v=1&cat=default)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text summaries with Python and shell snippets; API helper functions may return dictionaries parsed from JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UMeng API credentials and an application APPKEY for live API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
