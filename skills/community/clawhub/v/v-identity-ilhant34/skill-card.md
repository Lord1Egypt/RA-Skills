## Description: <br>
Billions decentralized identity for agents: link agents to human identities using Billions ERC-8004 and Attestation Registries, then generate or verify authentication proofs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilhant-34](https://clawhub.ai/user/ilhant-34) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to create and manage Billions Network DIDs, link an agent identity to a human owner, and verify identity ownership through signed challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys and identity data are stored under $HOME/.openclaw/billions, and keys may be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not set. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing an identity, restrict access to $HOME/.openclaw/billions, and keep that directory out of shared backups. <br>
Risk: Identity-linking and challenge-signing actions can bind an agent identity or produce authentication proof. <br>
Mitigation: Confirm each request before allowing the agent to create, link, or sign with an identity, and inspect challenge content before signing. <br>
Risk: The server security verdict is suspicious because the skill handles private keys and identity-linking flows. <br>
Mitigation: Install only if the publisher and Billions identity flow are trusted, and avoid passing private keys on the command line. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ilhant-34/v-identity-ilhant34) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DID strings, verification URLs, signed challenge results, and identity verification status from local Node.js scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
