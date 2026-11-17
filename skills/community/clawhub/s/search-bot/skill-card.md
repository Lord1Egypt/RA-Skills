## Description:

Answer a question with a fresh web search through AIProx (aiprox.dev): one POST /v1/search for 35 sats, paid in Bitcoin Lightning (L402 or a LightningProx spend token). Returns a short AI answer with key findings and up to 5 source URLs. Use it when the user asks for current information from the web and agrees to pay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

People who need current web information use this skill to receive an AI-generated answer, key findings, and up to five source URLs after approving the 35-sat Lightning charge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A search call incurs a 35-sat charge.

Mitigation: Get the user's approval for the disclosed cost before calling, unless they already approved this price in the conversation.

Risk: Search queries are sent to AIProx, and an optional spend token is a bearer credential.

Mitigation: Avoid confidential queries; never expose the token; use a minimally funded token or have the user pay individual invoices.

Risk: Search answers and source links are subject to AIProx search-content restrictions.

Mitigation: Follow the disclosed terms on storing, sharing, reselling, redistribution, and AI training use.

## Reference(s):

- [AIProx](https://aiprox.dev)
- [AIProx API documentation](https://aiprox.dev/docs.html)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Short AI-generated answer with key findings and up to five source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid 35-sat Lightning request per search; query limit is 500 characters.]

## Skill Version(s):

2.0.0 (source: release evidence and changelog, released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
