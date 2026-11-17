## Description:

Real-time on-chain settlement predictor for Ethereum, Bitcoin, Arbitrum, Optimism, Base, and Polygon with live fee tiers, mempool analysis, sandwich risk detection, transaction tracking, and fee trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethanwuqi-lang](https://clawhub.ai/user/ethanwuqi-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, traders, and blockchain operators use this skill to estimate gas or Bitcoin fees, predict settlement timing, inspect pending-pool risk, track transactions, and review fee trends across supported chains. It supports operational planning and transaction analysis, not guaranteed execution outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blockchain addresses, transaction hashes, and optional simulation details may be sent to public RPC, explorer, mempool.space, or Tenderly services.

Mitigation: Use the skill only with data you are comfortable sharing with those services, and avoid submitting sensitive wallet or transaction details when privacy is required.

Risk: Optional API credentials could expose account quota or metadata if reused broadly.

Mitigation: Use dedicated low-privilege Etherscan and Tenderly API keys for this skill, rotate them as needed, and keep them in environment variables rather than hard-coded files.

Risk: Local gas and fee history may be retained in the user's cache.

Mitigation: Delete ~/.cache/settlement-predictor when retained fee history is no longer needed.

Risk: Dependency behavior can change over time if packages are installed without pinned versions.

Mitigation: Install the skill in an isolated virtual environment and pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ethanwuqi-lang/skills/settlement-predictor)
- [Publisher profile](https://clawhub.ai/user/ethanwuqi-lang)
- [Etherscan API key setup](https://etherscan.io/myapikey)
- [Tenderly dashboard](https://dashboard.tenderly.co/)
- [mempool.space API](https://mempool.space/api)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON or terminal table text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimates, confidence labels, risk levels, recommendations, explorer URLs, and optional simulation results when configured.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
