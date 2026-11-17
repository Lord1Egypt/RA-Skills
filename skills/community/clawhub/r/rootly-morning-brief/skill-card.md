## Description:

Generates a Rootly morning incident digest for on-call operations, including active incidents, recent resolutions, current on-call assignments, and overdue action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanibu2777](https://clawhub.ai/user/yanibu2777)

### License/Terms of Use:

MIT-0

## Use Case:

SREs, incident commanders, and on-call engineers use this skill to produce a concise daily Rootly briefing for Slack or terminal review. It helps teams scan active incidents, resolved incidents from the last 24 hours, current on-call coverage, and overdue follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that bearer credentials can be forwarded to user-configurable or API-provided arbitrary URLs.

Mitigation: Use a read-only Rootly token and do not set ROOTLY_BASE_URL, --base-url, or --api-key-env to untrusted values until URL and credential-source scoping is hardened.

Risk: Generated incident and on-call digests may contain operationally sensitive information and can be posted by OpenClaw cron.

Mitigation: Pin Slack delivery to the intended private channel and avoid enabling private incidents unless they are required.

Risk: Live operation requires access to a Rootly API key.

Mitigation: Store the key in the documented secret-file path or an environment variable with least-privilege access, and use mock data for formatting tests when live Rootly access is not needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yanibu2777/skills/rootly-morning-brief)
- [Google SRE practical alerting guidance](https://sre.google/sre-book/practical-alerting/)
- [Atlassian incident communication tips](https://support.atlassian.com/statuspage/docs/incident-communication-tips/)
- [Atlassian incident response handbook](https://www.atlassian.com/incident-management/handbook/incident-response)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Slack-compatible Markdown text by default, or indented JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Phone-friendly digest; defaults to three items per section and public incidents unless private incidents are explicitly opted in.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
