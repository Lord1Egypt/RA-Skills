## Description: <br>
Uploads HTML rich text directly to a WeChat Official Account draft box while preserving complete HTML formatting without Markdown conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuo-wentao](https://clawhub.ai/user/zuo-wentao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to upload preformatted HTML articles, cover images, and referenced images into a WeChat Official Account draft for later review and publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat Official Account credentials and uploads selected HTML, cover images, and referenced images to WeChat. <br>
Mitigation: Use only intended credentials, keep the app secret out of repositories and logs, and run the publisher only for content that is approved for upload. <br>
Risk: HTML may include absolute local image paths or remote image URLs that will be processed during upload. <br>
Mitigation: Review the HTML and referenced images before execution, and remove any unintended local paths or remote image sources. <br>
Risk: The workflow creates a draft that still requires human content review before publication. <br>
Mitigation: Check the generated draft in the WeChat Official Account backend before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuo-wentao/wechat-html-publisher) <br>
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/offiaccount/) <br>
- [WeChat Add Draft API](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html) <br>
- [WeChat Material Management API](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WeChat API calls that create a draft media_id when executed with valid credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
