## Description:

SEO analysis and optimization via RankForge API for site audits, keyword research, competitor analysis, backlink checks, and search ranking optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

External users, developers, and SEO practitioners use this skill to request RankForge API workflows for site audits, keyword research, competitor analysis, backlink checks, and ranking optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SEO URLs and analysis payloads are sent to the RankForge service.

Mitigation: Use the skill only with SEO data approved for submission to the RankForge API.

Risk: The helper script can obtain and print an API key when auto-signup is used.

Mitigation: Set RANKFORGE_API_KEY directly and avoid running auto-signup in logged CI or shared agent sessions.

Risk: RANKFORGE_API_URL can redirect requests and credentials to a different endpoint.

Mitigation: Override RANKFORGE_API_URL only when the endpoint is trusted.

## Reference(s):

- [RankForge skill page](https://clawhub.ai/jbennett111/skills/rankforge)
- [RankForge OpenAPI schema](https://anton.vosscg.com/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RankForge API key for analysis requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
