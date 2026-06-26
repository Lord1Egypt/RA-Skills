## Description: <br>
Provides guidance for using node-telegram-cli to interact with Telegram over MTProto, including reading and sending messages, managing groups and contacts, searching conversations, downloading media, and automating workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baontq23](https://clawhub.ai/user/baontq23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to operate a Telegram account through node-telegram-cli for account messaging, conversation search, media handling, group administration, contact management, and Telegram workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad persistent access to private Telegram account actions. <br>
Mitigation: Install only if that access is acceptable, prefer a dedicated Telegram account, and log out when finished. <br>
Risk: An agent could read broad inbox data, search all chats, send or delete messages, forward content, download media, or change groups and contacts without sufficient consent. <br>
Mitigation: Require explicit approval before broad reads, global searches, message sends or deletion, forwarding, downloads, group changes, or contact changes. <br>
Risk: The skill depends on an external npm package that performs Telegram account operations. <br>
Mitigation: Review the external npm package before installation and deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baontq23/telegram-cli) <br>
- [node-telegram-cli npm package](https://www.npmjs.com/package/node-telegram-cli) <br>
- [node-telegram-cli repository](https://github.com/baontq23/node-telegram-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with command examples and JSON output schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JSON mode for automation; read commands return machine-readable Telegram conversation and message data.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
