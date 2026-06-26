## Description: <br>
LLM-driven daily stock analysis for A-share, Hong Kong, and U.S. watchlists, producing technical indicators, trend judgments, buy-signal scores, decision dashboards, and market review reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robottk](https://clawhub.ai/user/robottk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch market data, compute technical indicators, and generate AI-assisted daily stock analysis for selected A-share, Hong Kong, and U.S. securities. The resulting reports are for analysis support and are not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can download, update, and run mutable external code that was not part of the reviewed package. <br>
Mitigation: Review helper scripts before installation and prefer the bundled analyzer modules directly, or pin and inspect the external repository before running setup.sh, run.sh, or update.sh. <br>
Risk: Configured AI providers may receive portfolio, watchlist, and technical-analysis data. <br>
Mitigation: Use a revocable AI API key, keep config files private, and avoid sending sensitive portfolio or watchlist data to an AI provider you do not trust. <br>
Risk: Generated analysis can be mistaken for investment advice. <br>
Mitigation: Treat outputs as analysis support only and require human review before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robottk/stock-daily-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/robottk) <br>
- [OpenClaw market-data integration](https://github.com/chjm-ai/openclaw-market-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python dictionaries and formatted text or Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external market-data and AI-provider APIs when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
