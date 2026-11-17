## Description:

Betting analysis for odds conversion, de-vigging, edge detection, Kelly criterion, arbitrage detection, parlay analysis, and line movement using odds from external sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonelli182](https://clawhub.ai/user/antonelli182)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to analyze already-supplied sportsbook or prediction-market odds for expected value, stake sizing, arbitrage, parlays, and line movement. It is computation-only and does not fetch live odds or market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bet sizing, edge, EV, arbitrage, and Kelly outputs may be mistaken for guaranteed profit or financial advice.

Mitigation: Treat outputs as informational, verify inputs independently, use conservative bankroll limits, and follow applicable gambling laws and responsible-gambling safeguards.

Risk: Incorrect odds formats or skipped de-vigging can produce misleading edge calculations.

Mitigation: Confirm the odds format before analysis and de-vig sportsbook odds before comparing against prediction-market probabilities.

## Reference(s):

- [Betting Analysis API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/antonelli182/skills/sports-skills-betting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with computed betting-analysis results and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No network fetching; outputs depend on user-supplied odds and probabilities.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata.version is 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
