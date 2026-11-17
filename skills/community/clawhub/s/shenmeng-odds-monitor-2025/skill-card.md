## Description:

Monitors sports betting line and odds movement for football, basketball, and related markets, highlighting abnormal fluctuations, bookmaker shifts, trend history, and alert-worthy signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor sports odds and betting line movement, compare market changes across platforms, review trend history, and receive alerts about abnormal movements or possible betting signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled billing module exposes a hard-coded SkillPay API key.

Mitigation: Remove the embedded key, rotate it before any release or deployment, and use deployment-specific secret storage such as environment variables or a managed secrets service.

Risk: The billing flow can perform user-linked charge operations without clear per-charge user control.

Mitigation: Authenticate billing identity server-side and require explicit user approval before each charge.

Risk: The skill can make outbound odds-provider and billing requests and retain odds snapshots in a local SQLite database.

Mitigation: Disclose required network endpoints, protect ODDS_API_KEY and SkillPay user identifiers, and define data retention and deletion practices for local SQLite files.

Risk: Odds-monitoring output may be mistaken for betting advice.

Mitigation: Present outputs as data monitoring and analysis only, preserve the disclaimer that reports are not betting advice, and require users to make independent decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-odds-monitor-2025)
- [The Odds API](https://the-odds-api.com/)
- [The Odds API v4 endpoint](https://api.the-odds-api.com/v4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown monitoring reports with signal summaries, command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese-language output, odds snapshots, trend summaries, alert recommendations, and local SQLite-backed report data.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact _meta.json, config.json, and __init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
