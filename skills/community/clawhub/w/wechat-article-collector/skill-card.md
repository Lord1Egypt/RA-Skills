## Description: <br>
微信公众号文章批量采集工具。通过 Browser Harness 连接用户已登录的微信公众号后台，自动提取文章列表、去重、下载全文并保存到本地知识库。适用于个人公众号内容备份、知识库构建、文章管理等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adchina2025](https://clawhub.ai/user/adchina2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect article lists and full article text from WeChat Official Accounts and other selector-configured article sites into a local knowledge base. It is intended for article backup, content management, and knowledge-base building workflows where the user controls the logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate a logged-in Chrome session and access account-scoped pages. <br>
Mitigation: Run it only with a dedicated browser profile that is logged into the intended account and does not hold unrelated sessions. <br>
Risk: Selector files and target URLs can direct scraping behavior toward arbitrary sites. <br>
Mitigation: Use trusted URLs and reviewed selector configuration only; avoid accepting selector files from untrusted sources. <br>
Risk: Server security guidance reports an unsafe shell invocation reachable through user-provided input. <br>
Mitigation: Do not use untrusted --url values and patch the shell invocation before broad or unattended use. <br>
Risk: Scheduled collection can accumulate sensitive article data without active review. <br>
Mitigation: Enable cron only with retention rules, monitoring, and a reviewed save directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adchina2025/wechat-article-collector) <br>
- [Browser Harness](https://github.com/browser-use/browser-harness) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown article files, JSON article-list data, and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes collected articles under the configured save_dir and writes /tmp/all_articles.json during collection.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
