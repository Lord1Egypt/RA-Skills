## Description:

地方标讯极速检索-比地招标，当用户指定省份、城市或特定地域进行下沉标讯搜索时调用，必须严格应用地域过滤器参数，快速返回按时间倒序排列的地方采购公告及预算金额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams and analysts use this agent to find local Chinese procurement notices by requested region, and to review related company and market information when needed.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Automatic signup collects platform, CPU architecture, and a MAC address hash; the security review says the signup notice understates device identification, and provider retention and deletion practices are unspecified.

Mitigation: Prefer a manually obtained API key. If automatic signup is needed, explain the device features and obtain the user's consent before collecting them.

Risk: The security review flags the update-notice workflow as lacking clear safeguards, and the package does not establish live acknowledgment validation.

Mitigation: Check update links independently before acting, and relay update notices without claiming the installed package is out of date.

Risk: Searches send keywords and filters to Zhiliaobiaoxun, and successful data requests can consume credits.

Mitigation: Keep the requested geography and query scope unchanged unless the user approves broadening it; protect saved API keys and automatic-login links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/skills/tender-express-search-bidizhaobiao)
- [Bid and project search reference](references/api-search.md)
- [Company analysis reference](references/api-company.md)
- [Market analysis reference](references/api-market.md)
- [Company registry interpretation reference](references/api-registry.md)
- [Account and credit reference](references/api-account.md)
- [Automatic signup and privacy reference](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Concise text summaries and Markdown tables of search results, company information, and market analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes returned filters, dates, locations, and amounts; contact details follow the service's privacy masking. Some successful queries consume credits.]

## Skill Version(s):

2.0.8 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
