## Description:

Text-to-image generation using the Doubao Seedream model, with concurrent batch generation and gallery output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aowind](https://clawhub.ai/user/aowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate one or more images from text prompts through Doubao Seedream and receive saved image files plus a local gallery preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to the external Volcengine/Doubao service.

Mitigation: Avoid secrets, personal data, or sensitive business information in prompts.

Risk: The skill handles an ARK API key.

Mitigation: Prefer ARK_API_KEY from a protected environment over passing keys on the command line.

Risk: The generated gallery page has a reported HTML-injection flaw.

Mitigation: Open generated index.html only for prompts you controlled or reviewed.

Risk: Dependencies are not pinned in the artifact.

Mitigation: Pin and review dependencies before routine use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aowind/skills/sjht-doubao-image-gen)
- [Volcengine Ark Console](https://console.volcengine.com/ark)
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions]

**Output Format:** [JPEG image files, prompts.json, index.html gallery, and Markdown image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ARK API key for live generation; dry-run mode prints parameters without calling the API.]

## Skill Version(s):

1.0.0 (source: changelog and server release metadata, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
