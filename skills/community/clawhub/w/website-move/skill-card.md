## Description:

Website Migration Orchestrator helps agents migrate an existing business website to a new platform while preserving content, URL mappings, 301 redirects, and SEO value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and website migration operators use this skill to plan and run full-site migrations from a source site to a target builder platform. It produces staged inventories, content mapping, static asset migration plans, URL and 301 mappings, SEO/GEO checks, and user-confirmed publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external third-party skills that may be unpinned or change independently.

Mitigation: Install only pinned and reviewed dependency skill versions before use, and verify the registered dependency names before invocation.

Risk: Broad source-site crawling and migration can access or copy content from the wrong site or from pages the operator is not authorized to migrate.

Mitigation: Require source-site ownership verification before any crawl, follow robots and rate limits, avoid private or login-gated content, and keep crawling in a network-restricted environment.

Risk: Target-site publishing and cache-clearing operations can modify production content.

Mitigation: Use a short-lived, narrowly scoped MCP token, confirm the target site before writes, and require explicit user confirmation for each write, overwrite, URL, cache, and go-live action.

Risk: 1:1 UI replication and migrated JavaScript can introduce copyright, trademark, or unsafe script risks.

Mitigation: Require copyright and rights confirmation for replication mode, maintain complaint-freeze handling, and manually review any JavaScript before publishing it on the new site.

## Reference(s):

- [Migration Templates](references/migration-templates.md)
- [Source Site Ownership Verification](references/source-site-ownership-verification.md)
- [ClawHub Skill Page](https://clawhub.ai/hsqduron/skills/website-move)
- [Builder Dependency Skill](https://skillhub.cn/skills/org-b0bh4w8c/jian-zhan)
- [SEO Dependency Skill](https://skillhub.cn/skills/org-b0bh4w8c/seo-skill)
- [GEO Dependency Skill](https://skillhub.cn/skills/org-b0bh4w8c/geo-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, tables, checklists, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration strategy summaries, inventories, content specifications, URL mappings, 301 redirect rules, SEO/GEO reports, and site-generation guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
