## Description: <br>
腾讯广告妙问 helps agents answer Tencent Ads and WeChat Ads questions, query campaign reports, analyze accounts, diagnose delivery issues, find creative inspiration, and guide ad material review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yishuang07](https://clawhub.ai/user/yishuang07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, advertisers, and agent users use this skill to consult Tencent Ads guidance, query authorized account reports, analyze delivery performance, diagnose campaign issues, get creative examples, and handle material review questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Tencent Ads/Miaowen API tokens are required and stored locally for helper scripts. <br>
Mitigation: Use the local token setup flow, avoid exposing tokens in chat or logs, and rotate the token if it may have been shared. <br>
Risk: The API-mode helper can use the stored token for broad authenticated requests. <br>
Mitigation: Keep API-mode use to documented Tencent Ads report paths and review request parameters before execution. <br>
Risk: Material audit workflows can upload local files to Tencent/Miaowen services. <br>
Mitigation: Upload only files the user is authorized to send for audit and avoid sensitive or unrelated materials. <br>


## Reference(s): <br>
- [腾讯广告妙问 on ClawHub](https://clawhub.ai/yishuang07/tencent-ads-assistant) <br>
- [妙问官网](https://miaowen.qq.com/) <br>
- [Token Management](references/token_management.md) <br>
- [daily_reports/get API Reference](references/api/daily_reports_get.md) <br>
- [hourly_reports/get API Reference](references/api/hourly_reports_get.md) <br>
- [Report Fields Reference](references/api/report_fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses, JSON API results, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tencent Ads/Miaowen access token for authenticated account data, report queries, and file upload workflows.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
