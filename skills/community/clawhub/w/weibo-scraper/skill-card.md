## Description: <br>
抓取指定微博用户的公开微博内容，支持按日期筛选、获取长文全文和滚动加载。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x1a0f31](https://clawhub.ai/user/x1a0f31) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect publicly visible posts from a specified Weibo account for a requested date or date range. It is intended for targeted lookup rather than repeated or bulk scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases could activate the skill unintentionally. <br>
Mitigation: Use explicit target account names, UIDs, and date ranges before browsing or collecting posts. <br>
Risk: Repeated or broad scraping may raise privacy, site terms, or rate-limit concerns. <br>
Mitigation: Limit use to public posts, avoid bulk collection, and review applicable site terms and rate limits before repeated runs. <br>
Risk: Browser extraction may miss posts or return incomplete content if the mobile page changes or scrolling does not load all entries. <br>
Mitigation: Verify the target date, scroll and resnapshot until relevant posts are loaded, and review sampled output before relying on it. <br>


## Reference(s): <br>
- [m.weibo.cn user page pattern](https://m.weibo.cn/u/{UID}) <br>
- [m.weibo.cn status page pattern](https://m.weibo.cn/status/{微博ID}) <br>
- [ClawHub skill release page](https://clawhub.ai/x1a0f31/weibo-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style text listing matched posts chronologically with post times and content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser navigation and evaluation guidance for public m.weibo.cn pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
