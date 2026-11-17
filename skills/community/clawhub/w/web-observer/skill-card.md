## Description:

Monitors website uptime and recovery, and optionally reports Vercel errors, Core Web Vitals, and GA4 traffic through companion skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anatoli-iliev](https://clawhub.ai/user/anatoli-iliev)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners and developers use this skill to check site availability, configure outage and recovery alerts, and ask about Vercel errors or GA4 traffic when the corresponding companion skills are installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled monitoring stores configuration and alert state locally.

Mitigation: Review local configuration and scheduled jobs before enabling monitoring.

Risk: Optional Vercel and GA4 reporting uses companion skills and credentials.

Mitigation: Review companion skills before enabling them and use least-privilege credentials where possible.

Risk: Application log messages may contain sensitive information when included in alerts.

Mitigation: Keep includeMessages disabled unless sharing application log text is acceptable.

## Reference(s):

- [Web Observer on ClawHub](https://clawhub.ai/anatoli-iliev/skills/web-observer)
- [Web Observer project homepage](https://github.com/anatoli-iliev/web-observer)
- [Vercel Insights companion skill](https://github.com/anatoli-iliev/openclaw-vercel-insights)
- [GA4 companion skill](https://github.com/anatoli-iliev/open-ga4)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration guidance]

**Output Format:** [Plain-text reports and alerts, with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled alerts report outages and recovery; Vercel and GA4 reports require separately installed companion skills.]

## Skill Version(s):

0.2.1 (source: frontmatter, package.json, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
