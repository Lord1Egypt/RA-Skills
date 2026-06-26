## Description: <br>
Official skill for UpKuaJing that finds companies and global buyers using customs trade data, retrieves trade order details, business contact information, and lead generation data for import/export market research and supply chain analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warmc](https://clawhub.ai/user/warmc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trade researchers use this skill to query UpKuaJing customs trade data, identify buyers or suppliers, inspect trade records, and enrich company results with details or contact information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an UpKuaJing API key and stores it locally when generated through the auth script. <br>
Mitigation: Use a dedicated API key where possible, avoid sharing the key, and remove it from local storage when it is no longer needed. <br>
Risk: API calls may incur fees, including list searches, company detail lookups, contact lookups, and top-up flows. <br>
Mitigation: Confirm query counts, fee counts, and any payment URL with the user before executing paid operations. <br>
Risk: Search results may contain sensitive business leads or contact information saved in local task_data files. <br>
Mitigation: Delete local result files when they are no longer needed and handle exported lead or contact data according to the user organization's data handling rules. <br>


## Reference(s): <br>
- [Company Detail API Reference](references/company-detail-api.md) <br>
- [Company List API Reference](references/company-list-api.md) <br>
- [Contact Fetch API Reference](references/contact-fetch-api.md) <br>
- [Trade List API Reference](references/trade-list-api.md) <br>
- [UpKuaJing Homepage](https://www.upkuajing.com) <br>
- [UpKuaJing Open Platform](https://developer.upkuajing.com/) <br>
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses, JSONL result files, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [List-search scripts write task metadata and result.jsonl files under task_data; detail and contact scripts print JSON responses that include fee information.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
