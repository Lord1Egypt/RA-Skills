## Description: <br>
Operate Telegram Bot API through UXC with a curated OpenAPI schema, bot-token path auth, polling-based reads, and webhook management guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Telegram Bot API authentication, inspect supported operations, send bot messages or media, poll updates, and manage webhook state through UXC with guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent send Telegram messages, upload selected files, and change webhook configuration through a real bot token. <br>
Mitigation: Use a dedicated bot token with limited chat or channel permissions, and require explicit confirmation before send, upload, or webhook-changing operations. <br>
Risk: Media or certificate upload commands may expose unintended local files if paths are chosen carelessly. <br>
Mitigation: Verify each local file path before media or certificate uploads and avoid granting the bot access to sensitive files. <br>
Risk: Polling can write Telegram updates to local log files that may contain private chat data. <br>
Mitigation: Write polling logs only to controlled locations with appropriate permissions and retention. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated Telegram Bot OpenAPI schema](references/telegram-bot.openapi.json) <br>
- [Telegram Bot API docs](https://core.telegram.org/bots/api) <br>
- [Local Bot API server](https://github.com/tdlib/telegram-bot-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, api calls] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Telegram API operation names, UXC auth setup, polling configuration, and confirmation prompts for write operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
