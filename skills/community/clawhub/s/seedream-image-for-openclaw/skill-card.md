## Description:

Uses the Volcengine Seedream-4.5 API to generate high-quality images for text-to-image, image-to-image, and related image series workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crabfishxy](https://clawhub.ai/user/crabfishxy)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate images through Volcengine Seedream from prompts, reference images, or sequential image-generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid Volcengine API key can be exposed when passed with --api-key in shell history, process listings, or logs.

Mitigation: Prefer VOLC_API_KEY or a managed secret store, and use a dedicated least-privileged Volcengine key.

Risk: Private image data can be sent to Volcengine when reference images or base64 input are used.

Mitigation: Avoid sending private images as base64 unless that transfer is intended and approved.

Risk: Requests are sent to Volcengine's cn-beijing endpoint.

Mitigation: Confirm the endpoint is acceptable for the intended data, users, and deployment geography before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crabfishxy/skills/seedream-image-for-openclaw)
- [Volcengine image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown with generated image links and MEDIA_URL text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs image URLs when the API returns them; does not download images unless the user asks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
