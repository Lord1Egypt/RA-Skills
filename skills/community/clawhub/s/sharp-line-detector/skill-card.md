## Description: <br>
Monitor line movements at sharp sportsbooks (Pinnacle, Circa, Bookmaker), detect steam moves, reverse line movement, and significant implied probability shifts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect sports betting line movement, identify sharp-book changes, and capture odds snapshots for later comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends ODDS_API_KEY to The Odds API when fetching odds data. <br>
Mitigation: Use a normal sport key, store it only in the expected environment variable, and rotate or remove it if it is exposed. <br>
Risk: Odds snapshots are saved as local JSON files and may accumulate over time. <br>
Mitigation: Use a snapshot directory you control and delete old snapshot files when they are no longer needed. <br>
Risk: Sports odds and line-movement signals can be stale, incomplete, or misleading if used without review. <br>
Mitigation: Review current source data and treat generated line-movement analysis as decision support rather than a guarantee. <br>


## Reference(s): <br>
- [Sharp Line Detector on ClawHub](https://clawhub.ai/rsquaredsolutions2026/sharp-line-detector) <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [AgentBets Sharp Line Detector Guide](https://agentbets.ai/guides/openclaw-sharp-line-detector-skill/) <br>
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files, Analysis] <br>
**Output Format:** [Markdown with inline bash commands and JSON snapshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ODDS_API_KEY, optional threshold environment variables, and local snapshot files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
