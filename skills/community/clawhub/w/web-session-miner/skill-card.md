## Description:

Web Session Miner guides an agent to use a logged-in browser session through browser-skill to collect account-authorized web data and produce structured JSON or HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyanjun](https://clawhub.ai/user/xiyanjun)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and due-diligence users can use this skill to automate collection of business registry, ownership, investment, and related web data that their logged-in account is authorized to view. It is intended for browser-mediated data collection workflows where site-specific recipes define login checks, URL patterns, extraction targets, and reporting expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reuses a live logged-in browser profile and can access or copy data visible to that account.

Mitigation: Use a dedicated browser profile and least-privileged account, and confirm the target site and account before each run.

Risk: Bulk browser scraping or avoiding official API billing may conflict with site terms or provider requirements for programmatic access.

Mitigation: Review the target site's terms and robots policy, avoid bulk scraping unless permitted, control request frequency, and prefer official APIs when required.

Risk: Collected business or relationship data can be incomplete, stale, or scoped to only visible pages.

Mitigation: Report the collection time, source site, login context, and data range, and avoid inferring facts that were not directly collected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiyanjun/skills/web-session-miner)
- [Publisher profile](https://clawhub.ai/user/xiyanjun)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Qichacha recipe](artifact/recipes/qcc.md)
- [Tianyancha recipe](artifact/recipes/tyc.md)
- [Data sanitization audit](artifact/AUDIT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript extraction snippets, structured JSON, and HTML report guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data source, logged-in session source, collection time, and data scope when reporting collected information.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
