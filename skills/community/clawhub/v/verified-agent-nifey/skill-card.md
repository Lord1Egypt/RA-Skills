## Description: <br>
Billions decentralized identity for agents links agents to human identities using Billions ERC-8004 and Attestation Registries and supports authentication proof generation and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mangfiksi](https://clawhub.ai/user/mangfiksi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create and manage Billions Network decentralized identities, sign verification challenges, link an agent DID to a human owner, and verify DID ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent identity keys may be stored in plaintext if BILLIONS_NETWORK_MASTER_KMS_KEY is not set. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing any identity and restrict local access to $HOME/.openclaw/billions. <br>
Risk: Imported or valuable wallet private keys could expose broader assets if reused for agent identity operations. <br>
Mitigation: Use a dedicated identity key for this skill and avoid importing valuable wallet private keys. <br>
Risk: Secrets passed as command-line arguments may be visible through shell history or process inspection. <br>
Mitigation: Avoid passing secrets through command-line arguments and prefer protected environment or key-management flows. <br>
Risk: Signing or linking an untrusted challenge can create an unintended identity assertion. <br>
Mitigation: Only sign or link challenges that the user intentionally trusts and understands. <br>


## Reference(s): <br>
- [Verified Agent Nifey on ClawHub](https://clawhub.ai/mangfiksi/verified-agent-nifey) <br>
- [mangfiksi publisher profile](https://clawhub.ai/user/mangfiksi) <br>
- [Billions Network](https://billions.network/) <br>
- [Billions Wallet](https://wallet.billions.network) <br>
- [Billions Identity Dashboard](https://identity-dashboard.billions.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent local identity, challenge, credential, and key files under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
