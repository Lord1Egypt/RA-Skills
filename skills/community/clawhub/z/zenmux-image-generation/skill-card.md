## Description:

Generate images via ZenMux API (Pro/Elite), including text-to-image, image-to-image, and multi-image reference fusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to generate or transform images through the ZenMux API with text prompts and optional reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected reference images, and API key authentication are sent to ZenMux.

Mitigation: Avoid confidential, regulated, or highly sensitive inputs unless ZenMux's data-handling terms fit the intended use.

Risk: The helper sends HTTP requests without explicit timeouts or response-size checks.

Mitigation: Add request timeouts and response-size controls before heavy or automated use.

## Reference(s):

- [ZenMux Vertex AI API endpoint](https://zenmux.ai/api/vertex-ai)
- [ClawHub skill page](https://clawhub.ai/dadaniya99/skills/zenmux-image-generation)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; generated images are written as PNG files by default.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZENMUX_API_KEY and a ZenMux Pro or higher plan.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
