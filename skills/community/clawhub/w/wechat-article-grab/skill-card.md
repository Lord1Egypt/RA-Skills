## Description: <br>
抓取微信文章正文、搜索公众号、查文章列表、爆款查询. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[one2agi](https://clawhub.ai/user/one2agi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve WeChat public-account article text, search accounts, list recent articles, compare accounts or URLs, and inspect trending article metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle WeChat public-platform session cookies and tokens. <br>
Mitigation: Use a dedicated low-privilege account, avoid full personal browser cookies, rotate or revoke cookies after use, and treat scripts/skill.env as sensitive. <br>
Risk: Article URLs, queries, and account data may be sent to third-party services. <br>
Mitigation: Install only if that data sharing is acceptable for the intended use case and avoid submitting sensitive article or account data. <br>
Risk: The security evidence flags an intentionally insecure no-SNI TLS bypass client. <br>
Mitigation: Remove or replace the bypass with normally verified HTTPS before trusting results or credentials around this skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/one2agi/skills/wechat-article-grab) <br>
- [Environment Configuration Guide](env-guide.md) <br>
- [Priority and Fallback Reference](references/priority.md) <br>
- [mptext API Dashboard](https://down.mptext.top/dashboard/api) <br>
- [WeChat Public Platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and Markdown-style summaries, with optional saved article content or configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include article titles, extracted body text, account search results, article lists, comparison summaries, trend metrics, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
