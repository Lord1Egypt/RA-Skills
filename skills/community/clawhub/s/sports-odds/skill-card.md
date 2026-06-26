## Description: <br>
Get live sports betting odds and compare lines across sportsbooks. Supports NFL, NBA, MLB, NHL, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianalloway](https://clawhub.ai/user/ianalloway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch live sports odds, compare moneylines, spreads, and totals across sportsbooks, and check API usage for The Odds API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided The Odds API key to make external API requests. <br>
Mitigation: Provide only the needed ODDS_API_KEY, avoid sharing unrelated secrets with the agent, and review commands before execution. <br>
Risk: Live odds requests can consume API quota and may return changing market data. <br>
Mitigation: Monitor request usage, cache responses when appropriate, and verify odds against an authoritative source before making business or betting decisions. <br>


## Reference(s): <br>
- [The Odds API](https://the-odds-api.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and an ODDS_API_KEY environment variable; commands call The Odds API and may consume account quota.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
