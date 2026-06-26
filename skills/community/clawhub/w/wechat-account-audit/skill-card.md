## Description: <br>
微信公众号账号诊断与对标分析工具，通过解析后台 tendency Excel 数据、文章分类交叉分析、用户画像提取和“你以为 vs 实际上”对比诊断，输出真实用户画像、内容方向修正建议和对标账号筛选标准。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xj797](https://clawhub.ai/user/xj797) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External WeChat Official Account operators use this skill to diagnose account positioning, compare assumed and actual audience profiles, analyze article category performance, and produce a structured Markdown report with benchmark account recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may share sensitive WeChat backend exports, audience screenshots, account identifiers, or unnecessary business metrics during diagnosis. <br>
Mitigation: Use only data the user is authorized to analyze, redact account identifiers and unrelated dashboard details, and prefer aggregate fields over raw screenshots when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xj797/wechat-account-audit) <br>
- [WeChat Tendency Excel format reference](references/excel_format.md) <br>
- [Report template](assets/report_template.md) <br>
- [Case study: 七海的底稿](assets/case_study_qihai.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, JSON article data from the parser, and optional shell commands for parsing Excel exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process WeChat backend Excel exports and user-provided audience screenshots; users should redact unnecessary private account and analytics details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
