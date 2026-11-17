## Description:

Generate and edit images with Imagen 4 through RunAPI for one-off image tasks or SDK-based application integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, edit, or transform images with Imagen 4 through RunAPI, using the CLI for one-off deliverables or SDK guidance for application integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may upload user-selected media inputs to RunAPI for generation or editing.

Mitigation: Confirm that media inputs are intended for upload before submitting requests, and use only the authenticated RunAPI account selected by the user.

Risk: RunAPI requests may create paid tasks.

Mitigation: Submit each task once, retry only under the documented safe conditions, and require user authorization before replacing a failed paid request.

Risk: Authentication is required before submitting RunAPI work.

Mitigation: Check RunAPI authentication status first and use RUNAPI_API_KEY or an explicitly requested login flow before creating tasks.

## Reference(s):

- [RunAPI Imagen 4 homepage](https://runapi.ai/models/imagen-4)
- [RunAPI Imagen 4 documentation](https://runapi.ai/models/imagen-4.md)
- [RunAPI Google provider overview](https://runapi.ai/providers/google.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Imagen 4 SDK](https://github.com/runapi-ai/imagen-4-sdk)
- [Imagen 4 variant](https://runapi.ai/models/imagen-4/imagen-4.md)
- [Imagen 4 Fast variant](https://runapi.ai/models/imagen-4/fast.md)
- [Imagen 4 Pro Remix Image variant](https://runapi.ai/models/imagen-4/pro-remix-image.md)
- [Imagen 4 Ultra variant](https://runapi.ai/models/imagen-4/ultra.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON request files, shell commands, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task metadata JSON, result JSON, and verified image/* deliverables.]

## Skill Version(s):

0.2.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
