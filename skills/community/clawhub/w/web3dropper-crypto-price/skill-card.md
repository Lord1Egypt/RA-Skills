## Description: <br>
Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Web3Dropper](https://clawhub.ai/user/Web3Dropper) <br>

### License/Terms of Use: <br>
UNLICENSED <br>


## Use Case: <br>
Developers, external users, and agent operators use this skill to create and manage Billions/Iden3 decentralized identities, link an agent DID to a human owner, sign challenges, and verify identity ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and stores long-lived identity keys and credentials under $HOME/.openclaw/billions, including unencrypted private keys. <br>
Mitigation: Use only on a trusted, access-controlled host; avoid shared workspaces and backups that capture this directory; treat DIDs, tokens, verification URLs, and credentials as sensitive. <br>
Risk: Server security evidence reports mismatched crypto-price artifacts in a skill whose behavior is identity linking. <br>
Mitigation: Review the installed package contents before broad use and require the publisher to remove unrelated crypto-price artifacts. <br>
Risk: Identity-linking and signing operations can fail or act on the wrong local identity if no default DID is configured. <br>
Mitigation: Check configured identities before signing or linking, create an identity only through the provided script when needed, and stop if a script exits with an error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Web3Dropper/web3dropper-crypto-price) <br>
- [Billions Network](https://billions.network/) <br>
- [Billions Wallet](https://wallet.billions.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and script outputs as text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the openclaw CLI; identity data is stored under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
