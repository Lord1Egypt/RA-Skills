## Description: <br>
销售税查询(免费版) helps developers query U.S. sales tax rates by address, ZIP code, or coordinates using the zip-tax.com API, with guidance for API-key setup, curl calls, and basic CLI-style usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building personal e-commerce or tax lookup workflows use this skill to generate commands and guidance for querying zip-tax.com sales tax rates and parsing state, county, city, and district rate components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address, ZIP code, or coordinate lookup data is sent to zip-tax.com. <br>
Mitigation: Use the skill only with data you are permitted to share with zip-tax.com, and avoid sensitive customer addresses unless that processing is approved. <br>
Risk: The ZIPTAX_API_KEY can be exposed if it is hard-coded, committed, or used in frontend code. <br>
Mitigation: Store the API key in an environment variable or secret manager and keep it out of repositories and client-side code. <br>
Risk: Broad activation wording could cause the skill to run outside explicit sales-tax lookup tasks. <br>
Mitigation: Narrow activation text or require an explicit sales-tax lookup request before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ziptax-tool-free) <br>
- [zip-tax.com API endpoint](https://api.zip-tax.com/request/v60) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript snippets, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZIPTAX_API_KEY and sends lookup inputs to zip-tax.com.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
