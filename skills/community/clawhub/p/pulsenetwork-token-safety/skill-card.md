## Description:

Deterministic rug-pull and honeypot verdicts (CLEAR/CAUTION/AVOID) for tokens on 10 chains. Pay per scan via x402, about $0.015. No API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pulsenetwork](https://clawhub.ai/user/pulsenetwork)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate crypto tokens before buying, trading, recommending, or acting on them. It guides an agent to request explicit consent for paid scans, call PulseNetwork token-safety endpoints, and report deterministic CLEAR, CAUTION, or AVOID verdicts with supporting flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages proposing paid token scans even when the user did not ask for one.

Mitigation: Quote the scan price and obtain explicit user approval or a batch budget before each paid scan.

Risk: The referenced payment MCP package may handle wallet credentials and is not pinned in the artifact.

Mitigation: Pin and verify the MCP package version before use, and use only a dedicated low-balance wallet or user-managed environment secret.

Risk: A paid x402 challenge could request an amount or recipient that differs from the documented endpoint price.

Mitigation: Pay only the exact amount and asset in the signed 402 challenge for the documented origin; stop and report if the challenge exceeds the listed price.

Risk: A CLEAR verdict could be mistaken for investment advice.

Mitigation: Present CLEAR only as deterministic on-chain facts, never as a buy recommendation or price prediction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pulsenetwork/skills/pulsenetwork-token-safety)
- [PulseNetwork service homepage](https://onchainpulse.theaslangroupllc.com)
- [PulseNetwork x402 machine catalog](https://onchainpulse.theaslangroupllc.com/.well-known/x402)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown or plain text with token-safety verdicts, quoted red and green flags, consent prompts, endpoint calls, and wallet or MCP setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid scans require explicit user consent, price disclosure, and budget controls before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
