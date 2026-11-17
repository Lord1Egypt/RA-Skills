## Description:

WhenToMeet group scheduling via public REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felixwortmann](https://clawhub.ai/user/felixwortmann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create, list, inspect, and manage WhenToMeet group scheduling events through the authenticated public API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill can delete events or cancel scheduling records through documented API endpoints.

Mitigation: Require explicit user confirmation before deletion or cancellation and verify the target resource identifier before issuing the request.

Risk: API calls can retrieve participant availability, booking details, and connected-calendar account information.

Mitigation: Retrieve sensitive scheduling or account details only when the user specifically requests them, and avoid storing or repeating unnecessary personal data.

Risk: Bearer API keys can allow account-level API access.

Mitigation: Use a scoped API key if available, keep credentials out of generated output, and rotate any key that may have been exposed.

## Reference(s):

- [WhenToMeet API Reference](references/API_REFERENCE.md)
- [Interactive API Docs](https://docs.whentomeet.io/api-docs)
- [OpenAPI Spec](https://whentomeet.io/api/openapi.json)
- [LLM-Friendly Product Overview](https://whentomeet.io/llms.txt)
- [WhenToMeet Main Site](https://whentomeet.io)
- [ClawHub Skill Page](https://clawhub.ai/felixwortmann/skills/whentomeet)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WhenToMeet Bearer API key.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
