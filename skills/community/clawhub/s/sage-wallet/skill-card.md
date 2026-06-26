## Description: <br>
Interact with the Sage Chia blockchain wallet via RPC for XCH transactions, CAT tokens, NFTs, DIDs, offers, options, coin management, and wallet configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and wallet operators use this skill to operate a local Sage Chia wallet through natural language or slash commands, including balance checks, transfers, token and NFT operations, offers, WalletConnect actions, and wallet configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate real cryptocurrency assets through wallet RPC actions. <br>
Mitigation: Use testnet or a low-value wallet first and require explicit review before sends, mints, offers, signing, broadcasts, key deletion, database deletion, or mnemonic retrieval. <br>
Risk: Wallet secrets, certificate/key files, and mnemonic material can be exposed if handled carelessly. <br>
Mitigation: Keep cert/key and mnemonic material private, avoid logging secrets, and use only trusted local RPC endpoints. <br>
Risk: The config loader uses eval-based shell behavior. <br>
Mitigation: Fix or avoid the eval-based config loader before deployment in sensitive environments. <br>


## Reference(s): <br>
- [Sage RPC Endpoints Quick Reference](artifact/references/endpoints.md) <br>
- [Sage Wallet project](https://github.com/xch-dev/sage) <br>
- [Chia Developer Documentation](https://docs.chia.net/) <br>
- [ClawHub Sage Wallet release](https://clawhub.ai/Koba42Corp/sage-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reference local Sage RPC endpoints, certificate paths, wallet fingerprints, and transaction payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
