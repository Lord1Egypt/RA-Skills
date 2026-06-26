## Description: <br>
Converts WeFlow-exported WeChat chat JSON into personal knowledge base entries, knowledge cards, customer profiles, and AI persona training data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weebrclb123-del](https://clawhub.ai/user/weebrclb123-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and external operators use this skill to analyze authorized WeFlow chat exports and turn selected conversations into structured knowledge cards, customer profile notes, follow-up summaries, and Feishu-ready knowledge base fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes private WeChat exports and can convert conversations into persistent customer profiles, knowledge records, and training data. <br>
Mitigation: Use only authorized, deliberately selected chat exports; remove unrelated or sensitive conversations before analysis. <br>
Risk: Generated profiles or summaries may expose personal, customer, or business-sensitive information if uploaded broadly. <br>
Mitigation: Review and redact outputs before any Feishu upload, and confirm workspace permissions, retention, and deletion plans. <br>
Risk: Using broad paths or unreviewed export folders may process more chat history than intended. <br>
Mitigation: Use exact file paths and verify the selected input files before running parsing or analysis commands. <br>


## Reference(s): <br>
- [Feishu knowledge base field design reference](artifact/references/feishu-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/weebrclb123-del/wechat-knowledge-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown knowledge cards, structured summaries, Feishu field guidance, and optional generated files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize private chat exports into persistent profiles or training data; review and redact outputs before storage or sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
