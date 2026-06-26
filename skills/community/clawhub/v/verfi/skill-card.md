## Description: <br>
Verfi helps agents guide TCPA consent verification for lead generation, including consent capture on web forms, pre-contact lead checks, session claim management, proof retrieval, API authentication, SDK setup, and create-to-proof workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poncho-punch](https://clawhub.ai/user/poncho-punch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and lead-generation teams use this skill to add Verfi consent capture to web forms, verify TCPA consent before contacting leads, claim sessions for retention, and retrieve proof for audits or disputes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SDK records form interactions, device details, hashed PII, and consent signals, which can affect privacy and compliance obligations. <br>
Mitigation: Confirm Verfi's legal basis, privacy notices, and data-processing terms before adding the SDK to production forms. <br>
Risk: Secret API keys can search sessions, retrieve proof, and mutate consent-record retention when granted broad scopes. <br>
Mitigation: Keep secret keys server-side, grant only the minimum required scopes, and require confirmation before claim, unclaim, or expiration-update actions. <br>
Risk: The documented MCP server receives a Verfi API key and can expose API actions to an agent runtime. <br>
Mitigation: Review the MCP package and tenant authorization model before providing an API key, and use it only in trusted agent environments. <br>


## Reference(s): <br>
- [Verfi Skill Page](https://clawhub.ai/poncho-punch/verfi) <br>
- [Verfi API Reference](references/api-reference.md) <br>
- [Proof Data Schema](references/proof-schema.md) <br>
- [Verfi SDK Reference](references/sdk-reference.md) <br>
- [Verfi Dashboard](https://app.verfi.io) <br>
- [Verfi OpenAPI Spec](https://api.verfi.io/.well-known/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with API examples, JSON snippets, shell commands, and configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include consent-verification workflow steps, API request examples, SDK setup snippets, and MCP server configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
