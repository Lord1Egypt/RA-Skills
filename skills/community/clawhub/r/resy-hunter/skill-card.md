## Description: <br>
Monitor hard-to-get restaurant reservations on Resy, OpenTable, and Tock. Check availability, manage a watchlist, and get Telegram alerts when tables open up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shahedkhan30](https://clawhub.ai/user/shahedkhan30) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check restaurant reservation availability, manage a local watchlist, and configure alerts for openings across Resy, OpenTable, and Tock. The skill is read-only for bookings and presents links so users can book directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses real Resy and OpenTable account credentials and stores authentication material or sessions locally. <br>
Mitigation: Use dedicated accounts or tokens where practical, keep local data under ~/.openclaw/data/resy-hunter protected, and delete saved sessions or cached data when monitoring is no longer needed. <br>
Risk: Background monitoring can make repeated reservation-platform requests and send Telegram alerts containing reservation details. <br>
Mitigation: Enable cron monitoring only when needed, respect the documented request-rate limits, and avoid sharing logs or Telegram configuration that may contain credentials or reservation details. <br>
Risk: The security verdict is suspicious because the skill combines credentials, saved sessions, background execution, and Telegram credential reuse. <br>
Mitigation: Review the skill before installation, run it only on a trusted machine, and verify that its credential and alert behavior matches the user's intended monitoring workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shahedkhan30/resy-hunter) <br>
- [OpenTable & Tock Reference](references/platforms.md) <br>
- [Resy API Reference](references/resy-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, booking links, and JSON availability data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only booking posture; may create local watchlist and cron-monitoring configuration when requested.] <br>

## Skill Version(s): <br>
2.1.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
