## Description:

分析微信公众号后台 tendency Excel 和可选用户画像截图，生成用户画像修正、内容方向建议与对标账号清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xj797](https://clawhub.ai/user/xj797)

### License/Terms of Use:

MIT-0

## Use Case:

微信公众号运营者 use this skill to diagnose real reader demographics, compare expected and actual audiences, evaluate content category performance, and choose better benchmark accounts. It is especially suited to cold-start or directionally uncertain public accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may require WeChat analytics exports and audience demographic screenshots that contain account or audience information.

Mitigation: Redact unrelated account details, share only aggregate metrics where possible, and avoid including personal data beyond what is needed for the diagnosis.

Risk: The bundled report template includes WorkBuddy attribution and a specific Chinese visual/reporting style.

Mitigation: Review and edit the final report template before sharing if attribution or styling does not match the publisher's intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xj797/skills/wechat-account-audit)
- [WeChat tendency Excel format reference](artifact/references/excel_format.md)
- [Structured report template](artifact/assets/report_template.md)
- [Qihai case study](artifact/assets/case_study_qihai.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with tables, optional parser JSON, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include HTML span styling from the bundled Chinese report template.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
