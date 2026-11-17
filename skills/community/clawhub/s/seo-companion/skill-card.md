## Description:

Deep SEO analysis and execution for on-page SEO, technical SEO, content strategy, local SEO, keyword research, and backlink risk/recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bedouijesser](https://clawhub.ai/user/bedouijesser)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, developers, and site operators use this skill to audit public pages and sites, diagnose SEO blockers, rewrite metadata, plan content opportunities, evaluate local SEO gaps, and review backlink risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL audit script follows redirects after checking the initial target, which can allow an apparently public URL to lead to an internal network page.

Mitigation: Use the skill only for public sites in an environment without sensitive internal network access, or update the audit script to block automatic redirects or validate every redirect destination.

Risk: Running audits against private, localhost, link-local, cloud metadata, or intranet targets can expose sensitive internal pages to the audit process.

Mitigation: Keep private and internal targets blocked by default, and run any intentional internal audit only in a trusted environment with explicit user approval.

Risk: Installing missing Python dependencies can alter the runtime environment.

Mitigation: Ask before installing dependencies and fall back to manual inspection when installation is not approved or appropriate.

## Reference(s):

- [SEO Companion on ClawHub](https://clawhub.ai/bedouijesser/skills/seo-companion)
- [On-Page SEO Reference](references/on-page.md)
- [Technical SEO Reference](references/technical.md)
- [Content Strategy & Keyword Reference](references/content-strategy.md)
- [Local SEO Reference](references/local-seo.md)
- [Link Building Reference](references/link-building.md)
- [Platform Playbooks](references/platform-playbooks.md)
- [Canada Local Notes](references/canada-local.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables, prioritized findings, rewrite options, and optional JSON from the audit script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact metadata rewrites, prioritized SEO roadmaps, and public URL audit results.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
