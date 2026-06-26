## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obrezhniev](https://clawhub.ai/user/obrezhniev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions Network decentralized identities for agents, link an agent DID to a human owner, sign identity challenges, and verify DID ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive identity keys and may store private key material in $HOME/.openclaw/billions/kms.json. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before first use, restrict permissions on $HOME/.openclaw/billions, and keep the directory outside shared workspaces. <br>
Risk: Importing an asset-holding Ethereum wallet key could expose funds or enable impersonation if the local key store is compromised. <br>
Mitigation: Use a dedicated identity key only; never import an Ethereum wallet key that controls assets. <br>
Risk: Identity linking and signature operations depend on Billions identity services and npm dependencies. <br>
Mitigation: Decide whether those services and dependencies are trusted before installation, and stop immediately if any script exits with a non-zero status. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/obrezhniev/the-verified-agent-identity) <br>
- [Publisher Profile](https://clawhub.ai/user/obrezhniev) <br>
- [Billions Network](https://billions.network/) <br>
- [Billions Wallet](https://wallet.billions.network) <br>
- [Billions Identity Dashboard](https://identity-dashboard.billions.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local identity state under $HOME/.openclaw/billions when its documented Node.js scripts are executed.] <br>

## Skill Version(s): <br>
1.12.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
