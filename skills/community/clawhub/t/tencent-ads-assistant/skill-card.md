## Description:

A Miaowen-based Tencent Ads assistant that helps agents answer advertising questions, query and analyze ad performance, diagnose delivery issues, suggest creative ideas, and support ad material review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yishuang07](https://clawhub.ai/user/yishuang07)

### License/Terms of Use:

MIT-0

## Use Case:

Advertising operators, marketers, and agents use this skill to consult Tencent Ads and WeChat Ads guidance, retrieve account and report data, analyze delivery performance, diagnose under-delivery, generate creative inspiration, and assist with material review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Miaowen API keys in ways the security evidence flags as unsafe.

Mitigation: Avoid pasting API keys into chat, prefer a safer local secret mechanism, and rotate any token previously pasted into conversation or passed on a command line.

Risk: The skill can upload arbitrary local files to a remote service.

Mitigation: Check the exact file path before upload and upload only intended advertising materials.

Risk: The skill sends requests to Tencent/Miaowen endpoints and may access advertising account data.

Mitigation: Use the skill only if you trust the publisher and Tencent/Miaowen endpoints, and limit account scope to the intended accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yishuang07/skills/tencent-ads-assistant)
- [Miaowen platform](https://miaowen.qq.com/)
- [Token management](references/token_management.md)
- [daily_reports/get API reference](references/api/daily_reports_get.md)
- [hourly_reports/get API reference](references/api/hourly_reports_get.md)
- [Report fields reference](references/api/report_fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON responses with shell command and configuration guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Miaowen chat, report, and file upload endpoints through bundled Node.js scripts.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
