## Description: <br>
Searches and analyzes Qianlima-style procurement and tendering data for bid discovery, company analysis, market aggregation, and trend reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and business development teams use this skill to search Chinese procurement notices, inspect company bid activity, compare suppliers and purchasers, and summarize market trends from tendering data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends procurement queries, company names, and contact lookup requests to a third-party Qianlima/ZLBX API. <br>
Mitigation: Use it only when the user is comfortable sharing those queries with the service, and avoid confidential strategy or sensitive company research unless approved. <br>
Risk: Company matching and contact lookups may affect privacy or return entities outside the intended scope. <br>
Mitigation: Ask the agent to confirm company matches or contact lookup scope when privacy, compliance, or entity precision matters. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Store ZLBX_API_KEY in environment or approved agent configuration storage and do not paste it into prompts or generated documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/tender-search-qianlima) <br>
- [Bid search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [ZLBX API key setup](https://ai.zhiliaobiaoxun.com/?ch=s22) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown reports, tables, charts, and JSON-backed API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and sends procurement queries, company names, and related search terms to the Qianlima/ZLBX API.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
