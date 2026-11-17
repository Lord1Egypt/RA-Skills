## Description:

Guides URL structure optimization for SEO, including readable paths, site hierarchy, static URL patterns, parameter handling, and redirect planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO practitioners use this skill to plan or audit URL structures for readable paths, shallow hierarchy, multilingual URL organization, parameter handling, canonicalization, and redirects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad URL wording where a narrower slug, canonicalization, or robots.txt skill would be more appropriate.

Mitigation: Use a more specific skill for per-page slugs, canonical URL consolidation, robots.txt Clean-param guidance, or other narrower tasks.

Risk: The skill may read local project context files such as .claude/project-context.md or .cursor/project-context.md when they exist.

Mitigation: Keep those context files current and scoped to the site structure information needed for URL planning.

Risk: URL restructuring advice can affect SEO and traffic if applied without migration planning.

Mitigation: Review recommendations before implementation and create 301 redirect and canonicalization plans for changed URLs.

## Reference(s):

- [Alignify URL optimization](https://alignify.co/zh/seo/url-optimization)
- [Google URL guidelines](https://developers.google.com/search/docs/crawling-indexing/url-structure)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with URL structure recommendations, slug conventions, hierarchy plans, and redirect guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to local project context files when present; no executable code is bundled.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
