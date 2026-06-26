## Description: <br>
Generates 5-second videos from text prompts using the Tomoviee Text-to-Video API through the Wondershare OpenAPI gateway, with controls for resolution, aspect ratio, and camera movement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate short text-to-video clips through Tomoviee/Wondershare OpenAPI, including establishing shots, B-roll, and rapid video concept prototypes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses third-party Tomoviee/Wondershare API services and may consume provider quota or incur billing when generating videos. <br>
Mitigation: Use a dedicated API key, monitor provider quota or billing, and run only when Tomoviee/Wondershare OpenAPI use is intended. <br>
Risk: Prompts and optional callback URLs may be sent to the third-party API provider. <br>
Mitigation: Avoid sensitive prompts, confidential media concepts, and internal callback URLs unless they are approved for third-party processing. <br>
Risk: The auth helper prints a Basic token to terminal output. <br>
Mitigation: Do not share logs or terminal output containing generated tokens, and rotate credentials if a token is exposed. <br>


## Reference(s): <br>
- [Tomoviee Video Generation APIs](artifact/references/video_apis.md) <br>
- [Camera Movement Types Reference](artifact/references/camera_movements.md) <br>
- [Tomoviee Prompt Engineering Guide](artifact/references/prompt_guide.md) <br>
- [Tomoviee Developer Portal (Global)](https://www.tomoviee.ai/developers.html) <br>
- [Tomoviee API Docs (Global)](https://www.tomoviee.ai/doc/) <br>
- [Tomoviee Developer Portal (Mainland)](https://www.tomoviee.cn/developers.html) <br>
- [Tomoviee API Docs (Mainland)](https://www.tomoviee.cn/doc/) <br>
- [Wondershare OpenAPI Gateway](https://openapi.wondershare.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python code examples, shell commands, and API usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API task identifiers and JSON result handling guidance for 5-second generated video URLs.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
