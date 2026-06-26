## Description: <br>
Billions decentralized identity for agents that links agents to human identities using Billions ERC-8004 and Attestation Registries, and verifies or generates authentication proofs based on the iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[layman88](https://clawhub.ai/user/layman88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage local decentralized identities for AI agents, link an agent DID to a human owner, sign identity challenges, and verify signed proofs of identity ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates, stores, and uses long-lived private identity keys. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and protect $HOME/.openclaw/billions as sensitive local identity storage. <br>
Risk: Supplying a valuable or reusable wallet private key with --key can persist sensitive key material for agent identity operations. <br>
Mitigation: Prefer a generated or isolated agent identity key, and do not pass valuable wallet keys to the skill. <br>
Risk: Linking or signing requests can associate an agent DID with a human owner or generate a verification URL. <br>
Mitigation: Confirm the linking request and challenge details before allowing the agent to sign or generate a verification URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/layman88/vai-layman88) <br>
- [Publisher profile](https://clawhub.ai/user/layman88) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or text script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local DID records, challenges, credentials, and key material under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
