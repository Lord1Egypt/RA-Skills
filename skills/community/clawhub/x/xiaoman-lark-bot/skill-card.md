## Description:

Lark Bot provides a Feishu/Lark bot integration workflow for sending and receiving messages, managing Wiki knowledge base content, and managing Bitable tasks with sensitive configuration read from environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[griffithkk3-del](https://clawhub.ai/user/griffithkk3-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to connect agents or scripts to Lark chat, event callbacks, Bitable task records, and Wiki documents. It is suited for workflow automation where the operator controls Lark app credentials and permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The webhook receiver may accept unauthenticated requests when LARK_APP_SECRET is missing or signature checks are not enforced.

Mitigation: Require LARK_APP_SECRET, reject missing or invalid signatures, bind locally unless deliberately exposed, and review the webhook implementation before using it on a reachable network.

Risk: The skill can send messages and modify Bitable tables or Wiki documents using the configured Lark app credentials.

Mitigation: Limit the Lark app permissions to the specific chats, Bitable tables, and Wiki spaces intended for automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/griffithkk3-del/skills/xiaoman-lark-bot)
- [Lark Open Platform](https://open.larksuite.com/)
- [Lark app permissions overview](https://open.larksuite.com/document/server-docs/getting-started/overview)
- [Lark IM message API](https://open.larksuite.com/document/server-docs/im-v1/message-content-description)
- [Lark Bitable API](https://open.larksuite.com/document/server-docs/bitable-v1)
- [Lark Wiki API](https://open.larksuite.com/document/server-docs/wiki-v2)
- [Lark webhooks](https://open.larksuite.com/document/server-docs/getting-started/using-webhooks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell command usage, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Lark app credentials supplied through environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
