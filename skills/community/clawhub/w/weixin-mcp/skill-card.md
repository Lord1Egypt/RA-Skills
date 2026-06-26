## Description: <br>
Send and receive WeChat messages, list contacts, and manage a listening daemon through the weixin-mcp CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkmashiro](https://clawhub.ai/user/bkmashiro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to integrate an agent with a WeChat bot account for sending messages, checking inbox activity, listing contacts, and configuring polling or webhook-based receiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send and read WeChat messages through a bot account. <br>
Mitigation: Use a dedicated bot account and confirm recipients, message content, and attachments before sending. <br>
Risk: The skill runs an external CLI package whose resolved version may change when using a range. <br>
Mitigation: Prefer an exact reviewed package version before installing or executing the CLI. <br>
Risk: Webhook endpoints can receive message content and context tokens. <br>
Mitigation: Keep webhooks local or otherwise trusted, and avoid exposing webhook URLs publicly. <br>
Risk: Local account token files are sensitive credentials. <br>
Mitigation: Protect the configured data directory and stop the daemon when real-time receiving is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bkmashiro/weixin-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/bkmashiro) <br>
- [weixin-mcp source](https://github.com/bkmashiro/weixin-mcp) <br>
- [weixin-mcp npm package](https://www.npmjs.com/package/weixin-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WeChat recipient identifiers, webhook URLs, daemon status guidance, and credential storage paths.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
