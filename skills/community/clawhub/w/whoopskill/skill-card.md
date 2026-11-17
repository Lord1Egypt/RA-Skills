## Description:

WHOOP CLI with health insights, trends analysis, and data fetching (sleep, recovery, HRV, strain).

This skill is ready for commercial/non-commercial use.

## Publisher:

[koala73](https://clawhub.ai/user/koala73)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to authenticate with WHOOP, fetch personal sleep, recovery, strain, workout, body, and profile data, and produce summaries, trends, and insights for health tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses sensitive WHOOP health and profile data.

Mitigation: Install only when that access is acceptable, and keep CLI output off shared machines, logs, backups, and repositories.

Risk: WHOOP client credentials and local OAuth tokens can grant continued access to user data.

Mitigation: Protect WHOOP_CLIENT_ID, WHOOP_CLIENT_SECRET, WHOOP_REDIRECT_URI, and ~/.whoop-cli/tokens.json; use whoopskill auth logout or revoke the app when access should stop.

## Reference(s):

- [Whoop Skill on ClawHub](https://clawhub.ai/koala73/skills/whoopskill)
- [whoopskill npm package](https://www.npmjs.com/package/whoopskill)
- [WHOOP Developer Portal](https://developer.whoop.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON by default, with optional human-readable text summaries, trends, and insights.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WHOOP API credentials and OAuth login; fetched data may include personal health and profile information.]

## Skill Version(s):

1.1.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
