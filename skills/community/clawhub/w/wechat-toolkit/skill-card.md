## Description: <br>
微信公众号一站式工具包，集成文章搜索、文章下载、AI 改写和公众号发布功能，适用于搜索、下载、改写和发布微信公众号文章的工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-q526](https://clawhub.ai/user/mr-q526) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to search and download WeChat public account articles, prepare rewritten Markdown drafts, manage media, and publish content to a WeChat official account draft box. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage WeChat account drafts, published articles, and delete or formal publish actions. <br>
Mitigation: Use it only with a WeChat account you control, manually review content before publication, and keep a backup before delete or formal publish commands. <br>
Risk: WeChat API credentials may be exposed or mishandled. <br>
Mitigation: Prefer explicit WECHAT_APP_ID and WECHAT_APP_SECRET environment variables, avoid storing secrets in shared files, and rotate credentials if exposure is suspected. <br>
Risk: Rewrite workflows can be used to disguise copied or AI-generated content as original. <br>
Mitigation: Use rewriting only on content you have rights to modify, preserve factual attribution, and review outputs for copyright and disclosure obligations. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Theme reference](references/themes.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [wenyan-cli](https://github.com/caol64/wenyan-cli) <br>
- [WeChat Official Account platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON search results, and generated article files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on Node.js, Google Chrome for downloads, and WeChat account API credentials for publishing.] <br>

## Skill Version(s): <br>
1.0.3 (source: target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
