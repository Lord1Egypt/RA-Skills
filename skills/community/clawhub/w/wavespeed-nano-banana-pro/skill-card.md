## Description: <br>
Generate and edit images using Google's Nano Banana Pro model via WaveSpeed AI, including text-to-image generation and natural-language image editing with flexible aspect ratios, native 4K resolution, multilingual text rendering, and camera-style controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and agent builders use this skill to generate images from text prompts or edit existing images through WaveSpeed AI's Nano Banana Pro endpoints. It is useful when an agent needs implementation guidance, API examples, and parameter choices for prompt-based image generation or editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and uploaded images are sent to WaveSpeed AI for processing. <br>
Mitigation: Avoid confidential, regulated, or sensitive images unless WaveSpeed AI's data handling terms have been reviewed and accepted. <br>
Risk: Untrusted image URLs can expose the agent workflow to unsafe or unintended external content. <br>
Mitigation: Use trusted or validated image URLs, and avoid arbitrary user-supplied links. <br>
Risk: The skill requires a WaveSpeed API key. <br>
Mitigation: Store WAVESPEED_API_KEY in environment variables or secret management and do not hardcode it in source files. <br>


## Reference(s): <br>
- [WaveSpeed AI API key access](https://wavespeed.ai/accesskey) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WaveSpeed model IDs, prompt and image parameters, aspect ratio options, resolution options, output format options, retry guidance, and error-handling examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
