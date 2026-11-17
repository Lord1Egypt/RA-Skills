## Description:

Verifies Today's Watermark Camera photo URLs through openapi.xhey.top and returns authenticity verdicts, tamper indicators, capture time, GPS coordinates, and location metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanmeishijie618](https://clawhub.ai/user/wanmeishijie618)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and developers use this skill to verify whether publicly reachable Today's Watermark Camera image URLs are authentic for insurance claims, attendance, construction acceptance, evidence review, and compliance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photo URLs are sent to openapi.xhey.top for verification, and successful results may include precise capture time and location metadata.

Mitigation: Use only publicly reachable, non-sensitive photo URLs when external verification is intended; avoid private, signed, internal, or sensitive links.

Risk: The bundled Feishu implementation logs sensitive photo and location-related data according to the security evidence.

Mitigation: Prefer the MCP server path and avoid the Feishu implementation until sensitive logging and weak default authorization configuration are removed.

Risk: The skill may initiate verification when image URLs are provided, which sends those URLs to an external service.

Mitigation: Use the tool only for explicit photo-authenticity workflows and make the external verification step clear to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanmeishijie618/skills/watermark-camera-verifier)
- [Publisher profile](https://clawhub.ai/user/wanmeishijie618)
- [Source homepage from ClawHub metadata](https://github.com/wanmeishijie618/trutu-photo-verify-mcp)
- [Today's Watermark Camera Trutu API documentation](https://docs.xhey.top/docs/trutu-build-api)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Analysis]

**Output Format:** [JSON text containing a task ID, task status, summary counts, per-photo verdicts, and optional capture metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts 1 to 10 publicly reachable photo URLs; can either wait for verification results or return a submitted task ID.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact frontmatter and package.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
