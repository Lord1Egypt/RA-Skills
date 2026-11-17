## Description:

Generates Python Solana trading bot code that uses Jupiter v6 for swaps and DexScreener data, with priority-fee handling and environment-variable key management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wterry57](https://clawhub.ai/user/wterry57)

### License/Terms of Use:


## Use Case:

Developers and trading-bot builders use this skill to generate Solana bot scaffolds, including Python code, dependency lists, and environment templates for Jupiter and DexScreener workflows. Generated code should be reviewed carefully before any live trading use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated bots may be used for live trading without enough guardrails for real-money loss.

Mitigation: Use devnet or paper trading until explicit live-trading confirmation, slippage limits, and position limits are added and reviewed.

Risk: Wallet private keys could be exposed or over-privileged in generated bot workflows.

Mitigation: Use a dedicated low-value wallet key, keep keys in environment variables, and never expose a primary wallet private key to generated code.

Risk: Unpinned or unaudited dependencies can introduce supply-chain or runtime risk.

Mitigation: Pin dependencies and run dependency auditing before installing or deploying generated bot code.

## Reference(s):

- [Jupiter v6 Quote API](https://quote-api.jup.ag/v6)
- [DexScreener API](https://dexscreener.com)
- [ClawHub Skill Page](https://clawhub.ai/wterry57/skills/solana-sniper-architect)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown containing Python code, requirements, and environment template snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include main.py, requirements.txt, and .env template content for generated trading bots.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
