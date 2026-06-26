## Description: <br>
Qwen Image Edit helps agents generate and edit images through Alibaba Cloud's Qwen Image API, including text-to-image, single-image edits, style transfer, and multi-image fusion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macwx](https://clawhub.ai/user/macwx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce posters, covers, banners, promotional graphics, and edited images from Chinese or English prompts. It can also guide an agent to run the bundled helper script with local or URL image inputs when image editing or multi-image fusion is requested. <br>

### Deployment Geography for Use: <br>
Global, subject to Alibaba Cloud DashScope regional endpoint availability and the user's privacy, compliance, and data residency requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, local images, and image URLs are sent to Alibaba Cloud DashScope for generation or editing. <br>
Mitigation: Use only data approved for that third-party service, and avoid private, confidential, regulated, or otherwise sensitive images unless the user's compliance requirements allow it. <br>
Risk: The skill requires sensitive DashScope credentials. <br>
Mitigation: Provide credentials through a secure environment variable or runtime argument, avoid committing keys to files, and rotate keys if they are exposed. <br>
Risk: The helper script includes an option to disable SSL verification. <br>
Mitigation: Keep SSL verification enabled except for approved corporate proxy scenarios, and document any exception before use. <br>


## Reference(s): <br>
- [Alibaba Cloud Qwen Image documentation](https://help.aliyun.com/zh/model-studio/text-to-image) <br>
- [DashScope API key console](https://dashscope.console.aliyun.com/) <br>
- [ClawHub release page](https://clawhub.ai/macwx/qwen-image-edit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell command examples, MEDIA_URL links or image embeds, and optional PNG files when saving is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key; local image inputs are encoded and sent to the API; generated image URLs expire after 24 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
