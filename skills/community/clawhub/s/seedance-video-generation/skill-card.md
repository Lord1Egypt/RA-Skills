## Description: <br>
Generate AI videos using ByteDance Seedance from text prompts or images, and query or manage video generation tasks across supported Seedance models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackyCSer](https://clawhub.ai/user/JackyCSer) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, creators, and agent workflows use this skill to generate, monitor, download, and manage Seedance video generation tasks through the Volcengine Ark API. It supports text-to-video, first-frame and first-plus-last-frame image-to-video, reference-image workflows, draft generation, and task status operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected image files are sent to Volcengine/ByteDance for generation. <br>
Mitigation: Use only content approved for that external service and avoid sensitive prompts or images unless policy and user consent allow it. <br>
Risk: Downloaded videos may auto-open on macOS after generation. <br>
Mitigation: Download to a trusted location, inspect the exact output path, and avoid unusual download destinations before opening the file. <br>
Risk: The optional Feishu workflow uploads generated videos and sends them to a configured chat using app credentials. <br>
Mitigation: Use the Feishu workflow only after confirming the exact file, recipient or chat, and message content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JackyCSer/seedance-video-generation) <br>
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3) <br>
- [Feishu media upload API endpoint](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all) <br>
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages/send) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with bash/Python examples, JSON task responses, and downloaded MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and may send prompts, image inputs, generated video files, and optional Feishu delivery data to external services.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
