## Description: <br>
Generates images from text prompts through Tencent Cloud HunYuan Text-to-Image, with optional reference images, resolution control, prompt rewriting, seed-based reproducibility, and job polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neck-cn](https://clawhub.ai/user/Neck-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to submit Tencent Cloud HunYuan text-to-image jobs, poll for completion, and return generated image URLs. It supports prompt-based image creation workflows that may use reference image URLs, custom resolution, prompt rewriting, and fixed seeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference image URLs are sent to Tencent Cloud for image generation. <br>
Mitigation: Avoid submitting secrets, private internal URLs, or sensitive content unless Tencent Cloud use is approved for that data. <br>
Risk: The skill uses Tencent Cloud quota or billing when generation jobs are submitted. <br>
Mitigation: Use a least-privilege Tencent Cloud key and monitor service usage and billing. <br>
Risk: The scripts can install the Tencent Cloud SDK at runtime if it is missing. <br>
Mitigation: Preinstall and pin an approved Tencent Cloud SDK version in managed environments. <br>


## Reference(s): <br>
- [Submit Text-to-Image API](references/submit_text_to_image_api.md) <br>
- [Query Text-to-Image API](references/query_text_to_image_api.md) <br>
- [Tencent Cloud AIART Console](https://console.cloud.tencent.com/aiart) <br>
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi) <br>
- [Tencent Cloud SubmitTextToImageProJob Documentation](https://cloud.tencent.com/document/product/1668/124632) <br>
- [Tencent Cloud QueryTextToImageProJob Documentation](https://cloud.tencent.com/document/product/1668/124633) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output from the Tencent Cloud API scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include a Tencent Cloud job ID, request ID, generation status, revised prompt, and temporary generated image URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
