## Description: <br>
A 股 + 新三板 + H 股跨市场上市主体综合信息查询工具，一站式聚合两大资本市场的企业公开披露数据，标准化整合多维度字段，可快速完成单企业信息全景调取、多标的横向对比，高效解决跨市场上市企业信息零散、口径不一、查询繁琐的痛点，适配各类商业分析、投研研判、企业尽调等工作场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llx-26](https://clawhub.ai/user/llx-26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, investment researchers, due-diligence teams, and agent developers use this skill to query listed-company market, shareholder, and financial-report information across A shares, NEEQ, and H shares. It supports single-company lookup and cross-target comparison through the Qixin API using either enterprise name or enterprise ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends queries to a third-party Qixin API and depends on the quality and availability of that provider's data. <br>
Mitigation: Install only when the Qixin provider is trusted for the intended workflow, and verify critical investment, due-diligence, or compliance outputs against authoritative sources. <br>
Risk: The QXBENT_API_TOKEN is a credential used for API access. <br>
Mitigation: Store the token in an environment variable or secret manager, restrict access to it, and rotate it if exposure is suspected. <br>
Risk: Name-based lookup can use fuzzy matching and may return the first matched enterprise when the input is ambiguous. <br>
Mitigation: Prefer enterprise ID queries for high-stakes workflows, or verify the returned enterprise name before relying on the result. <br>
Risk: The release depends on npm packages, including axios. <br>
Mitigation: Review and pin dependencies before production deployment, and keep dependency scanning in the deployment process. <br>


## Reference(s): <br>
- [getListedInfo API reference](references/getListedInfo.md) <br>
- [Qixin API token and skill quota page](https://www.qixin.com/app-center/home?route=skill-quota) <br>
- [Qixin listed-company API endpoint](https://external-api.qixin.com/skill/ent/public) <br>
- [ClawHub release page](https://clawhub.ai/llx-26/qxb-listed-info) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Configuration guidance] <br>
**Output Format:** [Structured company listing data returned by the Qixin API, usually summarized as text or JSON by the calling agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, axios, and a QXBENT_API_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
