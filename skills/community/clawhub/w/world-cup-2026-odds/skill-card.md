## Description: <br>
Aggregate FIFA World Cup 2026 odds across sportsbooks and prediction markets. Track outright winner futures, group stage odds, and match lines. Compare Polymarket prices vs traditional book futures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up FIFA World Cup 2026 betting futures, group or match odds, market favorites, underdogs, and pricing differences across sportsbook and prediction-market sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill passes ODDS_API_KEY to The Odds API in request URLs, which may expose the key through logs, shell history, or shared command output. <br>
Mitigation: Use a limited-purpose API key, avoid sharing full request URLs or command histories, and rotate the key if it may have been exposed. <br>
Risk: World Cup odds are time-sensitive and may be incomplete or stale if the external odds provider is unavailable or returns partial data. <br>
Mitigation: Treat returned odds as a live external data point and verify important betting or business decisions against the source market before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rsquaredsolutions2026/world-cup-2026-odds) <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [AgentBets](https://agentbets.ai) <br>
- [OpenClaw World Cup 2026 Odds Skill Guide](https://agentbets.ai/guides/openclaw-world-cup-2026-odds-skill/) <br>
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-processing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and an ODDS_API_KEY environment variable for live odds lookups.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
