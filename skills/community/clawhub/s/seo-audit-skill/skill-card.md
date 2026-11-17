## Description:

An SEO agent skill for quick, lightweight, default single-page SEO audits that performs basic on-page and site-level checks and outputs a structured basic SEO audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli1993](https://clawhub.ai/user/jeffli1993)

### License/Terms of Use:

MIT-0

## Use Case:

External users, clients, developers, and SEO practitioners use this skill for first-pass single-page SEO checks when only a live URL or limited page content is available. It helps agents gather basic site and page signals, apply bounded SEO judgment, and save a readable local audit report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-provided URLs from the local machine.

Mitigation: Use it only for URLs you are comfortable auditing from your environment, and avoid untrusted or attacker-supplied URLs until redirect and DNS SSRF handling are fixed.

Risk: The skill creates local HTML reports from fetched page data.

Mitigation: Review generated reports before sharing or opening them broadly, and treat report content from untrusted pages as potentially unsafe until HTML escaping is fixed.

Risk: Dependencies may drift in sensitive environments.

Mitigation: Pin dependencies before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffli1993/skills/seo-audit-skill)
- [seo-audit reference guide](references/REFERENCE.md)
- [HTML report template](assets/report-template.html)
- [Site-level check script](scripts/check-site.py)
- [Page-level check script](scripts/check-page.py)
- [Raw page fetcher](scripts/fetch-page.py)
- [Schema validation script](scripts/check-schema.py)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance plus a saved local HTML audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured JSON from helper scripts as evidence and saves reports under reports/<hostname>-<slug>-audit.html.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
