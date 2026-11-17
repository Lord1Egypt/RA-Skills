## Description:

Metal Dollar (XMD) stablecoin - mint, redeem, supply analytics, collateral reserves, and oracle prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect XMD treasury state, collateral reserves, balances, supply, and oracle prices, and to request mint or redeem transactions for supported XPR Network collateral.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write tools can sign real XPR Network financial transactions using environment credentials.

Mitigation: Install only with a dedicated, narrowly scoped XPR permission and small transaction limits.

Risk: Setting confirmed=true allows xmd_mint and xmd_redeem to submit transfers.

Mitigation: Require an external transaction preview or manual wallet confirmation before permitting confirmed=true.

Risk: Mint and redeem results depend on current treasury state, collateral enablement, pause status, caps, and oracle prices.

Mitigation: Check config, collateral status, reserves, and oracle price tools immediately before any write operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulgnz/skills/xmd)
- [XPR mainnet RPC endpoint](https://xpr-mainnet-rpc.saltant.io)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [Structured JSON tool responses with concise text guidance and transaction identifiers for submitted write operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only tools query XPR Network state; mint and redeem tools require explicit confirmation before signing.]

## Skill Version(s):

0.2.11 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
