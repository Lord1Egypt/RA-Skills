## Description: <br>
Generate AI videos with ByteDance Seedance from text prompts, images, first-and-last-frame inputs, or reference images, and query or manage generation tasks through the Volcengine Ark API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AsikoChen](https://clawhub.ai/user/AsikoChen) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to create, monitor, download, list, and delete Seedance video generation tasks. It supports text-to-video, image-to-video, draft generation, optional audio generation, and local image conversion for API submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to Volcengine under the user's ARK_API_KEY. <br>
Mitigation: Use only content approved for that external service and protect the API key as a credential. <br>
Risk: The bundled Feishu guide describes an additional external sharing path for generated videos. <br>
Mitigation: Confirm the exact file, recipient or chat, and sensitivity before sending, and protect Feishu app credentials. <br>
Risk: Downloaded videos may open automatically on macOS after completion. <br>
Mitigation: Review the download behavior and destination before running the CLI in environments where automatic opening is not desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AsikoChen/seedance-video-creation) <br>
- [Volcengine Ark API base URL](https://ark.cn-beijing.volces.com/api/v3) <br>
- [Feishu video sending guide](how_to_send_video_via_feishu_app.md) <br>
- [Feishu media upload endpoint](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all) <br>
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages/send) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and curl command examples, JSON task responses, and downloaded video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY; prompts and selected images are sent to Volcengine, and optional Feishu sharing can upload generated videos to Feishu.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
