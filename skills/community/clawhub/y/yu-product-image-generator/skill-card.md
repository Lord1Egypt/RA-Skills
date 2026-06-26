## Description: <br>
AI product image generation workflow with multi-style selection, multilingual copy options, storyboard planning, and batch image packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidunderwood7970](https://clawhub.ai/user/davidunderwood7970) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, commerce operators, and agent users can use this skill to turn product images into marketing image concepts, generated visuals, preview pages, and downloadable bundles. It supports style selection, language selection, storyboard review, and optional delivery through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, generated images, or product details may be sent to external image-generation services. <br>
Mitigation: Use only non-sensitive product images unless the external services and data handling terms have been reviewed and approved. <br>
Risk: The artifact includes embedded API credentials and Feishu credentials. <br>
Mitigation: Remove or rotate bundled credentials before use, and supply secrets through a managed runtime secret store or environment variables. <br>
Risk: The Feishu integration can upload generated images and send them to a recipient. <br>
Mitigation: Disable Feishu delivery unless needed, verify recipient IDs explicitly, and review all generated outputs before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidunderwood7970/yu-product-image-generator) <br>
- [Publisher profile](https://clawhub.ai/user/davidunderwood7970) <br>
- [Nano Banana API endpoint](https://grsai.dakka.com.cn) <br>
- [Volcengine API endpoint](https://ark.cn-beijing.volces.com/api/v3) <br>
- [DashScope API endpoint](https://dashscope.aliyuncs.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API calls, files, configuration, guidance] <br>
**Output Format:** [Conversational guidance, generated image files, preview HTML, ZIP archives, and optional Feishu messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send prompts, reference images, generated images, and delivery metadata to external image-generation or Feishu services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
