## Description: <br>
Generate and edit images using ByteDance's Seedream V4.5 model via WaveSpeed AI, including text-to-image generation and multi-image editing with custom resolutions up to 4096x4096. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative teams use this skill to guide agents in generating new images or editing existing images through WaveSpeed AI, especially when high-quality text rendering is needed for posters, logos, and branded visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WaveSpeed API key and may incur provider charges when agents generate or edit images. <br>
Mitigation: Configure the API key through environment variables or secret management, review expected usage before running requests, and monitor provider billing. <br>
Risk: Prompts and selected images are sent to WaveSpeed AI for processing, which may expose confidential, regulated, or personal content. <br>
Mitigation: Use only authorized prompts and images, avoid sensitive content unless approved, and review WaveSpeed AI data handling policies before use. <br>
Risk: Image editing uses external or uploaded image URLs, so untrusted image sources can create privacy or content-safety exposure. <br>
Mitigation: Validate image URLs and use trusted sources only; do not pass untrusted or user-provided image URLs without review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chengzeyi/wavespeed-seedream-45) <br>
- [WaveSpeed AI access keys](https://wavespeed.ai/accesskey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include WaveSpeed model IDs, prompt and image parameters, image output URLs, retry settings, and error handling patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
