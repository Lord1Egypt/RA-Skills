## Description: <br>
Official skill for upkuajing (跨境魔方). Find companies (找公司) and global people (找人) data. Get business registration, background info, and contact details (Email, Phone, WhatsApp). Ideal for customer development, background checks, and talent search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upkuajing](https://clawhub.ai/user/upkuajing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Exporters, sourcing agents, sales teams, and business-development users use this skill to search global companies and people, enrich records, retrieve contact details, and prepare B2B lead-development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive UpKuaJing API key and stores it for local script use. <br>
Mitigation: Set UPKUAJING_API_KEY through an environment secret or secret manager, and avoid printing or sharing local credential files. <br>
Risk: Searches and enrichment requests can incur UpKuaJing API charges. <br>
Mitigation: Confirm the expected number of paid calls and receive explicit user approval before running fee-incurring searches or batch enrichment. <br>
Risk: Company, people, and contact searches can create local result or task data containing business contact information. <br>
Mitigation: Use the data only for the approved contact-data use case and delete local task data or logs when they are no longer needed. <br>


## Reference(s): <br>
- [UpKuaJing Website](https://www.upkuajing.com) <br>
- [UpKuaJing Open Platform](https://developer.upkuajing.com/) <br>
- [UpKuaJing API Pricing](https://www.upkuajing.com/web/openapi/price.html) <br>
- [Company List API Reference](references/company-list-api.md) <br>
- [People List API Reference](references/human-list-api.md) <br>
- [Company Detail API Reference](references/company-detail-api.md) <br>
- [People Detail API Reference](references/human-detail-api.md) <br>
- [Contact API Reference](references/contact-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands, configuration notes, JSON API responses, and local result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY and may perform paid API calls after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence release version and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
