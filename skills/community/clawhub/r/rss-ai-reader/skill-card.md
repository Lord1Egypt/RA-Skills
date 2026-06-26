## Description: <br>
RSS AI Reader helps agents set up an RSS/Atom monitoring workflow that summarizes feed items with Claude or OpenAI and sends Chinese-language updates through Feishu, Telegram, or Email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BENZEMA216](https://clawhub.ai/user/BENZEMA216) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and knowledge workers use this skill to configure RSS or Atom feed monitoring, summarize new articles with an LLM, and deliver recurring updates to team or personal notification channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends feed content and summaries to selected AI and notification services, which may expose sensitive source material or derived information. <br>
Mitigation: Only configure feeds whose contents are appropriate for the selected services, and review privacy requirements before enabling scheduled runs. <br>
Risk: The skill requires LLM API keys and messaging credentials for regular operation. <br>
Mitigation: Store secrets in environment variables, use least-privilege bot, webhook, and app-password credentials, and avoid committing configuration files containing real secrets. <br>
Risk: The artifact references an external repository and Python requirements for installation. <br>
Mitigation: Review the referenced repository and dependencies before installing, prefer a pinned commit for regular use, and test with the one-time run mode before enabling scheduled execution. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/BENZEMA216/rss-ai-reader) <br>
- [Configuration guide](references/config_guide.md) <br>
- [RSS reader repository referenced in setup](https://github.com/BENZEMA216/rss-reader.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, text] <br>
**Output Format:** [Markdown with inline bash and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes RSS feed configuration, LLM provider settings, notification channel setup, and run commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
