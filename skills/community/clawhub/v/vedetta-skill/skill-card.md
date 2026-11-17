## Description:

Queries Vedetta's Base and Solana x402 endpoints for live or cached market intelligence on crypto, equities, and macro assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lacryptorina](https://clawhub.ai/user/lacryptorina)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can request descriptive market research, including sentiment, price divergence, news, predictions, and macro signals. Use it for research and monitoring, not trade execution or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that automatic payment signing may authorize more than the documented spending limit.

Mitigation: Use a dedicated low-balance wallet, check the live x402 offer, and abort if the requested amount exceeds the documented tier (up to $0.09 per live call).

Risk: The available security scan was partial because some local references were missing, so it does not establish that every referenced item was reviewed.

Mitigation: Review the referenced payment client scripts and configuration before enabling paid requests.

## Reference(s):

- [Vedetta service and API](https://vedetta.dethboy.com)
- [Vedetta install guide](https://vedetta.dethboy.com/install)
- [Base x402 manifest](https://vedetta.dethboy.com/.well-known/x402.json)
- [Solana x402 manifest](https://vedetta.dethboy.com/.well-known/x402-sol.json)
- [ClawHub release page](https://clawhub.ai/lacryptorina/skills/vedetta-skill)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Guidance]

**Output Format:** [Structured market data with concise research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One asset per call; descriptive market analysis only, not financial advice.]

## Skill Version(s):

2.14.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
