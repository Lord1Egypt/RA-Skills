## Description:

Interact with QR Coin auctions on Base. Use when the user wants to participate in qrcoin.fun QR code auctions - check auction status, view current bids, create new bids, or contribute to existing bids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktaesthetix](https://clawhub.ai/user/ktaesthetix)

### License/Terms of Use:


## Use Case:

External users use this skill to inspect QR Coin auction state and prepare bids or contributions for QR code URL placement on Base. It provides command-line status queries and transaction guidance for USDC approvals and Bankr-assisted auction calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users into real USDC approvals and blockchain transactions on Base.

Mitigation: Verify the contract address, network, function, URL, and amount in Bankr or the wallet before signing.

Risk: Excessive token allowance can leave funds exposed after bidding.

Mitigation: Approve only the minimum needed and revoke unused allowances after the auction workflow.

Risk: Auction timing or reserve values can change before a user submits a transaction.

Mitigation: Query the active token ID, auction status, and reserve prices immediately before approving or bidding.

## Reference(s):

- [QR Coin](https://qrcoin.fun)
- [QR Auction Contract on BaseScan](https://basescan.org/address/0x7309779122069EFa06ef71a45AE0DB55A259A176)
- [USDC on Base](https://basescan.org/token/0x833589fCD6eDb6E08f4c7c32D4f71b54bdA02913)
- [Publisher Profile](https://clawhub.ai/user/ktaesthetix)
- [ClawHub Skill Page](https://clawhub.ai/ktaesthetix/skills/qrcoin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and transaction prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for status queries; Bankr or a wallet is used for transaction execution.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
