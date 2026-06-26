## Description: <br>
Analyzes China A-share market themes using iTougu Theme Library data, including theme rankings, single-theme details, stock-theme relationships, and structured market insight reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QingYiXiaoYao](https://clawhub.ai/user/QingYiXiaoYao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to browse China A-share market themes, inspect theme drivers and related stocks, compare themes, and generate source-attributed Markdown analysis. The skill is intended for informational market research and not for investment advice. <br>

### Deployment Geography for Use: <br>
Global; analysis scope is limited to China A-share market data. <br>

## Known Risks and Mitigations: <br>
Risk: Generated market analysis could be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational only, retain the required investment-risk disclaimer, and avoid buy, sell, or precise price-target recommendations. <br>
Risk: The skill makes outbound read-only requests to public financial-data and search providers. <br>
Mitigation: Install only when those public providers are acceptable for the requested analysis, and review optional AKShare or search-tool dependencies separately. <br>
Risk: Upstream financial-data APIs may be unavailable, incomplete, or stale. <br>
Mitigation: Surface data-source attribution and missing-data notices in the report, and continue only with clearly identified available data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QingYiXiaoYao/subject-library) <br>
- [iTougu Theme Library API](https://group-api.itougu.com) <br>
- [Theme list endpoint](https://group-api.itougu.com/teach-hotspot/subject/fullList) <br>
- [Theme detail endpoint](https://group-api.itougu.com/teach-hotspot/subject/subjectDetail4Free) <br>
- [East Money quote API](https://push2.eastmoney.com/api/qt/ulist.np/get) <br>
- [AKShare](https://github.com/akfamily/akshare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Structured Markdown reports with tables, source attribution, optional Python snippets, and risk disclaimers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public financial-data requests; no credentials required; outputs should disclose data gaps and distinguish analysis from investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
