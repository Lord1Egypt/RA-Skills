## Description:

Monitor line movements at sharp sportsbooks (Pinnacle, Circa, Bookmaker), detect steam moves, reverse line movement, and significant implied probability shifts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to collect sportsbook line snapshots and reason about line movement, sharp action, steam moves, and reverse line movement signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an Odds API key when requesting sportsbook odds.

Mitigation: Keep shell tracing and verbose logging off around commands, restrict or rotate the key when needed, and avoid sharing captured command output that may expose credentials.

Risk: The skill creates local odds snapshot files in a configurable directory.

Mitigation: Use a trusted SHARP_SNAPSHOT_DIR value and review filesystem permissions for stored snapshot data.

Risk: Untrusted SPORT_KEY or snapshot path values could send unintended API requests or write files to unexpected locations.

Mitigation: Use known SPORT_KEY values and trusted environment variable settings before running the generated commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rsquaredsolutions2026/skills/sharp-line-detector)
- [The Odds API](https://the-odds-api.com/)
- [AgentBets Sharp Line Detector Tutorial](https://agentbets.ai/guides/openclaw-sharp-line-detector-skill/)
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline bash commands and JSON snapshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ODDS_API_KEY and optional SPORT_KEY, SHARP_SPREAD_THRESHOLD, SHARP_ML_THRESHOLD, and SHARP_SNAPSHOT_DIR settings.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
