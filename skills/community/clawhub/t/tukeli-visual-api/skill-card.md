## Description: <br>
调用图可丽（Tukeli）视觉处理 API，实现通用抠图、人脸变清晰、AI背景更换三项能力。支持文件上传、图片URL两种输入方式，返回二进制流或Base64编码结果。AI背景更换为异步接口，需先提交任务再查询结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cutout-pro](https://clawhub.ai/user/cutout-pro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-production teams use this skill to remove image backgrounds, enhance face images, and submit or query AI background replacement jobs through the Tukeli visual API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, image URLs, Base64 image data, face-analysis requests, and AI background prompts are sent to Tukeli's external API. <br>
Mitigation: Use the skill only with images the user is authorized to process, and avoid regulated or private face images unless consent and a suitable data-handling basis are in place. <br>
Risk: TUKELI_API_KEY authorizes billable API calls that can spend account credits. <br>
Mitigation: Store the key in an environment variable or local .env file, keep it out of logs and shared repositories, and configure daily limits where appropriate. <br>
Risk: Generated .meta.json files can include local file paths, source image URLs, request parameters, and timing details. <br>
Mitigation: Review or delete metadata sidecar files before sharing outputs when paths, URLs, or processing context are sensitive. <br>


## Reference(s): <br>
- [API 参考文档](references/api-reference.md) <br>
- [配置指南](references/setup-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/cutout-pro/tukeli-visual-api) <br>
- [Tukeli website](https://www.tukeli.net) <br>
- [Tukeli image matting API documentation](https://www.tukeli.net/apidoc-image-matting.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; API calls can produce image files, JSON status, or Base64 image data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TUKELI_API_KEY and may write generated images plus .meta.json sidecar files under data/outputs/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
