## Description:

Generates cover images, posters, campaign creatives, and image variations through SiliconFlow text-to-image and image-to-image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to generate social covers, promotional posters, concept visuals, and variations from reference images. It is not intended for OCR, visual question answering, text chat, code help, or high-precision document layout reconstruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, image base64 data, or local image file contents may be uploaded to SiliconFlow.

Mitigation: Use only prompts and images approved for upload to SiliconFlow, and avoid private or sensitive image paths unless that upload is acceptable.

Risk: The scripts may use a generic API_KEY when SILICONFLOW_API_KEY is not set, which could send an unrelated service token to SiliconFlow.

Mitigation: Configure a dedicated SILICONFLOW_API_KEY for this skill and avoid running it in sessions where API_KEY contains another provider's credential.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangziiiiii/skills/siliconflow-image-generator)
- [SiliconFlow Console](https://siliconflow.cn)
- [SiliconFlow Image Generation API Endpoint](https://api.siliconflow.cn/v1/images/generations)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls SiliconFlow image generation endpoints and may return image URLs or service error payloads.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
