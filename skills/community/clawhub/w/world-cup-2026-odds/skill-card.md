## Description:

Aggregates FIFA World Cup 2026 betting odds from sportsbooks and prediction markets into one unified view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up FIFA World Cup 2026 odds, futures, favorites, underdogs, and betting value across available markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls The Odds API with an API key that may appear in shell history, logs, or shared transcripts if users expose the full request URL.

Mitigation: Keep ODDS_API_KEY in an environment variable, avoid pasting expanded request URLs into logs or chats, and rotate the key if it is exposed.

Risk: Current evidence describes the skill as an outright World Cup winner futures lookup, not a complete sportsbook-versus-prediction-market comparison tool.

Mitigation: Set user expectations that coverage depends on available The Odds API markets and verify any unsupported group, match, or prediction-market requests before relying on results.

## Reference(s):

- [World Cup 2026 Odds Tracker on ClawHub](https://clawhub.ai/rsquaredsolutions2026/skills/world-cup-2026-odds)
- [The Odds API](https://the-odds-api.com/)
- [AgentBets OpenClaw World Cup 2026 Odds Skill Guide](https://agentbets.ai/guides/openclaw-world-cup-2026-odds-skill/)
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and JSON-derived odds summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and an ODDS_API_KEY credential for The Odds API.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
