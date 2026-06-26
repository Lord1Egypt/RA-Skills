## Description: <br>
Daily inspirational quotes from ZenQuotes.io. Get daily wisdom, random quotes, quote images. Supports automated daily delivery via cron scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisluo5311](https://clawhub.ai/user/chrisluo5311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use ZenQuote to fetch daily, random, or multiple inspirational quotes and quote images from ZenQuotes.io. Users can also configure optional recurring Telegram delivery for daily quote messages or images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running setup enables recurring daily Telegram delivery. <br>
Mitigation: Run setup only when recurring delivery is desired, verify the chat ID and account ID before use, and remove the generated ~/.openclaw/cron/zenquote-daily-*.json file to stop delivery. <br>
Risk: The skill depends on an external quote API and its documented rate limits. <br>
Mitigation: Expect network/API availability constraints and keep requests within the documented 5 requests per 30 seconds limit. <br>


## Reference(s): <br>
- [ClawHub ZenQuote Skill](https://clawhub.ai/chrisluo5311/zenquote) <br>
- [ZenQuotes API Documentation](https://docs.zenquotes.io/) <br>
- [ZenQuotes API](https://zenquotes.io/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown text for quotes, JSON for image and setup responses, and cron configuration for scheduled delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the ZenQuotes.io free API with attribution in outputs; documented API limits are 5 requests per 30 seconds.] <br>

## Skill Version(s): <br>
1.0.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
