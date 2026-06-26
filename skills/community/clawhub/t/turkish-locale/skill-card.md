## Description: <br>
Turkish locale skill pack for Hermes Agent with Turkish communication guidance, Turkish news aggregation, BIST100 and market tracking, and daily brief automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erhnysr](https://clawhub.ai/user/erhnysr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to localize Hermes Agent for Turkish-language interactions, Turkish news summaries, Turkish market lookups, and scheduled daily briefings through channels such as Telegram or Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring briefs may send content to the wrong channel or at an unexpected time if the schedule or delivery target is misconfigured. <br>
Mitigation: Confirm the cron schedule, Istanbul-to-UTC conversion, and Telegram or Discord destination before enabling recurring delivery. <br>
Risk: Telegram delivery requires a bot token and channel configuration. <br>
Mitigation: Use a dedicated Telegram bot token, limit its permissions, and keep the token outside prompts and shared logs. <br>
Risk: The BIST-named helper script fetches cryptocurrency prices rather than BIST100 equity prices. <br>
Mitigation: Review helper script behavior before relying on it for Turkish equity market data. <br>
Risk: The skill includes a Turkish personality template that changes assistant tone and locale behavior. <br>
Mitigation: Review the SOUL.md persona text before copying it into an agent configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erhnysr/turkish-locale) <br>
- [Bloomberg HT BIST100](https://www.bloomberght.com/borsa/endeksler/bist-100) <br>
- [Bigpara live market data](https://bigpara.hurriyet.com.tr/borsa/canli-borsa/) <br>
- [Yahoo Finance chart API example](https://query1.finance.yahoo.com/v8/finance/chart/XU100.IS?interval=1d&range=1d) <br>
- [CoinGecko markets API](https://api.coingecko.com/api/v3/coins/markets) <br>
- [Telegram Bot API](https://api.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, and optional JSON or terminal output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are primarily Turkish or bilingual Turkish/English and may include market/news timestamps for freshness.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
