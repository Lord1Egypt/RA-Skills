## Description:

Zuimei Zjz Api helps agents use the Zuimei ID photo API for ID-photo generation, portrait and background segmentation, face enhancement, print layouts, and image resizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flaravel](https://clawhub.ai/user/flaravel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route photo-processing requests to a third-party API for ID photos, portrait cutouts, background replacement, face enhancement, printable layouts, and image format or size changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive portraits or ID-style photos may be uploaded to a third-party API.

Mitigation: Ask for explicit confirmation before uploading user images and avoid sending any photo that is not required for the requested operation.

Risk: The artifact includes shared API credentials for testing.

Mitigation: Replace shared credentials with scoped user-controlled credentials stored in environment variables or a secret manager.

Risk: Processed image URLs are returned by the third-party service and may expose sensitive outputs if shared broadly.

Mitigation: Share result URLs only with the requesting user and avoid logging or reposting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flaravel/skills/zuimei-zjz-api)
- [Publisher profile](https://clawhub.ai/user/flaravel)
- [Zuimei official website](https://zuimei.huipai.vip)
- [API documentation](API.md)
- [OpenAPI specification](openapi.yaml)
- [SDK examples](examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python or shell snippets and JSON API response references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return third-party image URLs, enhanced image URLs, transparent PNG URLs, or layout and edit metadata from the API.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
