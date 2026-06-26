## Description: <br>
Publishes Markdown articles with optional local images to a WeChat Official Account draft box through the WeChat API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuejiangli](https://clawhub.ai/user/yuejiangli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare WeChat Official Account drafts from local Markdown articles and image files. It helps an agent handle credential setup guidance, image uploads, Markdown-to-HTML conversion, and draft creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WeChat account credentials. <br>
Mitigation: Use environment variables or a protected local config for secrets, keep config.json and .token_cache.json out of version control, and restrict file permissions where possible. <br>
Risk: The skill uploads selected article files and images to WeChat. <br>
Mitigation: Confirm the article content and image files before upload, and install only when WeChat draft creation from local files is intended. <br>


## Reference(s): <br>
- [WeChat Official Account API Reference](references/wechat_api.md) <br>
- [WeChat MP Backend](https://mp.weixin.qq.com) <br>
- [WeChat Stable Token API](https://api.weixin.qq.com/cgi-bin/stable_token) <br>
- [WeChat Draft Add API](https://api.weixin.qq.com/cgi-bin/draft/add) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, generated HTML, and WeChat media identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local intermediate files such as article HTML and image maps, and may return WeChat draft media_id values after upload.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
