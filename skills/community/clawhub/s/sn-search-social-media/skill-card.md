## Description:

搜索社区、社媒、新闻热点、百科趋势、开发者生态和技术讨论时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to gather public signals from community, social media, news, encyclopedia trend, developer ecosystem, and technical discussion sources. It supports cross-source trend checks while excluding cryptocurrency, blockchain, Web3, NFT, DeFi, exchange, mining, and wallet topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to public web APIs and websites.

Mitigation: Use only public, non-sensitive queries; do not enter secrets, customer data, private incident names, or unreleased product details.

Risk: Dependency behavior may change across installs.

Mitigation: Install dependencies in a virtual environment and pin httpx when reproducible execution is required.

Risk: The skill intentionally refuses cryptocurrency, blockchain, Web3, NFT, DeFi, exchange, mining, and wallet topics.

Mitigation: Stop processing those requests and use a different approved workflow when that coverage is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-search-social-media)
- [Wikimedia Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/)
- [GitHub public search](https://github.com/search)
- [Stack Exchange search](https://stackexchange.com/search)
- [Hacker News](https://news.ycombinator.com/)
- [Baidu Index](https://index.baidu.com/)
- [Weibo hot search](https://s.weibo.com/top/summary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts return standard JSON objects with success, query, provider, items, and error fields.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
