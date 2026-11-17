## Description:

Adds hats and headwear to avatar images by analyzing style, lighting, and head angle, then generating a matching accessory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ls569333469](https://clawhub.ai/user/ls569333469)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add generated hats or headwear to avatar images through an MCP tool or a local FastAPI endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The web API supports URL-based image loading, which can create exposure if deployed publicly.

Mitigation: Remove URL fetch support or enforce strict URL allowlisting before exposing the API.

Risk: Unauthenticated public API access can allow abuse, unexpected costs, or quota exhaustion.

Mitigation: Keep deployments private or add authentication, trusted CORS origins, request-size limits, rate limits, and spending or quota controls.

Risk: Avatar images and prompts are processed by Google Gemini.

Mitigation: Tell users not to submit sensitive personal images unless they accept that third-party data flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ls569333469/skills/the-clawcap)
- [Google Gemini image generation documentation](https://ai.google.dev/gemini-api/docs/image-generation#image-editing)

## Skill Output:

**Output Type(s):** [image, json, configuration]

**Output Format:** [PNG image through MCP, or base64-encoded PNG with JSON metadata through the API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY, an avatar image, and an accessory prompt.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
