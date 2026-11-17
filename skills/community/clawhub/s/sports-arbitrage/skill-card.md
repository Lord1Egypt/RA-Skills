## Description:

Scans sports odds from traditional bookmakers through The Odds API to detect arbitrage opportunities, calculate implied probabilities and stake splits, and write qualifying results to JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this automaton to monitor sports bookmaker odds and surface candidate arbitrage opportunities with calculated stake splits. The output is intended for review before any real-world betting or trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real ODDS_API_KEY may be exposed through scheduler output, stdout logs, or request-related error details.

Mitigation: Run the skill only where logs are private, prefer a version that redacts apiKey values, and rotate any key that may have been logged.

Risk: The skill writes automated JSON results to a configurable RESULTS_FILE path.

Mitigation: Set RESULTS_FILE to a dedicated safe path with appropriate permissions before running scheduled scans.

Risk: The runtime dependency list does not pin the requests package version.

Mitigation: Pin and review dependencies in the deployment environment before installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mibayy/skills/sports-arbitrage)
- [The Odds API](https://the-odds-api.com)
- [The Odds API sport keys documentation](https://the-odds-api.com/sports-odds-data/sports-apis.html)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Stdout log messages and JSON results file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes arbitrage opportunity objects with match, sport, profit percentage, implied probability, outcome odds, stake split, guaranteed return, and detection timestamp.]

## Skill Version(s):

1.0.1 (source: server release evidence, SKILL.md frontmatter, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
