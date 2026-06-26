## Description: <br>
Curates the top five daily GeekNews issues with emphasis on open source releases and GitHub projects, formats them as a concise Telegram brief, and supports scheduled delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongjus](https://clawhub.ai/user/dongjus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create a daily Telegram digest of GeekNews items, prioritizing open source launches, GitHub momentum, developer tools, AI, and infrastructure topics. It can be run manually or scheduled with cron after Telegram credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram, Anthropic, and GitHub tokens may be exposed if stored in shared shell profiles, dotfiles, logs, or copied into messages. <br>
Mitigation: Use a dedicated Telegram bot and chat, keep tokens in local environment configuration, avoid syncing secrets through dotfiles, and rotate any token that may have been exposed. <br>
Risk: Scheduled cron execution can repeatedly post to the wrong chat or send unreviewed content if enabled before testing. <br>
Mitigation: Test the recipient, generated message, and Telegram delivery path manually before enabling cron. <br>
Risk: The daily digest can include incomplete or misleading summaries from scraped or model-generated news curation. <br>
Mitigation: Review the generated brief before broad distribution when accuracy or audience impact matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongjus/telegram-geeknews) <br>
- [Telegram setup guide](references/telegram_setup.md) <br>
- [GeekNews](https://news.hada.io) <br>
- [GeekNews RSS feed](https://news.hada.io/rss) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown Telegram message plus shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Telegram messages are intended to stay within the 4096 character message limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
