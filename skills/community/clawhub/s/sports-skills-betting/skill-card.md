## Description: <br>
Betting analysis for odds conversion, de-vigging, edge detection, Kelly criterion, arbitrage detection, parlay analysis, and line movement using odds from sportsbook or prediction-market sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonelli182](https://clawhub.ai/user/antonelli182) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to analyze supplied sports betting odds or prediction-market probabilities for expected value, bet sizing, arbitrage, parlays, and line movement. It is intended for computation and interpretation after odds have been obtained from another source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect odds format or skipped de-vigging can produce misleading edge, expected-value, or Kelly outputs. <br>
Mitigation: Verify the odds format before analysis and de-vig sportsbook odds before comparing them with prediction-market prices. <br>
Risk: Kelly and edge analysis may influence gambling decisions. <br>
Mitigation: Independently verify inputs, use conservative bet sizing such as half-Kelly or quarter-Kelly, and follow applicable laws and platform rules. <br>
Risk: The skill does not fetch live odds, so stale or mismatched external prices can invalidate the analysis. <br>
Mitigation: Supply current odds or probabilities from trusted sources and ensure all prices refer to the same market, outcome, and time window. <br>


## Reference(s): <br>
- [Betting Analysis API Reference](references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/antonelli182/sports-skills-betting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, and concise betting-analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis depends on user-supplied odds or probabilities; the skill does not fetch live data or place bets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
