## Description: <br>
微信机器人快速搭建 - 基于 wechaty/itchat 的微信机器人模板。适合：想做微信自动化的开发者。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill as a starter guide for creating WeChat automation with Wechaty or itchat, including auto-replies, message monitoring, group management, forwarding, scheduled messages, and OpenClaw integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat monitoring, automated posting, and message forwarding can expose private conversation content or send unintended messages. <br>
Mitigation: Use a dedicated test or business WeChat account, restrict the bot to approved chats, add allowlists and confirmations for outbound messages, and rate-limit sends. <br>
Risk: External AI processing can disclose chat content if OpenClaw or another API endpoint is not appropriately protected. <br>
Mitigation: Do not forward chat content to OpenClaw or any API unless the endpoint is authenticated, protected, and governed by clear data-handling rules. <br>
Risk: Participants may not expect automated monitoring or forwarding in chat contexts. <br>
Mitigation: Document participant consent and usage boundaries before enabling monitoring, forwarding, or automated replies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/wechat-bot-starter) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, JavaScript, Python, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup commands, bot examples, configuration snippets, and operational guidance for WeChat automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
