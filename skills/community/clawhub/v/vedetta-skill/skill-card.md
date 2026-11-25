## Description:

Provides pay-per-call market intelligence for crypto, stocks, and macro through Base USDC and Solana x402 endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lacryptorina](https://clawhub.ai/user/lacryptorina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Vedetta to retrieve free, cached, or paid market sentiment, narrative, divergence, odds, news, prediction, and event analysis for crypto, US stocks, and macro. The results are descriptive research and are not financial advice or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the automatic payment client may sign an offer above its stated price limit; the scan was partial and some local references were unresolved.

Mitigation: Use a dedicated low-balance wallet, check each payment offer's network, amount, and payTo at runtime, and abort when the requested amount exceeds the expected tier.

## Reference(s):

- [Vedetta service](https://vedetta.dethboy.com)
- [Vedetta install instructions](https://vedetta.dethboy.com/install)
- [8004 specification](https://8004.qnt.sh)
- [Vedetta 8004 metadata](https://vedetta.dethboy.com/.well-known/8004-vedetta.json)

## Skill Output:

**Output Type(s):** [Analysis, JSON, API Calls]

**Output Format:** [Structured market data with concise descriptive analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One asset per call; descriptive market analysis only, not financial advice.]

## Skill Version(s):

2.14.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
