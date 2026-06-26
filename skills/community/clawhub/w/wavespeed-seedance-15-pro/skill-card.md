## Description: <br>
Generate text-to-video and image-to-video clips with ByteDance's Seedance V1.5 Pro model through WaveSpeed AI, including options for duration, resolution, audio, camera control, and seed configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate short videos from text prompts or animate trusted source images through WaveSpeed AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WaveSpeed API key exposure. <br>
Mitigation: Store WAVESPEED_API_KEY in environment variables or a secret manager, and do not hardcode or commit it. <br>
Risk: Prompts and selected images are sent to WaveSpeed for processing. <br>
Mitigation: Avoid uploading confidential media unless the provider's terms are acceptable, and validate media URLs before use. <br>
Risk: Video generation can create billing impact. <br>
Mitigation: Monitor usage and choose duration, resolution, and audio settings deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengzeyi/wavespeed-seedance-15-pro) <br>
- [WaveSpeed AI access keys](https://wavespeed.ai/accesskey) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WaveSpeed model endpoint names, generation parameters, output URL handling, and secret-management guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
