## Description: <br>
Markets orchestration connects ESPN live schedules with Kalshi and Polymarket prediction markets for unified dashboards, odds comparison, entity search, and bet evaluation across platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonelli182](https://clawhub.ai/user/antonelli182) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compare sports schedules, sportsbook odds, and prediction-market prices across ESPN, Kalshi, and Polymarket. It supports market discovery, price normalization, arbitrage checks, and bet-evaluation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market prices, liquidity, fees, rules, and event availability can change quickly, making odds comparisons or arbitrage claims stale. <br>
Mitigation: Verify current prices, liquidity, fees, and market rules directly on the relevant platform before acting on any recommendation. <br>
Risk: The skill can produce betting recommendations, Kelly sizing, and arbitrage claims that users may mistake for guaranteed financial advice. <br>
Mitigation: Treat outputs as analysis guidance only, apply independent judgment, and confirm local legal restrictions before placing any wager or trade. <br>
Risk: The skill depends on an external sports-skills CLI or SDK and third-party data sources. <br>
Mitigation: Install the CLI or SDK only from a trusted source and expect partial results or warnings when ESPN, Kalshi, or Polymarket data is unavailable. <br>


## Reference(s): <br>
- [Markets Orchestration API Reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/antonelli182/sports-skills-markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown text with shell commands, Python snippets, tabular market summaries, and JSON-shaped examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include odds comparisons, normalized probabilities, arbitrage allocations, expected value, Kelly sizing, warnings, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
