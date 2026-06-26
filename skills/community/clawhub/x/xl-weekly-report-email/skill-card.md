## Description: <br>
通用周报收集和邮件推送技能，支持交互式填写周报内容，自动计算周数和日期范围，生成美观的HTML格式邮件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zq62191161-ai](https://clawhub.ai/user/zq62191161-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual contributors use this skill to collect weekly report inputs, calculate the reporting week and date range, preview a formatted HTML email, and send the report through a configured SMTP account after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local SMTP credentials and can send email using that account. <br>
Mitigation: Use an app-specific SMTP authorization code, restrict access to the skill directory and .env file, and install only when SMTP sending authority is acceptable. <br>
Risk: Weekly report text, recipients, or CC addresses could expose sensitive information or be sent to unintended recipients. <br>
Mitigation: Review the generated HTML preview and all To/CC fields before confirming send, and avoid entering secrets or confidential content in report text. <br>
Risk: The security summary flags a vulnerable email-sending dependency. <br>
Mitigation: Prefer an updated release that upgrades nodemailer before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zq62191161-ai/xl-weekly-report-email) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, local configuration values, Node.js shell commands, and generated HTML email content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a temporary weekly-report Markdown file and send email through configured SMTP only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
