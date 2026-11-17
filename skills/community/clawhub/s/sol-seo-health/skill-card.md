## Description:

Daily SEO health check that validates blog posts for SEO completeness, checks sitemap, robots.txt, meta tags, broken links, and RSS feed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to run daily SEO health audits for thesolai.github.io blog posts, metadata, feeds, and site index files after builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured audit depends on an external seo-health.py script and a launchd job, so an installer should confirm the job targets only the intended site repository and expected log path.

Mitigation: Before installing, verify the referenced script and confirm the launchd job runs only for the intended thesolai.github.io repository and writes only logs/sol-seo.log.

Risk: The skill uses local file read/write access and HTTP requests while checking SEO files and links.

Mitigation: Review the requested permissions before deployment and run the audit with access limited to the intended site repository.

## Reference(s):

- [Sol Seo Health ClawHub page](https://clawhub.ai/amrree/skills/sol-seo-health)
- [Publisher profile](https://clawhub.ai/user/amrree)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text reports with issue counts and individual problem listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write audit output to logs/sol-seo.log when the configured SEO check runs.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
