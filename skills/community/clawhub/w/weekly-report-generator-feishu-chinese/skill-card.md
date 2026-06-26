## Description: <br>
Use this skill to generate weekly reports from git commit logs, work descriptions, and optional screenshots, then format the result as a professional report for Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prayone](https://clawhub.ai/user/prayone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and team leads use this skill to summarize weekly engineering work from local Git history and optional screenshots, rewrite technical commits into business-facing Chinese weekly-report prose, and send the report to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan local Git repositories and include commit history or work details in a weekly report. <br>
Mitigation: Set PROJECT_ROOT only to repositories intended for reporting and review the generated report before sharing. <br>
Risk: The skill can send generated reports to Feishu automatically without a built-in review step. <br>
Mitigation: Require a preview before sending, verify the Feishu recipient, and avoid enabling unattended scheduling unless recurring delivery is intended. <br>
Risk: Feishu application credentials are configured in the sender script. <br>
Mitigation: Store Feishu secrets outside the script where possible and limit the Feishu application permissions to the minimum required for report delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/prayone/weekly-report-generator-feishu-chinese) <br>
- [Publisher profile](https://clawhub.ai/user/prayone) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>
- [Artifact: weekly report feature overview](artifact/周报生成器功能介绍.md) <br>
- [Artifact: installation and configuration guide](artifact/安装和配置指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with shell command guidance and Feishu message delivery status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports summarize commits, code-change counts, repository counts, and business-facing work highlights; Feishu messages are truncated by the bundled sender script to 3000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
