## Description: <br>
全国招标中标采购信息搜索 - 保标招标 - 支持多条件筛选的招投标数据搜索，返回项目金额、甲方、乙方、代理机构、采集源网址等核心字段。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brade888](https://clawhub.ai/user/brade888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business researchers use this skill to search Chinese tender, bid award, contract, procurement-intent, and auction-rental project records with filters for keywords, category, region, dates, and pagination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tender-search terms, company names, locations, bid IDs, URLs, and similar business research inputs are sent to the stated Biaozhaozhao/Zhiliaobiaoxun API. <br>
Mitigation: Avoid entering secrets, regulated personal data, or confidential deal strategy as search terms. <br>
Risk: The skill requires an API key for the external bid-data service. <br>
Mitigation: Keep BID_API_KEY scoped, stored outside code, monitored, and rotated according to the provider's guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brade888/sbkj-bidsearch) <br>
- [Official website](https://www.bog-bid.com) <br>
- [API endpoint](https://gate.gov-bid.com/outer-gateway/bid/SearchProjectForAI) <br>
- [Interface documentation](http://faq.zhvac.com/web/#/p/50f55291c248b58163e9ae4aa178eb12) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BID_API_KEY and optionally BID_SERVER_URL; sends search parameters to the stated bid-data API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
