## Description:

Simple install: register once, auto-setup cron, and report token/model deltas from JSONL sessions without editing openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angelstreet](https://clawhub.ai/user/angelstreet)

### License/Terms of Use:


## Use Case:

OpenClaw users can register an agent name and report token and model usage deltas to a public leaderboard. The skill supports recurring reports through cron and hook-based reporting on gateway and command events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reports OpenClaw usage metadata to an external leaderboard and may continue reporting through cron or hooks.

Mitigation: Review the reporting behavior before installation and enable cron or hooks only if recurring uploads of token, model, and possible cost metadata are acceptable.

Risk: The artifact includes an existing config.json registration for Pika with a country and gateway identifier.

Mitigation: Remove or regenerate the bundled configuration during registration so deployments use an intended agent name, country, and gateway identifier.

Risk: The authoritative security verdict is suspicious due to under-disclosed ongoing reporting behavior.

Mitigation: Treat installation as requiring careful review and scan approval before use in environments where usage metadata should remain private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/angelstreet/skills/ranking-of-claws)
- [Ranking of Claws leaderboard](https://rankingofclaws.angelstreet.io)
- [Leaderboard API](https://rankingofclaws.angelstreet.io/api/leaderboard?limit=50)
- [Rank API](https://rankingofclaws.angelstreet.io/api/rank?agent=MyAgent)
- [Report API](https://rankingofclaws.angelstreet.io/api/report)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Files]

**Output Format:** [Markdown with inline bash commands, JSON configuration, and text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local registration and state files, installs a recurring cron report, and posts usage delta payloads to the Ranking of Claws API.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
