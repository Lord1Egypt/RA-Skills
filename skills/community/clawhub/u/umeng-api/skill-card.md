## Description: <br>
查询友盟 (UMeng) 应用统计数据分析，支持通过 APPKEY 获取应用的基础指标信息如新增用户数、活跃用户数等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and analytics teams use this skill to query UMeng app metrics such as new users, active users, daily data, and anomaly reports for a supplied APPKEY. It can help an agent retrieve metrics, format anomaly findings, and guide credential configuration for UMeng API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled UMeng SDK exposes account-changing request classes beyond the expected read-only metrics workflow. <br>
Mitigation: Use tightly scoped UMeng credentials and avoid create, edit, or back-report request classes unless account changes are intended. <br>
Risk: UMeng API credentials may be loaded from umeng-config.json or environment variables. <br>
Mitigation: Keep umeng-config.json private, exclude it from version control, and restrict file permissions to the owning user. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/squall0925/umeng-api) <br>
- [UMeng OpenAPI signature documentation](https://open.1688.com/api/sysSignature.htm) <br>
- [UMeng new users API](https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getNewUsers&v=1&cat=default) <br>
- [UMeng active users API](https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getActiveUsers&v=1&cat=default) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown or plain text summaries with JSON-like metric data and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UMeng credentials and an app APPKEY; may return raw API response fields for debugging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
