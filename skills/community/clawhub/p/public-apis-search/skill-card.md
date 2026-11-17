## Description:

Search and discover public APIs from the public-apis directory using a bundled local database with keyword, category, authentication, HTTPS, and random discovery filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jijinbao-code](https://clawhub.ai/user/jijinbao-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API-consuming teams use this skill to quickly find public APIs, compare authentication and HTTPS requirements, browse categories, and identify API documentation links from a local catalog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional update command downloads refreshed source data from GitHub.

Mitigation: Run the update only in a trusted environment and review refreshed data before relying on it.

Risk: Search results link to third-party APIs that may require credentials, API keys, or personal data.

Mitigation: Review each third-party API's documentation, terms, and security posture before sending credentials or sensitive data.

Risk: The bundled local API directory can become stale between manual updates.

Mitigation: Refresh from the documented source and verify critical API details before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jijinbao-code/skills/public-apis-search)
- [public-apis repository](https://github.com/public-apis/public-apis)
- [public-apis README data source](https://raw.githubusercontent.com/public-apis/public-apis/master/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with command examples and plain-text API result listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bundled local JSON API directory; an optional update command fetches the public-apis README from GitHub.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
