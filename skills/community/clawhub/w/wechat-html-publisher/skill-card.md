## Description:

Publishes HTML rich text directly to the WeChat Official Account draft box while preserving inline formatting and uploading referenced images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuo-wentao](https://clawhub.ai/user/zuo-wentao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare WeChat Official Account drafts from already-formatted HTML articles, including local or remote images and article metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML image references may cause broad local file reads or arbitrary URL fetches before upload.

Mitigation: Run only on trusted HTML, restrict image paths to a dedicated asset folder, and block private or internal network URLs before publication.

Risk: Article content, metadata, cover images, and embedded images are sent to WeChat.

Mitigation: Preview the exact content and confirm that all included data is approved for upload to WeChat before running the publisher.

Risk: Image type or size problems can cause failed uploads or unexpected draft content.

Mitigation: Validate image formats and sizes before upload and review the generated WeChat draft before publication.

## Reference(s):

- [Wechat HTML Publisher on ClawHub](https://clawhub.ai/zuo-wentao/skills/wechat-html-publisher)
- [ClawHub publisher profile: zuo-wentao](https://clawhub.ai/user/zuo-wentao)
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/offiaccount/)
- [WeChat draft add API](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html)
- [WeChat temporary material API](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python command-line usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script sends HTML content, article metadata, covers, and embedded images to WeChat APIs and returns a draft media_id on success.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
