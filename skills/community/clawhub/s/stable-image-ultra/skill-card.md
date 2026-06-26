## Description: <br>
Generate photorealistic images with Stability AI's Stable Image Ultra and Stable Diffusion 3.5 Large models through AWS Bedrock. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate high-quality PNG images from detailed text prompts for visual assets, illustrations, portraits, products, and scene imagery. It is intended for workflows that can supply AWS Bedrock credentials and accept paid image-generation calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make paid AWS Bedrock image-generation calls using available credentials. <br>
Mitigation: Use a dedicated least-privilege Bedrock profile or token and monitor AWS costs for image generation activity. <br>
Risk: Ambient or long-lived AWS credentials may be used by default. <br>
Mitigation: Prefer short-lived credentials or a scoped bearer token, and avoid exposing direct access keys to general agent sessions. <br>
Risk: Generic image requests may be sent to AWS without strong confirmation boundaries. <br>
Mitigation: Require explicit user confirmation before sending prompts or credential-backed requests to AWS Bedrock. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wujiaming88/stable-image-ultra) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG image files through AWS Bedrock calls; output paths, file sizes, and seed details may be reported by the script.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
