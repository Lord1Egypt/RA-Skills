## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ARMANMA0100](https://clawhub.ai/user/ARMANMA0100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and operators use this skill to create and manage decentralized agent DIDs, link agents to human owners, sign challenges, and verify identity ownership proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived identity keys and stores sensitive identity data under $HOME/.openclaw/billions. <br>
Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and treat the storage directory as sensitive. <br>
Risk: Importing an existing private key can expose valuable wallet material to the skill environment. <br>
Mitigation: Avoid importing valuable wallet keys with --key; prefer a dedicated identity key for this workflow. <br>
Risk: Human-agent linking may create a persistent association between a human identity and an agent DID. <br>
Mitigation: Install and run the linking flow only when that association is intended and understood. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ARMANMA0100/verified-agent-identity-7) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON outputs from identity scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DIDs, challenge strings, verification URLs, JSON status responses, and signature verification messages.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
