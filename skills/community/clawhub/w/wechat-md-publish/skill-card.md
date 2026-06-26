## Description: <br>
Publishes Markdown articles to WeChat Official Account, with support for AI-generated cover images, HTML card rendering, draft creation, and optional publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[864446285](https://clawhub.ai/user/864446285) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and publishing agents use this skill to turn Markdown articles and local assets into WeChat Official Account drafts, with optional automatic publishing after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WeChat Official Account API credentials and caches access tokens on the local machine. <br>
Mitigation: Use a dedicated environment where possible and protect ~/.wechat_publish/config.json and token_cache.json with restrictive file permissions. <br>
Risk: Selected Markdown content and referenced local images are uploaded to WeChat, and --publish can submit content for publication. <br>
Mitigation: Create drafts first, review the rendered article in WeChat, and use --publish only after explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/864446285/wechat-md-publish) <br>
- [Publisher profile](https://clawhub.ai/user/864446285) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>
- [WeChat API base](https://api.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and Python CLI/API execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates WeChat drafts by default; optional --publish submits the draft for publication.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
