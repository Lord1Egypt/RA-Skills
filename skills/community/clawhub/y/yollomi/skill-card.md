## Description:

Generates images and videos through Yollomi's unified API across text-to-image, image-to-image, text-to-video, and image-to-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anichikage](https://clawhub.ai/user/anichikage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent to generate or transform images and videos with Yollomi models through one API interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the YOLLOMI_API_KEY, prompts, and media references to a custom API host when YOLLOMI_BASE_URL is set.

Mitigation: Leave YOLLOMI_BASE_URL unset for the default Yollomi host, or set it only to a trusted HTTPS endpoint.

Risk: Prompts, supplied image URLs, and video inputs are processed by a third-party service.

Mitigation: Avoid secrets, private internal URLs, regulated data, and sensitive images unless organizational policy allows that processing.

Risk: Server security evidence marks the release suspicious because configurable hosts can receive credentials and media data.

Mitigation: Review the configured endpoint and environment variables before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anichikage/skills/yollomi)
- [Yollomi API](https://yollomi.com)
- [Yollomi API Models Reference](models-reference.md)

## Skill Output:

**Output Type(s):** [API calls, JSON, Generated media links]

**Output Format:** [JSON responses containing generated image or video URLs and remaining credit metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YOLLOMI_API_KEY; optional YOLLOMI_BASE_URL changes the API host.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
