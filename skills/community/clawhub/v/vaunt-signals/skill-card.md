## Description:

Vaunt signals provides real-money trading evidence from a live Hyperliquid engine through free and paid x402 routes that return BUY/NO signals, trade evidence, execution costs, and scorecards without an account or API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkdavey](https://clawhub.ai/user/jkdavey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Vaunt's crypto trading signal service for current BUY/NO answers, supporting evidence, execution costs, and recent scorecards. Paid routes use x402 USDC payments on Base and return financial signal outputs for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid routes spend USDC via x402 and return financial signal outputs.

Mitigation: Confirm user intent and route price before paid calls, and use only a wallet or signer intended for these requests.

Risk: Trading signal outputs may be wrong or unsuitable for a user's financial situation.

Mitigation: Treat responses as evidence for review rather than guaranteed investment advice, and compare paid results with the free scorecard and evidence endpoints before acting.

## Reference(s):

- [Vaunt agent homepage](https://vaunt-dispatch-production.up.railway.app/agent)
- [ClawHub skill page](https://clawhub.ai/jkdavey/skills/vaunt-signals)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON, Code]

**Output Format:** [Markdown guidance with route tables and JavaScript examples; service responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes free endpoints and paid x402 routes priced in USDC on Base.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
