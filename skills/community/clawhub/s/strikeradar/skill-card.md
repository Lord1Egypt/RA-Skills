## Description: <br>
Monitors US-Iran strike probability using open-source indicators including news, connectivity, oil prices, flight traffic, military tanker detection, weather, Polymarket odds, and Pentagon activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexpolonsky](https://clawhub.ai/user/alexpolonsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to query current StrikeRadar signals from the terminal and receive either human-readable status output or JSON suitable for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strike probability scores concern a sensitive geopolitical topic and may be mistaken for intelligence, safety, financial, or personal decision advice. <br>
Mitigation: Treat the scores as informational only and confirm any important conclusions with authoritative sources before acting. <br>
Risk: The skill depends on live responses from api.usstrikeradar.com, so output can be stale, unavailable, or affected by upstream service issues. <br>
Mitigation: Check timestamps, handle command errors, and avoid relying on a single run for time-sensitive decisions. <br>


## Reference(s): <br>
- [StrikeRadar](https://usstrikeradar.com/) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [ClawHub skill page](https://clawhub.ai/alexpolonsky/strikeradar) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text for interactive use and JSON with next_actions when piped] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npx on darwin or linux; queries api.usstrikeradar.com and does not require credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
