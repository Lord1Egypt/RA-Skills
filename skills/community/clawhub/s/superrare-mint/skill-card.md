## Description: <br>
Mint art to a SuperRare-compatible ERC-721 collection on Ethereum or Base via Bankr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, artists, and agent operators use this skill to upload NFT media and metadata to SuperRare, preview mint calldata, and optionally submit an NFT mint transaction through Bankr after selecting an explicit contract mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broadcast mode can mint NFTs and submit blockchain transactions through Bankr. <br>
Mitigation: Keep dry-run enabled until the previewed chain, contract mode, contract address, receiver, royalty receiver, and token URI have been reviewed. <br>
Risk: The skill uses a Bankr API key and can read it from environment or local Bankr configuration files. <br>
Mitigation: Install and run only in an environment where Bankr credential access is intended, and avoid sharing credential-bearing configuration. <br>
Risk: The metadata workflow uploads selected art files and metadata to SuperRare before minting. <br>
Mitigation: Use metadata-only mode or dry-run review when inspecting token metadata before any broadcast. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaigotchi/superrare-mint) <br>
- [Skill homepage](https://github.com/aaigotchi/superrare-mint) <br>
- [SuperRare API endpoint](https://api.superrare.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, API calls, Files] <br>
**Output Format:** [Console output, JSON metadata and receipt files, and transaction preview details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; successful broadcasts write JSON receipts under receipts/.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
