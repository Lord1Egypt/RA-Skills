## Description: <br>
Helps agents query and analyze Zhiliaobiaoxun procurement, bidding, award, company, supplier, competitor, market, and price-trend data through documented API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and procurement analysts use this skill to search bid notices, inspect award details, analyze companies and competitors, identify likely suppliers, and summarize procurement market trends from Zhiliaobiaoxun data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Procurement, supplier, competitor, company, and contact lookup queries are sent to a third-party Zhiliaobiaoxun service using the user's API key. <br>
Mitigation: Use the skill only for queries appropriate to share with that service and avoid including unnecessary sensitive details. <br>
Risk: Broad searches can expose or process more business information than needed for the task. <br>
Mitigation: Specify exact entities, date ranges, regions, and product terms so requests stay narrowly scoped. <br>
Risk: Company matching and market analysis may return related entities that need business review before action. <br>
Mitigation: Review matched company lists and analysis outputs before relying on them for procurement or competitive decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/zlbx-bidding-skill) <br>
- [Artifact: skill instructions](SKILL.md) <br>
- [Artifact: bid search API reference](references/api-search.md) <br>
- [Artifact: company analysis API reference](references/api-company.md) <br>
- [Artifact: market analysis API reference](references/api-market.md) <br>
- [Zhiliaobiaoxun API key setup](https://ai.zhiliaobiaoxun.com/?ch=s01) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API request guidance, configuration] <br>
**Output Format:** [Markdown or text with JSON API request examples and summarized bid-intelligence results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and sends user procurement, company, supplier, competitor, and contact lookup queries to the Zhiliaobiaoxun API.] <br>

## Skill Version(s): <br>
1.4.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
