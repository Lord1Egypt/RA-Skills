## Description: <br>
使用阿里云万相 2.6 模型生成微信公众号封面图、技术架构设计图和文章配图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[love254443233](https://clawhub.ai/user/love254443233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to generate WeChat public account cover images, technical architecture diagrams, and article illustrations from text prompts with Alibaba DashScope Wan 2.6. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and article text are sent to Alibaba DashScope. <br>
Mitigation: Avoid sensitive or regulated content in prompts and article text. <br>
Risk: API key misuse or unexpected usage costs may occur if credentials are exposed or unlimited. <br>
Mitigation: Use a dedicated, quota-limited API key and keep .env files private. <br>
Risk: Local dependency installation may affect the user's Python environment. <br>
Mitigation: Prefer an isolated Python environment for tighter dependency control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/love254443233/wan26-text-to-image) <br>
- [Alibaba Cloud Wan image generation API reference](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference) <br>
- [Alibaba Cloud Model Studio API key documentation](https://help.aliyun.com/zh/model-studio/get-api-key) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [PNG image files with optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image URLs are downloaded to a local output directory when available; json-only mode writes machine-readable JSON to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
