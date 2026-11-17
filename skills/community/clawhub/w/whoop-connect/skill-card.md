## Description:

Connects WHOOP wearable data to OpenClaw so an agent can fetch and store recovery, sleep, HRV, strain, workout, profile, and body-measurement data locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[belugary](https://clawhub.ai/user/belugary)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect their own WHOOP account to an agent for local recovery, sleep, strain, workout, and trend queries. It supports setup guidance, OAuth authorization, data synchronization, optional webhook handling, and bilingual summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses and stores sensitive WHOOP health, profile, body, and OAuth token data locally.

Mitigation: Review before installing, restrict access to local WHOOP data files, and treat the local database and token file as sensitive.

Risk: The optional public webhook server is documented without authentication, rate limiting, or replay protection.

Mitigation: Avoid enabling public webhooks unless authentication, rate limiting, and replay protection are added at the deployment boundary.

Risk: Credential examples place WHOOP client credentials in shell or service configuration.

Mitigation: Keep credentials out of shared shell profiles and systemd unit files, and use a private secret-management mechanism where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/belugary/skills/whoop-connect)
- [Project Homepage](https://github.com/Belugary/whoop-connect)
- [Setup Guide](references/setup-guide.md)
- [WHOOP API v2 Reference](references/api-reference.md)
- [Webhook Events](references/webhook-events.md)
- [WHOOP Developer Portal](https://developer.whoop.com)
- [WHOOP API Documentation](https://developer.whoop.com/api)
- [WHOOP Data Concepts](https://developer.whoop.com/docs/developing/user-data/recovery)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown summaries, optional JSON records, and setup or synchronization commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local WHOOP configuration, OAuth token, SQLite database, webhook heartbeat, and synchronization logs under the user's local WHOOP directory.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
