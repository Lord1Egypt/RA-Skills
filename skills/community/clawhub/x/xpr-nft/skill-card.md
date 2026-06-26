## Description: <br>
Manage the full AtomicAssets NFT lifecycle on XPR Network including creation, minting, selling, auctioning, transferring, and burning NFTs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query and manage AtomicAssets and AtomicMarket NFT operations on XPR Network, including collection setup, minting, transfers, sales, auctions, and burns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign real XPR Network NFT and marketplace transactions, which may be irreversible. <br>
Mitigation: Install with a dedicated low-value or least-privilege XPR account and require explicit user approval for every write action. <br>
Risk: Auction claiming needs additional review because evidence reports that one auction-claim action bypasses the documented confirmation pattern. <br>
Mitigation: Require explicit user approval before auction claiming and review the transaction details before signing. <br>
Risk: Misconfigured RPC endpoints or dependency sources can affect the integrity of blockchain reads and signed writes. <br>
Mitigation: Verify the configured RPC endpoint and the @proton/js dependency source before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulgnz/xpr-nft) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [JSON-like tool responses and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read operations return NFT and marketplace records; write operations may return blockchain transaction identifiers after explicit confirmation.] <br>

## Skill Version(s): <br>
0.2.11 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
