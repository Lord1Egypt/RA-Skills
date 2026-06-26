## Description: <br>
Feishu Card helps agents send rich Feishu interactive card messages using schema 2.0, including titles, Markdown body content, and color themes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare or send Feishu interactive cards to individual users or group chats when an agent needs structured notification messages with Markdown content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu app credentials to send messages through Feishu APIs. <br>
Mitigation: Install only when the publisher is trusted, use approved Feishu app credentials, confirm recipients before sending, and avoid sensitive content unless the app and destination are authorized. <br>
Risk: The artifact contains hardcoded Feishu app and example recipient identifiers. <br>
Mitigation: Replace the hardcoded app_id and example recipient IDs with approved local configuration before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dadaniya99/xiaolongxia-feishu-card) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu send message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu schema 2.0 interactive card payload guidance and optional send commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
