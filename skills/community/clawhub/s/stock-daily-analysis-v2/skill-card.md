## Description: <br>
Daily Stock Analysis v2.1 helps an agent analyze A-share, Hong Kong, and U.S. stocks with technical indicators, fundamental signals, market and sector reviews, LLM-assisted summaries, and optional notification delivery. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[same1317](https://clawhub.ai/user/same1317) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate daily stock analysis, batch stock reports, market and sector reviews, and strategy-oriented stock Q&A for research workflows. Outputs are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data, AI providers, and notification channels may receive portfolio, strategy, or credential-adjacent information when configured. <br>
Mitigation: Use limited-scope API keys and webhooks, enable only trusted delivery channels, and avoid sending confidential portfolio, client, or strategy details to external services. <br>
Risk: Setup and update scripts pull code from GitHub, which can change the executed code or dependencies. <br>
Mitigation: Review setup.sh and update.sh before running them, install in a virtual environment, and pin or lock dependencies. <br>
Risk: Generated stock analysis can be incomplete, stale, or misleading if market data or LLM output is wrong. <br>
Mitigation: Treat reports as research support only, verify outputs against trusted market sources, and require human review before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/same1317/stock-daily-analysis-v2) <br>
- [AkShare data source](https://github.com/akfamily/akshare) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw market-data skill](https://github.com/chjm-ai/openclaw-market-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON-like analysis objects, terminal text, Python function results, and notification payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external market data, LLM, webhook, chat, and SMTP services when configured.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
