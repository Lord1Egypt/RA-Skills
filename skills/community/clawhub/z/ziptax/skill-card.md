## Description: <br>
Looks up U.S. sales tax rates, jurisdiction-level tax breakdowns, freight and service taxability, product taxability codes, and account usage metrics through the ZipTax API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlakich](https://clawhub.ai/user/ericlakich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and finance operations teams use this skill to retrieve sales and use tax rates for U.S. addresses, ZIP codes, and coordinates, and to integrate ZipTax taxability data into applications. <br>

### Deployment Geography for Use: <br>
Global, for U.S. sales tax lookup use cases <br>

## Known Risks and Mitigations: <br>
Risk: Lookup requests send address, ZIP code, or coordinate data to ZipTax. <br>
Mitigation: Use the skill only with location data appropriate to share with ZipTax. <br>
Risk: API keys may be exposed when placed in URLs. <br>
Mitigation: Prefer the X-API-KEY request header and avoid logging URLs that include API keys. <br>
Risk: The bundled lookup script can run local code from specially crafted address text. <br>
Mitigation: Do not run scripts/lookup.sh with untrusted address text until the quoting issue is fixed; use direct API calls or a client with safe parameter handling. <br>


## Reference(s): <br>
- [ZipTax API Reference](references/api-reference.md) <br>
- [ZipTax API Platform](https://platform.zip.tax) <br>
- [ZipTax OpenAPI Specification](https://raw.githubusercontent.com/ZipTax/ziptax-reference/main/openapi/openapi.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/ericlakich/ziptax) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples, shell commands, and JSON response interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZIPTAX_API_KEY for live API calls; lookups may send location data to ZipTax.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
