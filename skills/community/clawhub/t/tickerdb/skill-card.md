## Description: <br>
TickerDB connects an agent to pre-computed categorical market context for stocks, crypto, and ETFs so it can answer market-data questions with smaller, structured API responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tickerdb](https://clawhub.ai/user/tickerdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-focused users use this skill to let an agent authenticate with TickerDB, retrieve categorical market summaries, search assets by market state, maintain watchlists, register webhooks, and schedule recurring market checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles email-based sign-in and a TickerDB API key. <br>
Mitigation: Use it only with a TickerDB account you trust, store the API key in the configured environment or secret store, and avoid pasting credentials into unrelated prompts. <br>
Risk: Watchlist and webhook commands can change saved account data. <br>
Mitigation: Review slash commands before sending them, especially watchlist removal and webhook removal commands, because the skill is designed to execute slash commands without an additional confirmation step. <br>
Risk: Registered webhook URLs and signing secrets can expose workflow endpoints if mishandled. <br>
Mitigation: Register only HTTPS endpoints you control, save webhook secrets securely when created, and verify TickerDB webhook signatures before processing payloads. <br>
Risk: Scheduled market-check workflows can repeatedly call the service and act on stale or misunderstood market context. <br>
Mitigation: Schedule checks after TickerDB's documented data refresh, review scheduled messages before enabling them, and treat the categorical data as factual context rather than trading advice. <br>


## Reference(s): <br>
- [TickerDB homepage](https://tickerdb.com) <br>
- [ClawHub skill page](https://clawhub.ai/tickerdb/tickerdb) <br>
- [TickerDB publisher profile](https://clawhub.ai/user/tickerdb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TICKERDB_KEY for authenticated API calls; TickerDB responses are structured JSON.] <br>

## Skill Version(s): <br>
0.1.97 (source: server-resolved ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
