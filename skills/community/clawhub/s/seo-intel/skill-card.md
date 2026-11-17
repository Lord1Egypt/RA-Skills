## Description:

SEO Intel is a local SEO competitive intelligence tool that helps agents crawl sites, compare competitors, analyze keyword and content gaps, audit AI citability, and produce implementation-ready SEO actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ukkometa](https://clawhub.ai/user/ukkometa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO operators, content teams, and agent workflows use this skill to run website crawls, compare target and competitor coverage, identify technical and content gaps, and convert those findings into briefs, reports, or prioritized implementation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website crawling and persistent local SEO data can collect sensitive or unwanted site information.

Mitigation: Confirm crawl targets explicitly and run scans in an isolated environment without unrelated credentials.

Risk: Cloud-backed model analysis can send SEO findings to external model services when enabled.

Mitigation: Use cloud analysis only when acceptable for the project data, and choose deterministic or local analysis paths when external processing is not approved.

Risk: The artifact describes live Cloudflare Wrangler deployment workflows, and the security evidence notes weak approval gating for autonomous deploys.

Mitigation: Do not allow autonomous production deploys; require a diff, exact target confirmation, and explicit human approval before any Wrangler deploy.

Risk: Unpinned or changing package dependencies can alter crawl, analysis, or deployment behavior.

Mitigation: Pin package versions where possible before scans or automation runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ukkometa/skills/seo-intel)
- [SEO Intel Product Page](https://ukkometa.fi/en/seo-intel/)
- [Agent Integration Guide](artifact/AGENT_GUIDE.md)
- [Database Schema Reference](artifact/references/db-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, structured JSON or CSV exports, CLI commands, and implementation briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May crawl live websites, persist local SEO data, and use cloud-backed model analysis when enabled.]

## Skill Version(s):

1.5.21 (source: release evidence and SKILL.md heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
