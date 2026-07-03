## Description: <br>
Accesses Polymarket public market data to search, monitor, summarize, and paper-trade prediction markets with local watchlists and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket odds, volume, momentum, resolution timing, and category activity without connecting a wallet. It also supports local watchlists, alerts, and simulated paper positions for tracking predictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data and paper-trading output could be mistaken for financial advice or real trading capability. <br>
Mitigation: Treat outputs as informational only; the artifact states paper trading is local simulation and real wallet-backed trading is not implemented. <br>
Risk: The skill makes external unauthenticated HTTPS requests and stores watchlist and simulated portfolio data locally. <br>
Mitigation: Use only if external requests to Polymarket's public Gamma API and local files under ~/.polymarket/ are acceptable for the environment. <br>
Risk: An external setup guide link is included in the artifact. <br>
Mitigation: Review external guide content before following it and avoid adding wallet, account, or API secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-polymarket-trade) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket documentation](https://docs.polymarket.com) <br>
- [Step-by-step OpenClaw guide](https://telegra.ph/How-Building-a-Weather-Polymarket-Bot-with-OpenClaw-Skill-and-turn-100--8000-Step-by-Step-Guide-02-28-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style terminal text with market summaries and local JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses unauthenticated HTTPS GET requests to Polymarket's public Gamma API; watchlist and paper portfolio state are stored locally under ~/.polymarket/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
