## Description: <br>
Daily check-in pattern for Simmer agents. One API call returns portfolio, risk alerts, and opportunities across all venues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch and summarize Simmer portfolio briefings across $SIM, Polymarket, and Kalshi. It is intended for heartbeat or user-requested check-ins that surface risk alerts, venue-level PnL, and opportunities without dumping raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Simmer API key that can access portfolio briefings across linked venues. <br>
Mitigation: Store SIMMER_API_KEY as a secret and avoid logging raw briefing responses. <br>
Risk: Briefing actions and opportunities could influence trading decisions if another workflow acts on them automatically. <br>
Mitigation: Require explicit user confirmation before any separate trading workflow acts on briefing recommendations. <br>
Risk: Mixing virtual $SIM values with USDC or USD venue values could mislead users about real-money exposure. <br>
Mitigation: Keep $SIM and real-money venue sections separate and read PnL from each venue block. <br>


## Reference(s): <br>
- [Simmer Briefing API reference](https://docs.simmer.markets) <br>
- [Simmer FAQ](https://docs.simmer.markets/faq) <br>
- [ClawHub skill page](https://clawhub.ai/simmer/simmer-briefing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and REST examples for producing a concise portfolio briefing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and the simmer-sdk package; briefing output should separate virtual $SIM from real-money venues.] <br>

## Skill Version(s): <br>
0.1.4 (source: evidence.release.version and metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
