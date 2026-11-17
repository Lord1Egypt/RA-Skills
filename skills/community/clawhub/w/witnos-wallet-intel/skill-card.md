## Description:

Profile any Base/EVM wallet or x402 buyer before you pay, front, or extend it credit, returning an onchain wallet score, whale detection, address risk, behavioral cluster, and named x402 spend graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andysalvo](https://clawhub.ai/user/andysalvo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, marketplace operators, and risk teams use this skill to profile unfamiliar Base/EVM wallets or x402 counterparties before paying, receiving funds, extending service, or granting credit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried wallet or counterparty addresses are sent to Crest Systems, which can reveal transaction-interest or business-intent information.

Mitigation: Use the skill only for addresses whose disclosure to Crest Systems is acceptable, and avoid confidential investigations unless that disclosure has been approved.

Risk: Paid wallet and service-trust checks may incur disclosed x402 fees.

Mitigation: Confirm the endpoint and fee before making paid calls, and reserve paid checks for cases where wallet intelligence is needed before transacting.

Risk: Wallet scores and spend history are decision-support signals, not financial advice or proof of counterparty safety.

Mitigation: Verify results against independent context before paying, extending service, or granting credit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andysalvo/skills/witnos-wallet-intel)
- [Witnos wallet intelligence endpoint](https://data.crestsystems.ai/data/wallet/{address})
- [Crest Systems service trust endpoint](https://data.crestsystems.ai/data/service-trust/{address})
- [Crest Systems x402 market endpoint](https://data.crestsystems.ai/data/x402-market)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance with HTTP endpoint references and response-field descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes paid and free Crest Systems wallet-intelligence checks; paid checks disclose queried addresses to Crest Systems and may incur x402 fees.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
