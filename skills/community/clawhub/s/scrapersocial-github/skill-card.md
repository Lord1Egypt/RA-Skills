## Description:

GitHub data toolkit via ScraperSocial for public repositories, commits, contributors, issues, releases, languages, user profiles, repository search, and trending projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to look up public GitHub project and profile data for dependency evaluation, issue triage, release research, and discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the ScraperSocial API key to ScraperSocial.

Mitigation: Use a dedicated key and grant access only if this third-party service is acceptable.

Risk: Public GitHub lookups consume ScraperSocial credits.

Mitigation: Limit query scope and pagination, and monitor credit usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nikhonit/skills/scrapersocial-github)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON responses, which the agent can summarize in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public GitHub data only; paginated requests are limited to 50 items per call.]

## Skill Version(s):

1.0.4 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
