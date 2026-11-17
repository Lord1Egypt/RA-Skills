## Description:

Screens Ethereum and other EVM wallet addresses against the ScamSniffer community-maintained blocklist of reported phishing, wallet-drainer, and scam addresses without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and crypto operations teams use this skill to quickly check whether an EVM address appears on a known scam or wallet-drainer blocklist before sending funds, signing transactions, claiming airdrops, or minting NFTs. It should be used as one fast screening signal, not as a final safety determination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean result may be mistaken for proof that a wallet or contract is safe.

Mitigation: State that a clean result is only a miss from this specific blocklist and recommend independent checks such as contract review, transaction simulation, and additional threat-intelligence sources before moving value.

Risk: The skill downloads a community-maintained blocklist from GitHub and caches it locally for 6 hours, so results can be stale or unavailable during network or source outages.

Mitigation: Disclose the source and cache behavior, use refresh mode when the latest public feed is needed, and treat stale-cache results as time-limited evidence.

Risk: Coverage is limited to Ethereum-style EVM addresses and one community-maintained list.

Mitigation: Do not use the skill for non-EVM chains, and combine its output with chain-specific analysis or paid threat-intelligence services for higher-value decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/scam-wallet-screener)
- [ScamSniffer scam-database](https://github.com/scamsniffer/scam-database)
- [ScamSniffer address blocklist feed](https://raw.githubusercontent.com/scamsniffer/scam-database/main/blacklist/address.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text screening report or JSON object with blocklist size and per-address results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are based on a public community blocklist cached locally for 6 hours unless refreshed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
