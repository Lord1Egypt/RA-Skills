## Description: <br>
Use this skill for computer vision tasks including image recognition (OCR, object detection) and image generation (text-to-image, image-to-image). Supports asynchronous task execution with Tencent COS storage and Doubao AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgwanai](https://clawhub.ai/user/lgwanai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add visual recognition, OCR-style extraction, visual question answering, and image generation workflows to text-first agents. It is suited for document digitization, UI or content creation, image analysis, and batch visual processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chosen images, reference images, prompts, and generated outputs are sent through Tencent COS and Doubao/Volcengine services. <br>
Mitigation: Use the skill only for content your policies allow to be processed by those services, and avoid regulated or confidential documents unless approved. <br>
Risk: Cloud credentials are required for Tencent COS and Doubao access. <br>
Mitigation: Use least-privilege credentials, keep the COS bucket private or tightly scoped, and rotate credentials according to organizational policy. <br>
Risk: Local task history under .tasks/ may contain prompts, image URLs, outputs, or error details. <br>
Mitigation: Periodically clear .tasks/ or disable retention where task history may expose sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgwanai/vision-skill) <br>
- [Volcengine Ark API endpoint used by the skill](https://ark.cn-beijing.volces.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [JSON task status, text or Markdown recognition results, code blocks for code OCR, and downloaded image files when an output path is provided] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tasks run asynchronously by default and can be polled by task ID; local task metadata is stored under .tasks/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
