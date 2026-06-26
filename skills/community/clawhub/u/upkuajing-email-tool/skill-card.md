## Description: <br>
Official skill for UpKuaJing that sends emails and tracks email task status through email sending, task list, and task record list APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upkuajing](https://clawhub.ai/user/upkuajing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, marketers, exporters, and sales users can use this skill to send personalized email campaigns, inspect campaign task lists, and review delivery, open, and click status for individual task records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends email content and recipient data to an external email provider. <br>
Mitigation: Use only with recipient lists and message content approved for UpKuaJing processing, and confirm the target recipients before sending. <br>
Risk: The security summary flags account, balance, recharge/payment, and background version-check behavior beyond basic email sending. <br>
Mitigation: Review the requested action before execution and require explicit confirmation before any recharge, payment, or paid email-send operation. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Store UPKUAJING_API_KEY only in the expected environment or user configuration file and avoid sharing logs or outputs that may expose account details. <br>


## Reference(s): <br>
- [Email Send API Reference](references/email-send-api.md) <br>
- [Email Task List API Reference](references/email-task-list-api.md) <br>
- [Email Task Record List API Reference](references/email-task-record-list-api.md) <br>
- [UpKuaJing Homepage](https://www.upkuajing.com) <br>
- [UpKuaJing Open Platform](https://developer.upkuajing.com/) <br>
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/upkuajing-email-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; email sending may incur provider fees.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
