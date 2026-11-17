## Description:

Use Volc Engine AI to generate, edit, batch produce, and create variations of images with customizable styles and sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Volc Engine Ark image APIs for text-to-image generation, image editing, batch generation, and image variations with selected styles and sizes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-edit inputs can read arbitrary local files or internal URLs and send their contents to an external image API.

Mitigation: Use the skill only in a constrained runtime and do not pass private documents, secrets, internal URLs, or regulated images as inputs.

Risk: Outbound API calls depend on a Volcengine credential and can incur spend or expose data if misconfigured.

Mitigation: Use a narrowly scoped Volcengine key, a fixed trusted API base URL, outbound network restrictions, and spending limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/skills/volc-image-gen)
- [Volc Engine Ark Console](https://console.volcengine.com/ark)

## Skill Output:

**Output Type(s):** [JSON, Files, API Calls, Guidance]

**Output Format:** [JSON result objects with image URLs, local file paths, usage metadata, and error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download generated or input images to local temporary storage and uses a one-hour cache for generation results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
