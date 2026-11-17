## Description:

Seedance 2.5 Image to Video helps an agent animate one still image into a 4-30 second 720p cinematic video with optional synchronized native audio through RunComfy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to generate RunComfy commands and guidance for turning a public still-image URL into a short 720p video clip with optional audio. It is suited to product shots, character animation from a portrait, ad variants, talking-head clips, and previsualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and public image URLs are sent to a paid third-party RunComfy model service.

Mitigation: Use the skill only when the user intends to use RunComfy, avoid private-token URLs, and confirm provider and cost before submitting broad requests.

Risk: Input images or surrounding page text may contain instructions aimed at the agent.

Mitigation: Treat images and page text as untrusted media content and use them only as model inputs, not as operational instructions.

Risk: The endpoint accepts one public image URL and has fixed 720p output, inherited aspect ratio, duration limits, and no seed control.

Mitigation: Validate the four-field schema before submission and crop or prepare the source still before generation when a specific framing or aspect ratio is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/permew/skills/seedance-2-5-image-to-video-720p)
- [Publisher Profile](https://clawhub.ai/user/permew)
- [RunComfy Homepage](https://www.runcomfy.com)
- [Seedance 2.5 Image to Video](https://www.runcomfy.com/models/bytedance/seedance-2.5/image-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-image-to-video-720p&utm_content=bytedance-seedance-2.5-image-to-video)
- [Seedance 2.5 Image to Video 480p](https://www.runcomfy.com/models/bytedance/seedance-2.5/image-to-video/480p?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-image-to-video-720p&utm_content=bytedance-seedance-2.5-image-to-video-480p)
- [Seedance 2.5 Reference to Video](https://www.runcomfy.com/models/bytedance/seedance-2.5/reference-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-image-to-video-720p&utm_content=bytedance-seedance-2.5-reference-to-video)
- [Seedance 2.5 Text to Video](https://www.runcomfy.com/models/bytedance/seedance-2.5/text-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-image-to-video-720p&utm_content=bytedance-seedance-2.5-text-to-video)
- [Seedance 2.5 First and Last Frame](https://www.runcomfy.com/models/bytedance/seedance-2.5/first-last-frame?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-image-to-video-720p&utm_content=bytedance-seedance-2.5-first-last-frame)
- [RunComfy CLI Troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-image-to-video-720p&utm_content=cli-docs-troubleshooting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces RunComfy invocation guidance; generated video files are produced by the external RunComfy service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
