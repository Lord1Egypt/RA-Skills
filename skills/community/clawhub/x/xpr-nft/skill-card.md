## Description:

Manage the full AtomicAssets NFT lifecycle on XPR Network, including creation, minting, selling, auctioning, transferring, burning, and querying NFTs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to manage AtomicAssets and AtomicMarket NFT workflows on XPR Network. It supports collection, schema, template, asset, sale, and auction operations, including write actions that can submit blockchain transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet signing and blockchain write operations may move assets, spend tokens, consume resources, or be irreversible.

Mitigation: Use a dedicated low-value XPR account, a restricted permission rather than active, and a trusted HTTPS RPC endpoint; review every write request before setting confirmed=true.

Risk: Credential requirements for write operations are under-disclosed.

Mitigation: Document and provision XPR_PRIVATE_KEY, XPR_ACCOUNT, XPR_PERMISSION, and XPR_RPC_ENDPOINT only in a secure runtime, and rotate or revoke credentials if exposure is suspected.

Risk: One auction-claim write action bypasses the skill's stated confirmation rule.

Mitigation: Manually review auction claim requests and restrict wallet permissions until confirmation handling is fixed or enforced by surrounding policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulgnz/skills/xpr-nft)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, API calls]

**Output Format:** [Markdown guidance and JSON-like tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations may sign and submit XPR Network transactions when wallet environment variables are configured.]

## Skill Version(s):

0.2.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
