## Description: <br>
Wyckoff Agent Skill guides setup and use of a Wyckoff A-share analysis workflow with CLI and optional MCP integration for market data checks, structural analysis, portfolio review, signal queries, and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youngcan-wang](https://clawhub.ai/user/youngcan-wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and configure the Wyckoff CLI, connect A-share market data sources and model credentials, and produce auditable Wyckoff-style market and portfolio analysis. It can also route operational requests to CLI commands for portfolio views, signals, recommendations, backtests, reports, dashboard access, sync, cleanup, updates, and optional MCP setup. <br>

### Deployment Geography for Use: <br>
Global, with a China A-share market focus <br>

## Known Risks and Mitigations: <br>
Risk: Installation guidance includes a remote shell installer and optional MCP registration, which can expand local tool access. <br>
Mitigation: Prefer the pip install path, inspect any remote installer before running it, and enable MCP only for clients the user trusts. <br>
Risk: The workflow handles passwords, API keys, and saved local credentials for market data, model providers, and the Wyckoff service. <br>
Mitigation: Use interactive entry or revocable keys, avoid pasting secrets into shared terminals, and protect the local Wyckoff credential file. <br>
Risk: Portfolio, sync, cleanup, update, and MCP registration commands can change account, portfolio, or local state. <br>
Mitigation: Require explicit user confirmation before portfolio changes, data sync or cleanup, updates, purchases, or MCP registration. <br>
Risk: Finance analysis and add, reduce, hold, exit, or switch suggestions may be incorrect or unsuitable for a user's situation. <br>
Mitigation: Treat outputs as decision-support analysis, review the data audit and assumptions, and require human judgment before acting on any recommendation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/youngcan-wang/wyckoff-agent-skill) <br>
- [Wyckoff Analysis Registration](https://wyckoff-analysis.pages.dev/) <br>
- [Tushare](https://tushare.pro/) <br>
- [TickFlow Registration](https://tickflow.org/auth/register?ref=5N4NKTCPL4) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with audit tables, Chinese status lines, portfolio action sections, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include data-source fallback notes, trading-session verdicts, chart-generation guidance, and explicit uncertainty when data is unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
