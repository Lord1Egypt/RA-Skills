## Description:

Looks up public Snapchat creator profiles through ScraperSocial and returns structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, researchers, and developers can check public Snapchat handles and incorporate profile details into cross-platform creator records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ScraperSocial API key is sent as bearer authorization to api.scrapersocial.com.

Mitigation: Use a dedicated API key and only install the skill if sharing that credential with ScraperSocial is acceptable.

Risk: Queried Snapchat handles are sent to ScraperSocial.

Mitigation: Only look up public handles that may be shared with this service.

Risk: Profile lookups may consume ScraperSocial API credits.

Mitigation: Confirm expected usage and available credits before repeated lookups.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-snapchat)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Structured data]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public profile data with a request ID; errors are returned as JSON.]

## Skill Version(s):

1.0.4 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
