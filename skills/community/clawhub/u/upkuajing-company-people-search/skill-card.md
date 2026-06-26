## Description: <br>
Search UpKuaJing company and people data, enrich selected records, and retrieve business, background, and contact information through the UpKuaJing Open Platform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warmc](https://clawhub.ai/user/warmc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, sourcing, recruiting, and due diligence users use this skill to find companies or people, inspect selected records, and request contact details for customer development, background research, and talent search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid API searches and enrichment calls can incur charges. <br>
Mitigation: Confirm the expected fee count with the user before running paid operations and use the pricing interface or pricing page for current rates. <br>
Risk: The skill requires a sensitive UpKuaJing API key. <br>
Mitigation: Use a dedicated API key, avoid sharing it in prompts or logs, and restrict access to the environment or local credential file where it is stored. <br>
Risk: Returned company, people, and contact results may contain sensitive personal or business data. <br>
Mitigation: Apply access controls, review lawful-use requirements, and delete saved result files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/warmc/upkuajing-company-people-search) <br>
- [UpKuaJing homepage](https://www.upkuajing.com) <br>
- [UpKuaJing Open Platform](https://developer.upkuajing.com/) <br>
- [UpKuaJing API pricing](https://www.upkuajing.com/web/openapi/price.html) <br>
- [Company List API reference](references/company-list-api.md) <br>
- [People List API reference](references/human-list-api.md) <br>
- [Company Detail API reference](references/company-detail-api.md) <br>
- [People Detail API reference](references/human-detail-api.md) <br>
- [Contact API reference](references/contact-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; scripts return JSON responses and JSONL result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, httpx, and UPKUAJING_API_KEY; paid searches and enrichments may create task result files.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
