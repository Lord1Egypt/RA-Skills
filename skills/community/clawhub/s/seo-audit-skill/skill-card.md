## Description: <br>
An agent skill for quick, lightweight SEO audits of public URLs using basic on-page, site-level, trust-page, and JSON-LD checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli1993](https://clawhub.ai/user/jeffli1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce a first-pass SEO audit report for a public page when they need a fast, readable assessment rather than a deep technical audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to the audited site and may request sitemap URLs listed in robots.txt. <br>
Mitigation: Use it only for sites you are comfortable auditing from your environment and within the network boundaries described by the release security guidance. <br>
Risk: The generated SEO report may contain incomplete or misleading conclusions when public page signals are limited or JavaScript-rendered content is not visible. <br>
Mitigation: Review the generated HTML report before sharing it and treat it as a basic first-pass audit, not a replacement for a full technical SEO review. <br>


## Reference(s): <br>
- [Seo Audit Skill on ClawHub](https://clawhub.ai/jeffli1993/seo-audit-skill) <br>
- [Basic SEO Audit Reference Guide](artifact/references/REFERENCE.md) <br>
- [Basic SEO Audit Report Template](artifact/assets/report-template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a generated local HTML audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public web pages and writes reports to local files; review generated reports before sharing.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
