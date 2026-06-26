## Description: <br>
Provides Billions decentralized identity tooling for agents to create DIDs, link them to human identities, and verify authentication proofs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nopalempl](https://clawhub.ai/user/nopalempl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions Network decentralized identities for agents, link an agent DID to a human owner, and verify DID ownership through challenge-response signatures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent identity keys may be stored unencrypted if BILLIONS_NETWORK_MASTER_KMS_KEY is not configured. <br>
Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before generating or importing keys and treat $HOME/.openclaw/billions as sensitive. <br>
Risk: Signing or human-agent linking actions can prove DID control or start a human-agent verification flow from broad prompts. <br>
Mitigation: Require explicit confirmation before signing challenges or linking identities, and check existing identities before any linking operation. <br>
Risk: Passing real private keys on the command line can expose them through shell history or process inspection. <br>
Mitigation: Avoid command-line private-key arguments where possible and use secure secret handling for imported keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nopalempl/verifiedagentidentity) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or text script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; supports optional BILLIONS_NETWORK_MASTER_KMS_KEY configuration for key encryption.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
