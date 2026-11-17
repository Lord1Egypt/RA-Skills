## Description:

Generate a dark-theme static HTML status page with health checks, ping, SSL certificate validation, and uptime history for self-hosted services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to configure service checks, collect uptime and certificate status, and generate a self-contained HTML status page for self-hosted services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background execution can continue checking services without clear operational oversight.

Mitigation: Enable cron or LaunchAgent scheduling only with logging, documented removal steps, and a trusted, unchanged skill directory.

Risk: Generated status pages can expose service names, URLs, health state, and uptime history if published publicly.

Mitigation: Keep private infrastructure status pages in user-owned local or access-controlled locations and avoid public Gist publishing for sensitive services.

Risk: Service monitoring data is stored locally and may accumulate over time.

Mitigation: Use an appropriate history file location, review its contents before sharing, and prune old history when retention is not needed.

## Reference(s):

- [status-page-gen Setup Guide](references/setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/status-page-gen)
- [Publisher Profile](https://clawhub.ai/user/newageinvestments25-byte)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated HTML output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSON check results, uptime history, and a self-contained HTML status page when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
