## Description: <br>
同步多个微信公众号的文章列表，抓取单篇或单账号文章详情和图片，并导出最近文章汇总或 Markdown 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryczq](https://clawhub.ai/user/henryczq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage WeChat official-account login, sync account article lists, fetch article bodies and images, configure proxies, and export recent article reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable WeChat login credentials, imported cookie/token files, or JSON command output may expose sensitive session data. <br>
Mitigation: Treat session files and command output as credentials, restrict where they are stored or shared, and clear login state when finished. <br>
Risk: Configured gateways, proxy URLs, or messaging targets may receive sensitive article-fetch or synchronization traffic. <br>
Mitigation: Use only trusted private messaging targets and trusted gateways, and avoid public or unknown proxy URLs. <br>
Risk: Article detail fetches can be incomplete when image downloads fail or WeChat returns an environment-check page. <br>
Mitigation: Verify image downloads before treating a fetch as complete, inspect proxy settings, and retry through a trusted gateway when the skill reports environment-check failures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/henryczq/wechat-article-assistant) <br>
- [Operations Reference](references/operations.md) <br>
- [Interface Reference](references/interface-reference.md) <br>
- [Design Reference](references/design.md) <br>
- [SQLite Schema Notes](references/sqlite-schema.md) <br>
- [Account Classification and Summary Design](references/account-classification-summary-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command output, and exported article or report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite records, downloaded images, and Markdown/HTML/JSON article exports when save options are used.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
