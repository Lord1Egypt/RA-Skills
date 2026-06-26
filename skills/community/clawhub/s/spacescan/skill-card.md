## Description: <br>
Access Chia blockchain data including blocks, transactions, addresses, CAT tokens, NFTs, network stats, and XCH price through the Spacescan.io API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Spacescan to perform read-only Chia blockchain lookups from CLI, Telegram, or JavaScript workflows. It is suited for checking blocks, transactions, balances, network state, token data, NFT details, and XCH price. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried blockchain addresses, hashes, and the Spacescan API key are sent to Spacescan.io. <br>
Mitigation: Use a scoped Spacescan API key where possible and avoid querying sensitive addresses or hashes from shared environments. <br>
Risk: Persisting SPACESCAN_API_KEY in shared shell profiles or synced dotfiles can expose the credential. <br>
Mitigation: Store the API key in a local secret manager or private environment file and avoid committing or syncing shell profiles that contain it. <br>
Risk: npm link installs global scan and spacescan commands. <br>
Mitigation: Skip npm link unless global commands are needed, and use local invocation for narrower exposure. <br>


## Reference(s): <br>
- [ClawHub Spacescan release](https://clawhub.ai/Koba42Corp/spacescan) <br>
- [Spacescan](https://www.spacescan.io) <br>
- [Spacescan API plans](https://www.spacescan.io/apis) <br>
- [Chia Network](https://chia.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Plain text and Markdown-style command responses with JavaScript API examples and shell configuration commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPACESCAN_API_KEY and sends queried addresses, hashes, and the API key to Spacescan.io.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
