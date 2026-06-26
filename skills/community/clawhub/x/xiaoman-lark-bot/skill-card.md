## Description: <br>
Lark Bot helps agents integrate with Feishu/Lark for message sending and receiving, Wiki knowledge base operations, and Bitable task management using environment-based configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[griffithkk3-del](https://clawhub.ai/user/griffithkk3-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to connect an agent to a configured Lark workspace for chat notifications, webhook message handling, Wiki document work, and Bitable task updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages and create or update content in a real Lark workspace. <br>
Mitigation: Use a least-privileged test app first and require explicit confirmation before creating, updating, or deleting Bitable or Wiki content. <br>
Risk: Credential and tenant access token handling can expose sensitive Lark app access if logged or shared. <br>
Mitigation: Keep LARK_APP_SECRET in environment-only storage, do not print or share tenant access tokens, and limit app permissions to the minimum required. <br>
Risk: The webhook server may accept unauthenticated events if LARK_APP_SECRET is not configured. <br>
Mitigation: Require LARK_APP_SECRET before running webhook handling and bind the server only where needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/griffithkk3-del/xiaoman-lark-bot) <br>
- [Lark Open Platform](https://open.larksuite.com/) <br>
- [Lark app permissions](https://open.larksuite.com/document/server-docs/getting-started/overview) <br>
- [Lark IM message API](https://open.larksuite.com/document/server-docs/im-v1/message-content-description) <br>
- [Lark Bitable API](https://open.larksuite.com/document/server-docs/bitable-v1) <br>
- [Lark Wiki API](https://open.larksuite.com/document/server-docs/wiki-v2) <br>
- [Lark webhooks](https://open.larksuite.com/document/server-docs/getting-started/using-webhooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lark credentials and workspace identifiers from environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
