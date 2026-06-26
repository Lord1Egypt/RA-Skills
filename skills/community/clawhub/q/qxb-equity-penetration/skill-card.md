## Description: <br>
基于工商数据源，深度解析企业股权结构，呈现直接股东、间接股东、持股比例和穿透路径，帮助识别企业股权架构与控制关系。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llx-26](https://clawhub.ai/user/llx-26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business analysts, investment due-diligence teams, compliance reviewers, and developers use this skill to query a company's direct and indirect shareholders and inspect ownership paths before transactions, partnerships, or control-structure reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends queried company names or enterprise IDs to Qixin's external API. <br>
Mitigation: Use it only where that external disclosure is acceptable and avoid submitting sensitive entities unless the data-sharing posture has been approved. <br>
Risk: Fuzzy company-name lookup may select the wrong entity. <br>
Mitigation: Prefer enterprise ID lookup for legal, investment, or compliance decisions, or verify the returned company name before relying on the result. <br>
Risk: Dependency reproducibility is weaker without a lockfile and with a broad axios version range. <br>
Mitigation: Pin and update axios and publish a lockfile before deployment in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/llx-26/qxb-equity-penetration) <br>
- [查询企业股权穿透 reference](references/getEquityPenetration.md) <br>
- [Qixin API token portal](https://www.qixin.com/app-center/home?route=skill-quota) <br>
- [Qixin external API base](https://external-api.qixin.com/skill/ent/public) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or JSON-backed API results describing direct shareholders, indirect shareholders, ownership percentages, and shortest ownership paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, axios, and QXBENT_API_TOKEN; company lookup accepts either a company name or enterprise ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
