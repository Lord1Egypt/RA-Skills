## Description: <br>
Upscale images to 2K, 4K, or 8K resolution using WaveSpeed AI's Image Upscaler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to guide image upscaling workflows with WaveSpeed AI, including local image upload, image URL input, target resolution selection, output format selection, retry configuration, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images submitted for upscaling are sent to WaveSpeed AI and may be sensitive. <br>
Mitigation: Use only images approved for third-party processing, and avoid confidential images unless WaveSpeed's data handling terms are acceptable. <br>
Risk: WaveSpeed API usage can incur charges under the configured API key. <br>
Mitigation: Keep the API key in an environment variable or secret manager, restrict key access, and monitor account usage. <br>
Risk: Untrusted image URLs can introduce unsafe input or unexpected external access. <br>
Mitigation: Validate image URLs and only use trusted image sources before sending requests. <br>


## Reference(s): <br>
- [WaveSpeed API key access](https://wavespeed.ai/accesskey) <br>
- [ClawHub skill release](https://clawhub.ai/chengzeyi/wavespeed-image-upscaler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides API-key configuration and WaveSpeed API usage; the upscaled image URL is produced by the WaveSpeed API when the workflow is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; SKILL.md frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
