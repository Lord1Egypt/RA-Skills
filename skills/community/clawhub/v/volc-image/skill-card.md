## Description: <br>
火山引擎图像生成 - 使用火山引擎方舟API生成图片并下载. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magieSky](https://clawhub.ai/user/magieSky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to generate images from text prompts with the Volcengine Ark API and download the generated image file for local review or reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an ARK_API_KEY credential for Volcengine Ark. <br>
Mitigation: Provide the key through the environment or platform secret settings, and avoid passing secrets as command-line arguments. <br>
Risk: Prompts are sent to an external Volcengine API for image generation. <br>
Mitigation: Avoid sending sensitive or confidential prompt content unless that external service is approved for the use case. <br>
Risk: Generated images are downloaded and saved locally. <br>
Mitigation: Review saved output files before sharing, publishing, or reusing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magieSky/volc-image) <br>
- [Publisher profile](https://clawhub.ai/user/magieSky) <br>
- [Volcengine Ark console](https://console.volcengine.com/ark/endpoint) <br>
- [Volcengine Ark image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Files, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance, shell commands, Python code, and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and saves generated images locally as JPG files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
