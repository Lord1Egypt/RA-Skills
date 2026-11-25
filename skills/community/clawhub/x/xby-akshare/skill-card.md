## Description:

AKShare MCP Server 是一个通过AKShare提供中国股票市场数据的模型上下文协议服务器，支持实时行情、历史数据、基本面分析等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to retrieve Chinese stock-market data, including real-time quotes, historical prices, market summaries, disclosures, financial indicators, news, rankings, and research data. The agent selects the relevant stock-data tool, collects required parameters, calls XiaoBenYang, and summarizes the returned data for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a dedicated key, avoid sharing the workspace, and rotate or remove the key after testing or deployment.

Risk: Requests and parameters are sent to XiaoBenYang rather than directly to AKShare.

Mitigation: Avoid sending sensitive or reusable credentials, and review whether query parameters are acceptable to share with XiaoBenYang.

Risk: Server security evidence reports stale cross-domain references.

Mitigation: Review the artifact before installation and confirm the stock-data behavior, endpoints, and credential handling match the intended release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/xby-akshare)
- [XiaoBenYang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON API results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and sends request parameters to XiaoBenYang rather than directly to AKShare.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
