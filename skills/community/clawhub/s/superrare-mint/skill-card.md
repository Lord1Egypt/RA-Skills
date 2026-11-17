## Description:

Mint art to a SuperRare-compatible ERC-721 collection via Bankr, with explicit support for artist-given contracts and own-deployed SR factory contracts on Ethereum or Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to upload NFT media and metadata, then mint to SuperRare-compatible ERC-721 collections on Ethereum or Base through Bankr after choosing an artist-given or own-deployed collection mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected media and metadata to SuperRare endpoints, including before a full mint workflow broadcasts a transaction.

Mitigation: Provide only media intended for publication and inspect names, descriptions, tags, attributes, and token URIs before continuing to mint.

Risk: Broadcast mode can submit mint transactions through Bankr using BANKR_API_KEY.

Mitigation: Keep the default dry-run behavior until the printed chain, contract mode, contract address, function, receivers, and calldata preview have been reviewed.

Risk: Configurable API, RPC, contract, and receipt paths can redirect requests or mint against the wrong collection if local configuration is modified.

Mitigation: Prefer explicit command-line contract and deploy receipt paths, keep API endpoints at official defaults, and avoid running the skill where untrusted files can alter its configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaigotchi/skills/superrare-mint)
- [Publisher profile](https://clawhub.ai/user/aaigotchi)
- [SuperRare API endpoint](https://api.superrare.org)
- [Bankr API endpoint](https://api.bankr.bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output or receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mint previews are the default; successful broadcasts write JSON receipts.]

## Skill Version(s):

0.3.0 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
