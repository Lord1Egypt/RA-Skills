## Description:

同花顺问财全功能合并技能，集成行情、指数、财务、公司基本资料、事件、经营数据、机构研究与评级、研报、公告、新闻、A股选股和板块筛选查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhofchina](https://clawhub.ai/user/hhofchina)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer Chinese financial-market questions by routing natural-language iWenCai queries across market data, index data, financial metrics, company information, events, research reports, announcements, news, A-share screening, and sector screening. It is intended for users who need concise tabular or listed outputs with source attribution to 同花顺问财.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an iWenCai API key and can accept the key on the command line.

Mitigation: Provide IWENCAI_API_KEY through a protected environment or secret store and avoid passing secrets through --api-key.

Risk: Financial queries may include sensitive portfolio, account, or trading-interest details.

Mitigation: Avoid sending private account identifiers or sensitive portfolio details in queries.

Risk: Changing IWENCAI_BASE_URL could send requests and API credentials to an untrusted endpoint.

Mitigation: Keep IWENCAI_BASE_URL fixed to the official HTTPS iWenCai endpoint before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hhofchina/skills/wen-cai)
- [Publisher profile](https://clawhub.ai/user/hhofchina)
- [同花顺问财 query page](https://www.iwencai.com/unifiedwap/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables or lists, optional raw JSON from the CLI, and configuration guidance for required environment variables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IWENCAI_API_KEY and uses IWENCAI_BASE_URL, defaulting to the HTTPS iWenCai endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
