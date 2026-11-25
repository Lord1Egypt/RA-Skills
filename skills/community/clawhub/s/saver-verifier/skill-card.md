## Description:

Fact-checking API for research reports and factual claim verification. Before publishing, verify a factual claim against its cited source. Send the claim and optionally a source URL as context. Get a model-assessed verdict, linked evidence, and sources for 0.20 USDC per completed check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saver-si](https://clawhub.ai/user/saver-si)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, writers, and agents use this skill to check factual claims against cited sources before publishing. It submits a claim and optional source URL for a model-assessed verdict with linked evidence and sources; each completed check costs 0.20 USDC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Claims and optional source context are sent to an external verification service, and completed checks incur a 0.20 USDC charge.

Mitigation: Review the information before sending and require explicit approval for each charge or an existing bounded spending policy before authorizing payment.

Risk: The recovery token is a secret used to retrieve a retained result.

Mitigation: Generate a random token, keep it out of URLs and logs, and reuse it only for the same claim, context, and response version.

## Reference(s):

- [SAVER Verifier skill page](https://clawhub.ai/saver-si/skills/saver-verifier)
- [Agent tool schema and transport](https://saververify.com/agent-tool.json)
- [Example verification reports](https://saververify.com/examples.json)
- [API contract](https://api.saververify.com/openapi.json)
- [x402 payment requirements](https://api.saververify.com/.well-known/x402)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Structured verification result with a model-assessed verdict, evidence links, and sources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each completed check costs 0.20 USDC. Confidence is model-assessed and is not a calibrated probability.]

## Skill Version(s):

1.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
