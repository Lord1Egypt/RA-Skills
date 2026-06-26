## Description: <br>
Generate and edit images using Google's Nano Banana 2 model via WaveSpeed AI, including text-to-image, multi-image editing, flexible aspect ratios, up to 4K output, multilingual text rendering, and camera-style prompt controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for WaveSpeed AI setup, JavaScript examples, and usage guidance for generating images from prompts or editing uploaded or URL-based images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WaveSpeed API keys can be exposed if hardcoded or committed. <br>
Mitigation: Store WAVESPEED_API_KEY in environment variables or secret management, and avoid placing credentials in source files. <br>
Risk: WaveSpeed image generation and editing requests may incur provider usage charges. <br>
Mitigation: Use the service deliberately with an account intended for billing, and review resolution-specific costs before high-volume use. <br>
Risk: Prompts and uploaded images are shared with the WaveSpeed AI service. <br>
Mitigation: Only upload images and prompts that are appropriate to share with that provider, and validate image URLs before sending requests. <br>


## Reference(s): <br>
- [WaveSpeed API key access](https://wavespeed.ai/accesskey) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes model IDs, parameter tables, aspect ratio options, pricing notes, prompt tips, and security constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
