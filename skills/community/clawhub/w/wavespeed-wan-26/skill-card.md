## Description: <br>
Generate videos using Alibaba's Wan 2.6 model via WaveSpeed AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate short videos from text prompts or animate images through WaveSpeed AI's Wan 2.6 text-to-video and image-to-video endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WaveSpeed API keys can be exposed if hardcoded or committed to source control. <br>
Mitigation: Store WAVESPEED_API_KEY outside source control using environment variables or a secret manager, and use revocable keys. <br>
Risk: Prompts, images, and audio selected for generation are sent to WaveSpeed. <br>
Mitigation: Avoid sending sensitive prompts or media unless the user intentionally wants those assets processed by WaveSpeed. <br>
Risk: Untrusted media URLs can expand exposure beyond the intended source asset. <br>
Mitigation: Use trusted image and audio URLs and validate media inputs before passing them to the API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengzeyi/wavespeed-wan-26) <br>
- [WaveSpeed API keys](https://wavespeed.ai/accesskey) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward WaveSpeed API requests that return generated video URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
