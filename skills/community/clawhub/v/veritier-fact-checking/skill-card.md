## Description:

Veritier helps agents gate tool calls against systems of record, verify factual claims, scan documents, and produce reconstructable signed workpapers for the checks performed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salomonhenao](https://clawhub.ai/user/salomonhenao)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill before an agent executes a tool call, publishes a factual answer, audits AI-generated text, or handles an untrusted document. The skill supports fail-closed action attestation, claim extraction and verification, private-reference checks, document validation, MCP setup, REST examples, and webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer API keys and submitted text, document content, URLs, or private references are sent to Veritier's hosted API.

Mitigation: Review data-sharing requirements before use, avoid submitting sensitive content unless approved, and keep VERITIER_API_KEY scoped and protected in the local environment.

Risk: The JavaScript integration test can send a bearer key to an API_URL value controlled by the environment.

Mitigation: Use VERITIER_TEST_KEY for integration tests and do not run javascript/quickstart/test_integration.mjs with a production key when API_URL can be influenced.

Risk: Example dependencies and generated API calls may change behavior if dependencies are installed without version control.

Mitigation: Pin and review dependencies before production use.

Risk: Claim Credentials prove what was checked and decided, but they are not certificates of truth or legal findings.

Mitigation: Use credentials as audit workpapers and keep human review or domain-specific controls for high-impact decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/salomonhenao/skills/veritier-fact-checking)
- [Veritier Website](https://veritier.ai)
- [Hosted Skill File](https://veritier.ai/skill.md)
- [Examples README](https://veritier.ai/README.md)
- [Live OpenAPI](https://api.veritier.ai/openapi.json)
- [Interactive API Docs](https://api.veritier.ai/docs)
- [Hosted MCP Endpoint](https://api.veritier.ai/mcp/)
- [API Key Dashboard](https://veritier.ai/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration, shell commands, code examples, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include claim verdicts, confidence scores, source URLs, document validation results, setup guidance, and signed Claim Credential identifiers.]

## Skill Version(s):

3.4.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
