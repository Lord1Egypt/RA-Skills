## Description: <br>
Deploy and manage a Telegram customer service bot powered by Claude and retrieval-augmented generation over local Markdown knowledge base documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youziyouzishu](https://clawhub.ai/user/youziyouzishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support teams use this skill to deploy a long-running Telegram customer service assistant, configure Telegram and Anthropic credentials, load product documentation into a local knowledge base, and route unresolved requests to a human support chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot runs from a real Telegram account and depends on a reusable Telethon session plus Telegram and Anthropic API credentials. <br>
Mitigation: Use a dedicated Telegram account, protect and rotate credentials and session files, and restrict runtime access to the bot host. <br>
Risk: Customer chat content is sent to Anthropic and escalation notices may forward user identifiers and message excerpts to a human support chat. <br>
Mitigation: Publish privacy and consent notices before deployment, redact sensitive content where possible, and limit handoff recipients to authorized support staff. <br>
Risk: The bundled Seers knowledge base includes financial and deposit guidance that may be incomplete or outdated for production support. <br>
Mitigation: Review and correct the knowledge base before launch, add clear risk disclosures, and establish an update process for market, deposit, and policy information. <br>
Risk: Dependencies are specified with lower bounds instead of pinned versions. <br>
Mitigation: Pin and review dependency versions before production deployment, then scan the final environment as part of release. <br>


## Reference(s): <br>
- [Telegram CS Agent ClawHub Page](https://clawhub.ai/youziyouzishu/tg-cs-agent) <br>
- [Seers FAQ](references/seers-faq.md) <br>
- [Seers Platform Overview](references/seers-platform.md) <br>
- [Seers Trading Guide](references/seers-trading.md) <br>
- [Seers User Guide (English)](references/seers-user-guide-en.md) <br>
- [Seers User Guide (Chinese)](references/seers-user-guide-zh.md) <br>
- [Telegram API Credentials](https://my.telegram.org) <br>
- [Anthropic API Endpoint](https://api.anthropic.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, operation, customization, and troubleshooting guidance for a Telegram customer support bot.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
