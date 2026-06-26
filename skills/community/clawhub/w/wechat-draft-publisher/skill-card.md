## Description: <br>
Generates WeChat Official Account articles from a short topic, optionally creates images and cover art, formats the article, and saves it to the WeChat draft box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuzhudewenjian](https://clawhub.ai/user/zhuzhudewenjian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to draft WeChat Official Account posts from a topic, prepare optional generated images and cover art, and create a draft for review in the WeChat backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured WeChat credentials and image API keys can authorize account actions or expose paid services if mishandled. <br>
Mitigation: Keep config.json and environment variables private, and install only when the skill should use the configured WeChat official account. <br>
Risk: Article text, prompts, and generated images may be sent to a third-party image API provider. <br>
Mitigation: Use a trusted image API provider and avoid confidential article text or prompts. <br>
Risk: The optional publish path can submit content beyond draft creation. <br>
Mitigation: Review drafts in the WeChat backend and use --publish only when publication is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuzhudewenjian/wechat-draft-publisher) <br>
- [README](artifact/README.md) <br>
- [WeChat Official Account Platform](https://mp.weixin.qq.com/) <br>
- [WeChat API base endpoint](https://api.weixin.qq.com/cgi-bin) <br>
- [SiliconFlow image API provider](https://siliconflow.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown article content with shell commands and generated WeChat draft artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create WeChat drafts, upload images, and optionally submit publication when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
