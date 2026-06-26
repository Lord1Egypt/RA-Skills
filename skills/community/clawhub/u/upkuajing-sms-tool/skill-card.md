## Description: <br>
Official skill for upkuajing (跨境魔方). SMS tool API for sending SMS and tracking SMS task status. Includes SMS sending, task list, and task record list APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upkuajing](https://clawhub.ai/user/upkuajing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, sales, and operations teams use this skill to send SMS messages, review SMS task lists, and inspect delivery records through UpKuaJing's SMS service. It supports promotional outreach, notifications, two-factor authentication, and client communication workflows that require explicit user review before paid sends or account top-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive recipient phone numbers, SMS message bodies, delivery records, billing activity, and an UPKUAJING_API_KEY. <br>
Mitigation: Use environment variables or a managed secrets store for the API key, avoid committing local credential files, and share SMS content or delivery data only with trusted UpKuaJing accounts. <br>
Risk: SMS sending and account top-up actions can incur charges. <br>
Mitigation: Review pricing through the documented price endpoint or pricing page and require explicit user confirmation before executing paid sends or creating top-up orders. <br>
Risk: Normal operation sends request data to UpKuaJing's hosted API and may keep a small local version cache. <br>
Mitigation: Use the skill only where contacting openapi.upkuajing.com is acceptable and where local cache behavior is permitted by the user's environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/upkuajing/upkuajing-sms-tool) <br>
- [UpKuaJing homepage](https://www.upkuajing.com) <br>
- [UpKuaJing developer portal](https://developer.upkuajing.com/) <br>
- [UpKuaJing SMS pricing](https://www.upkuajing.com/web/openapi/price.html) <br>
- [SMS Send API Reference](references/sms-send-api.md) <br>
- [SMS Task List API Reference](references/sms-task-list-api.md) <br>
- [SMS Task Record List API Reference](references/sms-task-record-list-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; invoked scripts return JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, httpx, and UPKUAJING_API_KEY; normal use contacts openapi.upkuajing.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence, release metadata, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
