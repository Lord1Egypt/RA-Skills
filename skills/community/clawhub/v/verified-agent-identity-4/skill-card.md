## Description: <br>
Billions decentralized identity for agents that links agents to human identities using Billions ERC-8004 and Attestation Registries, and verifies or generates authentication proofs based on the iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devkonten](https://clawhub.ai/user/devkonten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to create and manage Billions Network decentralized identities, link an agent DID to a human owner, and verify DID ownership through signed challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent Billions/iden3 signing keys and stores identity data under $HOME/.openclaw/billions. <br>
Mitigation: Install only when persistent agent identity is intended, use a dedicated key, and protect or back up the identity directory. <br>
Risk: Private keys can be stored in plaintext by default. <br>
Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing keys so private key entries are encrypted at rest. <br>
Risk: Signing or human-linking requests can share proofs tied to the agent identity. <br>
Mitigation: Approve signing and linking requests only after reviewing the requested challenge and understanding what proof will be shared. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/devkonten/verified-agent-identity-4) <br>
- [Billions Network](https://billions.network/) <br>
- [Billions Wallet](https://wallet.billions.network) <br>
- [Billions Identity Dashboard](https://identity-dashboard.billions.network) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and writes persistent identity data under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
