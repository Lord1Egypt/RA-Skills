## Description: <br>
全网持续收录每日公众号原创热门文章内容，向用户推送公众号原创热门文章；当用户需要获取全领域的公众号原创热门文章、或订阅每日原创热门文章推送时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, editors, planners, and operations teams use this skill to retrieve original viral WeChat Official Account article rankings by category or date, generate shareable HTML/PDF reports, and request daily category subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and the scanner reports HTTPS certificate checks are disabled. <br>
Mitigation: Use a revocable, low-privilege API key, avoid untrusted networks, and fix TLS verification before broad deployment. <br>
Risk: Generated HTML can contain third-party article data and external scripts. <br>
Mitigation: Review generated reports before sharing or archiving, and treat linked article and author content as third-party material. <br>
Risk: Daily subscription behavior is offered, but evidence does not explain how subscription state is stored or canceled. <br>
Mitigation: Confirm storage, retention, cancellation, and notification behavior with the publisher before enabling push notifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/wechat-original-article-king) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [Category mapping reference](references/category_mapping.md) <br>
- [RedFox article data API](https://redfox.hk/story/api/cozeSkill/getWxDataByCategoryAndTime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML files, configuration guidance] <br>
**Output Format:** [Markdown article tables and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may include third-party article links, read counts, author links, data freshness notes, and subscription prompts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
