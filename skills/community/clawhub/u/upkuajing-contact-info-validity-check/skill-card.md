## Description: <br>
Checks phone numbers, email addresses, and domains through UpKuaJing's contact validity APIs and returns status, type, and related metadata for each contact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upkuajing](https://clawhub.ai/user/upkuajing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams, recruiters, traders, and data operations users can validate contact records before outreach, CRM cleanup, candidate screening, and supplier verification. The skill is intended for external API-backed contact validation workflows that may incur fees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends phone numbers, email addresses, and domains to UpKuaJing's external API for validation. <br>
Mitigation: Use it only when contact data may be shared with UpKuaJing and avoid submitting data that violates privacy, contractual, or regulatory requirements. <br>
Risk: Validation and account helper actions use a paid API and may create top-up or usage charges. <br>
Mitigation: Confirm current pricing with the provided pricing command or pricing page and obtain explicit user confirmation before fee-incurring checks or top-up actions. <br>
Risk: The API key can be stored in ~/.upkuajing/.env and is required for authenticated requests. <br>
Mitigation: Protect the local credentials file, restrict access to the environment variable, and rotate the key if it may have been exposed. <br>
Risk: The skill performs a limited daily version-check request to the UpKuaJing API service. <br>
Mitigation: Account for this outbound request in environments with strict network or telemetry policies. <br>


## Reference(s): <br>
- [Phone Validity API](references/phone-api.md) <br>
- [Email Validity API](references/email-api.md) <br>
- [Domain Validity API](references/domain-api.md) <br>
- [UpKuaJing Homepage](https://www.upkuajing.com) <br>
- [UpKuaJing Developer Platform](https://developer.upkuajing.com/) <br>
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validation results include totals, per-contact result objects, and fee information when returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
