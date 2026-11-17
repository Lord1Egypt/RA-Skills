## Description:

Verfi helps agents add TCPA consent capture to lead-generation forms, verify lead consent through the Verfi API, manage consent sessions, and retrieve proof for disputes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poncho-punch](https://clawhub.ai/user/poncho-punch)

### License/Terms of Use:


## Use Case:

Developers, lead-generation teams, and compliance operators use this skill to instrument consent capture, verify lead consent before contact, claim sessions for retention, and retrieve machine-readable proof for disputes or audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration enables broad form-activity recording.

Mitigation: Review Verfi's privacy, consent, retention, and tenant-access controls; provide explicit user notice and legally appropriate consent before recording; deploy the SDK only on required forms.

Risk: Secret-key powered API and MCP usage can expose sensitive tenant capabilities if keys are over-scoped or long-lived.

Mitigation: Use narrowly scoped, rotatable secret keys and grant only the session permissions required for the workflow.

Risk: The MCP example uses an unpinned npx package, which creates supply-chain exposure in production.

Mitigation: Pin and verify the MCP package and run it in a restricted environment before production use.

Risk: Client-side SDK loading can be altered if script integrity or deployment controls are weak.

Mitigation: Use CSP or integrity and version controls where possible, and monitor SDK deployment against approved pages and versions.

## Reference(s):

- [Verfi API Reference](references/api-reference.md)
- [Proof Data Schema](references/proof-schema.md)
- [Verfi SDK Reference](references/sdk-reference.md)
- [Verfi Dashboard](https://app.verfi.io)
- [Verfi OpenAPI Spec](https://api.verfi.io/.well-known/openapi.json)
- [ClawHub Skill Page](https://clawhub.ai/poncho-punch/skills/verfi)
- [ClawHub Publisher Profile](https://clawhub.ai/user/poncho-punch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include API calls, SDK snippets, proof checks, MCP configuration, and compliance workflow steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
