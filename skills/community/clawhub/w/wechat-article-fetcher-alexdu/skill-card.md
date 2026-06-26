## Description: <br>
微信公众号文章抓取工具。当用户发送 mp.weixin.qq.com 链接时自动触发，将文章内容提取为 Markdown/文本，无需 API 密钥。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexduming](https://clawhub.ai/user/alexduming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to fetch public WeChat article content from mp.weixin.qq.com links and return it as Markdown or text without configuring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat article links are sent to the public third-party service down.mptext.top. <br>
Mitigation: Use only with public, non-confidential, non-access-restricted links and avoid tracking-sensitive URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexduming/wechat-article-fetcher-alexdu) <br>
- [Publisher profile](https://clawhub.ai/user/alexduming) <br>
- [mptext public service](https://down.mptext.top) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown, text, JSON, or HTML returned from a public HTTP endpoint, with shell and Python usage examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a URL-encoded mp.weixin.qq.com article link; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
