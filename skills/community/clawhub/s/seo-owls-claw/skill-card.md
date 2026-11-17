## Description:

Generates SEO-optimized content, briefs, content plans, and deploy-ready HTML using persona-driven writing, brand profiles, locale-aware templates, and built-in SEO checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larya-dot-eu](https://clawhub.ai/user/larya-dot-eu)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, content strategists, marketers, and agency teams use this skill to research search intent, plan content clusters, draft SEO briefs, and produce CMS-ready text or HTML for pages such as blog posts, landing pages, product pages, FAQs, and social content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML, links, meta attributes, and JSON-LD may be publishable but still require review before deployment.

Mitigation: Review and sanitize generated HTML before publishing, with particular attention to links, metadata, and structured data.

Risk: The skill can produce or save SEO briefs and plans, which may overwrite or alter strategy artifacts if the destination is not checked.

Mitigation: Require explicit confirmation before saving, verify the exact destination path, and avoid overwriting existing briefs or plans unless intended.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/larya-dot-eu/skills/seo-owls-claw)
- [Publisher profile](https://clawhub.ai/user/larya-dot-eu)
- [Core skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Schema markup reference](artifact/SEO_CHECKS/schema-markup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown responses containing plain text, structured briefs/plans, or HTML code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Schema.org JSON-LD in generated HTML; brief and plan file saves should require explicit user confirmation.]

## Skill Version(s):

0.9.2 (source: server release metadata; artifact README and SKILL.md also indicate v0.9.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
