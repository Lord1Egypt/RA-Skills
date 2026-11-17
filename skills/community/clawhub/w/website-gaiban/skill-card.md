## Description:

An end-to-end website redesign orchestration skill for redesigning existing sites, upgrading visual style, restructuring information architecture, and migrating old-site content into a new website workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, site operators, and developers use this skill to orchestrate full corporate website redesigns from audit and strategy through information architecture, page planning, content migration, SEO/GEO, lead generation, preview, and publish.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires unpinned third-party dependency skills before operating on a website.

Mitigation: Review or pin the four dependency skills and require explicit approval before fetching or invoking them.

Risk: The workflow may use site write credentials for backup, migration, generation, publish, delete, or cache-clear actions.

Mitigation: Use short-lived, site-specific MCP tokens with minimum permissions, confirm the target site, and complete backups before write or publish operations.

Risk: The skill references a commercial trial link that may not be required for every workflow.

Mitigation: Treat the trial link as optional unless the selected website platform workflow specifically requires it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hsqduron/skills/website-gaiban)
- [Redesign templates and checklists](references/redesign-templates.md)
- [Dependent skill: 建站助手](https://skillhub.cn/skills/org-b0bh4w8c/yunzhi-jian-zhan)
- [Dependent skill: SEO](https://skillhub.cn/skills/org-b0bh4w8c/yunzhi-seo-skill)
- [Dependent skill: GEO](https://skillhub.cn/skills/org-b0bh4w8c/yun-zhi-geo)
- [Dependent skill: website lead generation](https://skillhub.cn/skills/org-b0bh4w8c/yun-zhi-website-leadgen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown plans, checklists, reports, code snippets, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before site write, publish, delete, or cache-clear operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
