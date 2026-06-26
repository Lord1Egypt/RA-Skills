## Description: <br>
Tianshu Image uses Alibaba Cloud DashScope Tongyi Wanxiang to generate images from text prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn written image descriptions into generated images through Alibaba Cloud DashScope. It is intended for text-to-image requests and not for image editing or style transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to Alibaba Cloud DashScope and may contain sensitive personal or proprietary information. <br>
Mitigation: Avoid including secrets or sensitive personal data in prompts, and only use the skill when prompt sharing with DashScope is acceptable. <br>
Risk: The DashScope API key may consume quota or incur charges. <br>
Mitigation: Store the key in environment or configuration storage, avoid passing it on the command line, and use an account with appropriate quota controls. <br>
Risk: Generated images may be saved to unintended local paths when a filename is supplied. <br>
Mitigation: Review the target output path before running the skill and save generated images only to intended locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/tianshu-image) <br>
- [Publisher profile](https://clawhub.ai/user/wangshengli0421) <br>
- [DashScope console](https://dashscope.console.aliyun.com/) <br>
- [DashScope multimodal generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with generated image URL or local image path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print MEDIA_URL for remote display or MEDIA for a saved local image file.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
