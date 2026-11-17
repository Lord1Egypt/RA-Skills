## Description:

WebsiteMonitor helps agents create a website HTTP monitoring system that checks target URLs every five minutes, stores HTTP status and latency data, and generates daily HTML availability reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yb0554](https://clawhub.ai/user/yb0554)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to scaffold a custom uptime monitor for one or more websites, with persistent history and daily reports covering availability, latency, status code distribution, and time-series trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Linux service setup can run a persistent monitor with excessive privileges.

Mitigation: Run the monitor as a dedicated non-root user and restrict writable directories before enabling the service.

Risk: Monitoring internal or sensitive endpoints may probe systems that were not intended for this monitor.

Mitigation: Validate and approve allowed target URLs before deployment, and avoid internal or sensitive endpoints unless explicitly authorized.

Risk: Generated reports may include target names, URLs, status data, and error strings.

Mitigation: Escape report values and review report storage and sharing paths for sensitive endpoint information.

Risk: Unpinned runtime dependencies can change monitor or report behavior over time.

Mitigation: Pin Python dependencies and review the external Chart.js dependency used by generated reports.

## Reference(s):

- [WebsiteMonitor ClawHub release](https://clawhub.ai/yb0554/skills/website-monitor-skill)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Python scripts, JSON configuration, systemd service examples, Docker configuration, and HTML report generation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
