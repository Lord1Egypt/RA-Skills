## Description:

Queries TickFlow real-time quotes and K-line market data for one or more stock, ETF, US equity, or Hong Kong equity symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cengsin](https://clawhub.ai/user/cengsin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch current quote summaries, compare multiple symbols, and retrieve recent K-line data from the TickFlow API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom --base-url value can send the TickFlow API key to an arbitrary server.

Mitigation: Use the default TickFlow endpoint; only use --base-url with a controlled destination and a non-production key, or remove or allowlist that option before use.

## Reference(s):

- [TickFlow API Notes](references/api.md)
- [Output Contract](references/output-contract.md)
- [TickFlow OpenAPI Schema](https://api.tickflow.org/openapi.json)
- [TickFlow API Endpoint](https://api.tickflow.org)
- [ClawHub Skill Page](https://clawhub.ai/cengsin/skills/tickflow-realtime)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text or markdown summaries and tables, with optional raw JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads TICKFLOW_API_KEY from the environment and suppresses API key output.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
