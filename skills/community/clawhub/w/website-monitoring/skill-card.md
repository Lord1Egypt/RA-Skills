## Description:

Creates and manages Crawlora monitors for page or sitemap changes, with optional signed webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can create, inspect, update, and remove monitors for public pages or sitemaps, then receive alerts when content or URLs change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed Crawlora API key could allow unauthorized changes to monitors.

Mitigation: Keep CRAWLORA_API_KEY private and review monitor update and delete requests before execution.

Risk: Monitoring private or login-only URLs is unsupported and may expose sensitive targets.

Mitigation: Use publicly reachable URLs only; do not submit private or login-only URLs.

## Reference(s):

- [ClawHub website-monitoring release](https://clawhub.ai/crawlora-org/skills/website-monitoring)
- [Crawlora monitor endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and JSON monitor results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional signed webhook notifications on changes]

## Skill Version(s):

1.0.14 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
