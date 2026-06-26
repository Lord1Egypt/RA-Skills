## Description: <br>
Billions decentralized identity for agents that links agent DIDs to human identities using Billions ERC-8004 and Attestation Registries and supports authentication proof generation and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sahilkhan6006](https://clawhub.ai/user/sahilkhan6006) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create and list agent DIDs, sign and verify identity challenges, and link an agent identity to a human owner on the Billions Network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and uses persistent local private keys, and evidence notes weak default protection. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and restrict access to $HOME/.openclaw/billions. <br>
Risk: Supplying a real private key with --key can expose sensitive material through command history or process inspection. <br>
Mitigation: Prefer generating a new identity or use only controlled environments when importing an existing key. <br>
Risk: Linking and verification workflows send DID and authentication metadata to Billions and Privado services. <br>
Mitigation: Run linking or verification only after confirming user consent and the intended network destinations. <br>
Risk: Identity, challenge, credential, profile, and key files are stored outside the workspace. <br>
Mitigation: Review $HOME/.openclaw/billions permissions and contents before and after use. <br>


## Reference(s): <br>
- [Billions Network](https://billions.network/) <br>
- [Verified Agent Identity on ClawHub](https://clawhub.ai/sahilkhan6006/sahil-agent-unique-1777529868) <br>
- [sahilkhan6006 Publisher Profile](https://clawhub.ai/user/sahilkhan6006) <br>
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and JSON objects with Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist DID, challenge, credential, profile, and key material under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
