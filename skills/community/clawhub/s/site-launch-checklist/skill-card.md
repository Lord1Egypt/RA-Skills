## Description:

Pre-launch checklist for shipping a new website. Orchestrates analytics setup (GA4, PostHog, Google Search Console, Ahrefs), legal compliance, security headers and audit, SEO and GEO with keyword research validated against Google Trends (robots.txt, sitemaps, llms.txt, AI policy, schema markup, hreflang), copywriting consistency via a TONE.md and a humanizer pass in the matching language, OpenGraph and social previews, full favicon set with manifest, quality gates (Lighthouse, Core Web Vitals, WCAG accessibility, mobile testing), and setup of a weekly SEO agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers, site owners, and launch teams use this skill to run an interactive pre-launch audit for websites, apps, documentation sites, SaaS pages, paid courses, and portfolios. It helps verify infrastructure, analytics, legal/compliance posture, security headers, SEO/GEO readiness, social previews, favicons, quality gates, ecosystem links, and weekly SEO maintenance setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to install third-party skills or tools that are not pinned to immutable versions.

Mitigation: Require explicit user confirmation before each install and review or pin remote packages, skills, commits, and tools before use.

Risk: The weekly SEO maintenance agent may run on a recurring or headless schedule.

Mitigation: Run scheduled jobs only in a tightly sandboxed account with read-only credentials where possible and explicit approvals for shell commands, file writes, and outbound posting.

Risk: API credentials and Slack webhooks may be used for analytics, SEO, and reporting workflows.

Mitigation: Store credentials in a secrets manager or uncommitted environment configuration, limit credential scope, and review outbound reports before posting to external channels.

Risk: Security evidence marks the release suspicious because it combines remote installs, credential-backed calls, recurring agents, and outbound data flows.

Mitigation: Install only after reviewing the release, scan results, requested tools, and data-flow implications for the target workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/site-launch-checklist)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Source homepage](https://github.com/samber/cc-skills)
- [Decisions and matrices](references/decisions.md)
- [Templates](references/templates.md)
- [Weekly SEO maintenance sub-agent](references/weekly-seo-agent.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports, checklist guidance, inline shell commands, configuration snippets, and optional agent definition files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces phase-by-phase launch status with blockers, recommended fixes, optional improvements, and optional weekly SEO report files.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
