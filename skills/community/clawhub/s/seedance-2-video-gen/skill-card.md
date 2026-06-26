## Description: <br>
Seedance 2.0 AI video generation via EvoLink API with text-to-video, image-to-video, and reference-to-video modes that can use images, videos, audio, and automatic audio generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Seedance 2.0 video generation workflows, including text-to-video, image-to-video, and multimodal reference-to-video requests. It also helps configure required dependencies and the EVOLINK_API_KEY environment variable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EvoLink API key and may encourage handling credentials in normal agent chat or shell startup files. <br>
Mitigation: Set EVOLINK_API_KEY through a secure environment or secret manager, avoid pasting keys into chat, and do not store the key in plaintext shell files unless that storage is acceptable. <br>
Risk: Prompts, media URLs, callback URLs, and generated-task data are sent to EvoLink for video generation. <br>
Mitigation: Do not submit sensitive prompts, private media, internal endpoints, or privileged signed URLs unless sharing them with EvoLink is intended. <br>


## Reference(s): <br>
- [Seedance 2.0 API Parameters Reference](references/api-params.md) <br>
- [EvoLink Skills Homepage](https://github.com/EvoLinkAI/evolink-skills) <br>
- [EvoLink Service](https://evolink.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/evolinkai/seedance-2-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task status updates and a temporary video URL when EvoLink generation succeeds.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
