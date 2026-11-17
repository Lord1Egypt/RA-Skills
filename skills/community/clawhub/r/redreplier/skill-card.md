## Description:

Monitor Reddit, Hacker News, X, Bluesky, and Facebook for keyword mentions of a product or website using the RedReplier API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarasshyn](https://clawhub.ai/user/tarasshyn)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw agents use this skill to monitor brand and website mentions across social platforms, review relevance-scored leads, manage keywords, and configure mention alerts through RedReplier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedReplier API token and makes authenticated requests to the service.

Mitigation: Use a dedicated, revocable token, send it only to the documented RedReplier API, and revoke or rotate it if exposed.

Risk: The security review was partial and left dependency advisories and network scope questions unresolved.

Mitigation: Review dependency versions and advisories, and confirm the plugin's network access fits the intended installation before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tarasshyn/skills/redreplier)
- [RedReplier](https://redreplier.com)
- [RedReplier API OpenAPI specification](https://ai.redreplier.com/ai-app/api/v1/openapi.json)
- [API reference](references/api-reference.md)
- [Mention filtering reference](references/mention-filtering.md)

## Skill Output:

**Output Type(s):** [API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline cURL and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
